from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from collections import defaultdict

from django.contrib.auth import authenticate, login,logout
from django.db.models import F, Max
from asgiref.sync import sync_to_async

from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from datetime import datetime, timedelta



def get_latest_active_auctions(category,is_staff):
        if  is_staff ==True:
            latest_auctions = Auction.objects.filter(
                product__product_group=category,
                auction_status=True,
                product__user__is_staff=is_staff, #by admin
            ).order_by('-created_at')[:4]
            return latest_auctions
        else :
            latest_auctions = Auction.objects.filter(
                auction_status=True,
                product__user__is_staff=is_staff, #by Customer 
            ).order_by('-created_at')[:6]
            auctions_by_category = defaultdict(list)

            for auction in latest_auctions:
                category_name = auction.product.product_group.name
                auctions_by_category[category_name].append(auction)

            # Convert defaultdict to regular dict for better readability
            auctions_by_category = dict(auctions_by_category)
            return auctions_by_category

def Home(request,category=None):
    if category ==None :
         category=Category.objects.get(name ='Mobile')
    categories = Category.objects.all()
    latest_active_auctions=get_latest_active_auctions(category,True)
    latest_customers_active_auctions=get_latest_active_auctions(category,False)
    context = {
        "categories": categories,
        'latest_active_auctions':latest_active_auctions,
        'latest_customers_active_auctions':latest_customers_active_auctions
    }
    return render(request, 'home/home.html', context)
from .models import Customer  # استيراد النموذج Customer
@csrf_exempt
def register(request):
    if request.method == 'POST':
        # استخراج البيانات المدخلة من الاستمارة
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['confirm']
        phone_number = request.POST['telephone']  # إضافة استخراج رقم الهاتف

        # التحقق من ملء جميع الحقول المطلوبة
        if not first_name or not last_name or not email or not password or not password_confirm or not phone_number:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('Register')

        # التحقق من تطابق كلمة المرور مع تأكيد كلمة المرور
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return redirect('Register')

        # التحقق من عدم تكرار البريد الإلكتروني
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken.')
            return redirect('Register')
        # التحقق من عدم تكرار  الهاتف 
        if Customer.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'Phone number is already taken.')
            return redirect('register')
        # إنشاء مستخدم جديد
        user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
        user.save()

        # إنشاء عميل جديد وربطه بالمستخدم
        customer = Customer.objects.create(user=user, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
        customer.save()

        messages.success(request, 'Account created successfully. You can now log in.')
        return redirect('Register')

    return render(request, 'Register/register.html')
@csrf_exempt
def Login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('Home')  # تحويل المستخدم إلى الصفحة الرئيسية
        else:
                messages.error(request, 'Invalid email or password.')
    return render(request , 'Login/login.html')
def logout_view(request):
    logout(request)
    print('seccuess')
    # Redirect to a success page
    return redirect('Home')
def auction_details(request, auction):
    get_auction = Auction.objects.get(id=auction)
    context={
         'auction':get_auction,
    }
    return render(request,'auction_details/auction_details.html',context)
@csrf_exempt  
def auction_search(request):
    if request.method == 'POST':
        auction_name = request.POST['search']
        # ابحث عن المزاد باستخدام الجزء من اسمه ورتب النتائج حسب الاحدث
        auctions = Auction.objects.filter(product__name__icontains=auction_name,auction_status=True).order_by('-auction_start_date')
        return render(request, 'auction_search_results/auction_search_results.html', {'auctions': auctions})
    else:
        return redirect('Home') 
@sync_to_async   
def calc_highest_price(auction_id):
    auction = Auction.objects.get(pk=auction_id)
    bid = Bid.objects.filter(auction=auction)
    highest_bid = Bid.objects.filter(auction=auction).aggregate(Max('bid_amount'))['bid_amount__max']
    if highest_bid is not None:
        auction.current_price=highest_bid
        auction.save()
        return float(highest_bid)
    return None

def auction_page(request,auction_id): 
    auction = Auction.objects.get(id=auction_id )
    print(auction.auction_end_date)
    context={
        'auction':auction,
        'current_time': timezone.now(),
    }
    return render (request,'Auction/Auction.html',context)
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        starting_price = request.POST.get('starting_price')
        product_group_id = request.POST.get('product_group')
        main_image = request.FILES.get('main_image')
        additional_images = request.FILES.getlist('additional_images')
        auction_start_date = request.POST.get('starting_date')
        number_of_days = request.POST.get('NumberOfDays')
        minimum_bid_increment=request.POST.get('minimum_bid_increment')
        print(product_group_id)

        errors = {}
    
        # Validation
        if not name:
            errors['name'] = 'Please enter the product name.'
        if not description:
            errors['description'] = 'Please enter the product description.'
        if not starting_price:
            errors['starting_price'] = 'Please enter the starting price.'
        if not product_group_id:
            errors['product_group'] = 'Please select a product group.'
        if not main_image:
            errors['main_image'] = 'Please upload the main image.'

        if errors:

            return JsonResponse({'success': False, 'errors': errors})

        # Save product
        try:
            product_group = Category.objects.get(pk=product_group_id)
            print('product_group',product_group)
            product = Product.objects.create(
                user=request.user,
                name=name,
                description=description,
                starting_price=starting_price,
                main_image=main_image,
                product_group=product_group,
            )

            # Save additional images
            for image in additional_images:
                ProductImage.objects.create(
                    product=product,
                    image=image
                )
            auction_start_date = datetime.strptime(auction_start_date, '%Y-%m-%dT%H:%M')

            number_of_days=int(number_of_days)
            auction = Auction.objects.create(
                product= product,
                auction_start_date = auction_start_date,
                current_price = starting_price,
                auction_status=False ,
                minimum_bid_increment=minimum_bid_increment,
                auction_end_date =  auction_start_date + timedelta(days=number_of_days)


            )
            auctionRequest=AuctionRequest.objects.create(
            Auction=auction,
            user= request.user 

            )
            categories = Category.objects.all()
            return render(request, 'add_product/add_product.html', {'categories': categories}) 
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'message': str(e)})

    categories = Category.objects.all()
    return render(request, 'add_product/add_product.html', {'categories': categories})

