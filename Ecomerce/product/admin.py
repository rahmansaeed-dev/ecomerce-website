from django.contrib import admin
from .models import Cart,CustomUser,Product,Orderplaced, News, ModelAdressModal, Customer, Contact


@admin.register(Orderplaced)
class OrderPlacedAdmin(admin.ModelAdmin):
        list_display = ['id','customer','product','quantity','order_date','status']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
        list_display = ['id','user','product','quantity']

@admin.register(Customer)
class CartAdmin(admin.ModelAdmin):
        list_display = ['id','user','Name','locality','city','zipcode','state']

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
        list_display = ['id','email','locality','city','zipcode','state']

@admin.register(Product)
class CustomUserAdmin(admin.ModelAdmin):
        list_display = ['id','name','title','price','is_sale','sale_price','cetegory','image']

@admin.register(News)
class NewsModelAdmin(admin.ModelAdmin):
        list_display = ['id','title','user','date','description','image']

@admin.register(ModelAdressModal)
class AddressModalAdmin(admin.ModelAdmin):
        list_display = ['id','Name','email','state','zipcode','locality']


@admin.register(Contact)
class ContactModalAdmin(admin.ModelAdmin):
        list_display = ['id','name','email','phone','subject','message']
