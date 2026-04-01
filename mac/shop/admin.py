from django.contrib import admin

# Register your models here.
from .models import Product

class Showdata(admin.ModelAdmin):
    list=("product_id","product_name","category","subcategory","price","desc","pub_date","image")
admin.site.register(Product,Showdata)