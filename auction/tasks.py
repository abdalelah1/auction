from celery import shared_task
from .views import *

@shared_task
def end_auction_task(auction_id):
    from .models import Auction
    auction = Auction.objects.get(id=auction_id)
    save_winner_for_auction(auction_id)
    task = PeriodicTask.objects.get(name=f'end-auction-task-{auction_id}')
    task.enabled = False
    task.save()
    auction.auction_status = False
    auction.save()
    print(f"Auction {auction_id} has ended.")