def auction_by_category(request , category_id):
    category = Category.objects.get(name=category_id)
    auctions = Auction.objects.filter(
            product__product_group=category,
            auction_status=True,
        ).order_by('-auction_start_date')
    return render(request, 'auction_search_results/auction_search_results.html', {'auctions': auctions})

def auctions_by_customer(request):
    active_auctions_by_customers = Auction.objects.filter(
    product__user__is_staff=False,  # Assuming 'is_staff' is False for customers
    auction_status=True  # Only active auctions
    ).order_by('-auction_start_date')
    return render(request, 'auction_search_results/auction_search_results.html', {'auctions': active_auctions_by_customers})
def auctions_history(request):
    user = request.user
    auctions = Auction.objects.filter(product__user=user).order_by('-created_at')
    context = {
        'auctions': auctions
    }
    return render(request, 'auction_history/auction_history.html',context)

def save_winner_for_auction(auction_id):
    print('save_winner_for_auction')
    try:
        print(' try save_winner_for_auction')
        # الحصول على المزاد
        auction = Auction.objects.get(pk=auction_id)

        # الحصول على أعلى مزايدة
        highest_bid = Bid.objects.filter(auction=auction).order_by('-bid_amount').first()
        print('highest_bid', highest_bid)
        if highest_bid:
            # التحقق إذا كان هناك سجل فائز بنفس الفائز ونفس المزاد
            existing_winner = Winner.objects.filter(auction=auction, customer=highest_bid.customer).first()
            if existing_winner:
                existing_winner.delete()
                print("Existing winner record deleted.")

            # إنشاء وحفظ الفائز في جدول الفائزين
            winner = Winner(
                auction=auction,
                customer=highest_bid.customer,
                winning_bid=highest_bid.bid_amount,
                win_date=timezone.now()
            )
            winner.save()

            print("Winner saved successfully.")
        else:
            print("No bids found for this auction.")

    except Auction.DoesNotExist:
        return {"success": False, "message": "Auction not found."}
