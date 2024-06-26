from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# تحديد إعدادات Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_auction.settings')

app = Celery('online_auction')

# قراءة الإعدادات من ملف settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# اكتشاف المهام تلقائيًا من جميع التطبيقات المثبتة
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
app.autodiscover_tasks(['auction'])