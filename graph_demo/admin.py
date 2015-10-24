__author__ = 'indrajit'

from django.contrib import admin

from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_filter = ['name']


class PurchasesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(Purchases, PurchasesAdmin)
