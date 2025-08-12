from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from store.models import Customer, Product
from django.core.cache import cache
from django.db import transaction
from typing import Optional


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender: type, **kwargs: any) -> None:
    if kwargs["created"]:
        Customer.objects.create(user=kwargs["instance"])


def _bump_recs_version():
    try:
        cache.incr("recs_version")
    except ValueError:
        cache.set("recs_version", 2)


@receiver(post_save, sender=Product)
def product_saved_invalidate_recs(
    sender: type,
    instance: Product,
    created: bool,
    update_fields: Optional[frozenset[str]] = None,
    **kwargs: any
):
    relevant = {"title", "description"}
    if created or update_fields is None or (relevant & set(update_fields)):
        transaction.on_commit(_bump_recs_version)


@receiver(post_delete, sender=Product)
def product_deleted_invalidate_recs(sender: type, instance: Product, **kwargs: any):
    transaction.on_commit(_bump_recs_version)
