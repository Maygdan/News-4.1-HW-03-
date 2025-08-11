from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post_Category
from .basic import new_post





@receiver(m2m_changed, sender=Post_Category)
def notifly(sender,instance,**kwargs):
    if kwargs['action']=='post_add':
        new_post(instance)
