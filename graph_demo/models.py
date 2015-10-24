__author__ = 'indrajit'

from django.db import models
from django.contrib.auth.models import User

from django_facebook_graph.signals import new_relation_event

class Product(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class Purchases(models.Model):
    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        from views import get_user_model
        user_model = get_user_model()
        social_user = user_model.objects.get(user=self.user)
        super(Purchases, self).save(force_insert, force_update, using, update_fields)
        new_relation_event.send(sender=None, social_user=social_user,
                                model_instance=self.product, relation='purchases')