__author__ = 'indrajit'

import importlib

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django_facebook_graph.models import FacebookGraphUser, BaseMapper

from models import *

def get_user_model():
    path = settings.FACEBOOK_USER_MODEL
    module_name, class_name = path.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), class_name)

@login_required
def home(request):
    user = request.user
    user_model = get_user_model()
    social_user = user_model.objects.get(user=user)
    facebook_node = FacebookGraphUser.get(social_user)
    friends = facebook_node.friends()
    friends_of_friends = facebook_node.friends_of_friends()
    products = Product.objects.all()
    purchases = []
    friends_purchased = []
    for product in products:
        prod_node = BaseMapper.get_or_create(product)
        relation = facebook_node.has_relation(prod_node, 'purchases')
        if relation is not None:
            purchases.append(product.name)
        f = facebook_node.get_friends_with_relation(product, 'purchases')
        if f:
            friends_purchased.append(product.name)
    products = [x.name for x in products]
    friends_purchased = list(set(friends_purchased))
    purchases = list(set(purchases))

    context = {'friends': friends, 'fof': friends_of_friends, 'purchases': purchases,
               'friend_purchases': friends_purchased, 'products': products, 'user': user}

    return render(request, 'home.html', context)