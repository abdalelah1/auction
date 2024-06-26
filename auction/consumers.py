import json
import os 
from channels.generic.websocket import AsyncWebsocketConsumer
import django
from django.conf import settings
from asgiref.sync import sync_to_async
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_auction.settings')
django.setup()
from .models import * 
from auction.views import calc_highest_price

# Now this script or any imported module can use any part of Django it needs.

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.auction_id = self.scope['url_route']['kwargs']['auction_id'] 
        self.auction_group_name = f'auction_{self.auction_id}'

        await self.channel_layer.group_add(
            self.auction_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.auction_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        bid_amount = data['bid_amount']
        user_id = data['user_id']
        print(f"Received bid_amount: {bid_amount}, user_id: {user_id}")
        user = await sync_to_async(User.objects.get)(pk=user_id)
        customer= await sync_to_async(Customer.objects.get)(user=user)
        auction = await sync_to_async(Auction.objects.get)(pk=self.auction_id)
        bid = await sync_to_async(Bid.objects.create)(
            customer=customer,
            auction=auction,
            bid_amount=bid_amount
        )

        await self.channel_layer.group_send(
            self.auction_group_name,
            {
                'type': 'auction_bid',
                'bid_amount':bid.bid_amount,
                'user_id': user.id
            }
        )

    async def auction_bid(self, event):
        bid_amount = event['bid_amount']
        user_id = event['user_id']
        print(f"Sending bid_amount: {bid_amount}, user_id: {user_id} ,auction_id {self.auction_id}" )
        highest=await calc_highest_price(self.auction_id)

        await self.send(text_data=json.dumps({
            'bid_amount': highest,
            'user_id': user_id
        }))
