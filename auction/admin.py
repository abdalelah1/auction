from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Customer)

admin.site.register(Category)
class ProductImageInline(admin.TabularInline):  # أو admin.StackedInline حسب التصميم المطلوب
    model = ProductImage
    extra = 1  # عدد النماذج الفارغة التي يمكن إضافتها

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ['product', 'auction_start_date', 'auction_end_date', 'current_price', 'auction_status', 'minimum_bid_increment']
    list_filter = ['auction_start_date', 'auction_end_date', 'auction_status']
    ordering = ['-auction_start_date']  # ترتيب السجلات حسب الاقدمية

admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid)

class AuctionRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'request_date', 'admin_message', 'is_approved', 'Auction')
    list_filter = ('is_approved', 'request_date')
    search_fields = ('user__username', 'admin_message')

    actions = ['approve_requests']

    def approve_requests(self, request, queryset):
        print("approve_requests called")  # تأكيد استدعاء التابع
        for auction_request in queryset:
            if auction_request.is_approved != True:
                auction_request.is_approved = True
                auction_request.save()
                print(f"Approved request: {auction_request.id}")  # تأكيد الموافقة

                # Update the auction status if it exists
                if auction_request.Auction:
                    auction_request.Auction.auction_status = True
                    auction_request.Auction.save()
                    print(f"Auction {auction_request.Auction.id} activated")  # تأكيد تفعيل المزاد

        self.message_user(request, "Selected requests have been approved and corresponding auctions activated.")

    approve_requests.short_description = 'Approve selected requests and activate corresponding auctions'

admin.site.register(AuctionRequest, AuctionRequestAdmin)