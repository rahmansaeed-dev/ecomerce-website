from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import CustomUser, Customer
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import login,logout, authenticate
from django.views import View
from .models import *
from .forms import ProfileForm 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from django.db.models import Q
from django.http import JsonResponse
import stripe
from django.conf import settings

# Register page 
def register_page(request):
    if request.method == 'POST':
        name = request.POST.get('Name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'This Name or email is already taken!')
            return HttpResponseRedirect(request.path_info)
        try:
            messages.success(request, 'Signup successfully!!!')
            CustomUser.objects.create_user(Name=name,email=email, password=password)
            return redirect('signin')
        except Exception as e:
            print(e)
            messages.error(request, 'Error creating user.')
            return HttpResponseRedirect(request.path_info)
    else:
        return render(request, 'register.html')
        
# Signin page / Login page
def signin_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successfully..')
            return redirect('index')
        else:
            messages.warning(request, 'Please enter correct information..')
            return redirect('signin')
    return render(request, 'signin.html')
    
# Logout 
@login_required(login_url='signin')
def user_logout(request):
    logout(request)
    return redirect('signin')

# Index Page 
def index_page(request):
    if request.user.is_authenticated:
        product = Product.objects.all()
    else:
        return render(request, 'signin.html')
    return render(request, 'home/index.html',context={'products':product})

# About page 
@login_required(login_url='signin')
def about_page(request):
    return render(request, 'about/about.html')

# Index_2 Page 
@login_required(login_url='signin')
def index_2_page(request):
    return render(request, 'home/index_2.html')

# 404 page 
@login_required(login_url='signin')
def NotFound(request):
    return render(request, 'about/404.html')

# Cart page 
@login_required(login_url='signin')
def cart_page(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    print(product_id)
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    print(product)
    return redirect('showcart')

# Show cart view
@login_required(login_url='signin')
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user 
        showcart = Cart.objects.filter(user=user)
        amount = 0.0
        sheping_amount = 45.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = ( p.quantity * p.product.price )
                amount += tempamount
                total_amount= amount + sheping_amount
        return render(request, 'show-cart.html', context={'showcart':showcart,'amount':amount,'total_amount':total_amount})

# Increase item view
@login_required(login_url='signin')
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(product=prod_id, user=request.user)
        c.quantity +=1
        c.save()
        totalamount = 0.0
        sheping_amount = 45
        cart_product = Cart.objects.filter(user=request.user)
        for p in cart_product:
            totalamount += ( c.quantity * p.product.price )
        data = {
            'quantity' : c.quantity,
            'price' : c.product.price,
            'amount' : c.product.price * c.quantity,
            'totalamount' : totalamount + sheping_amount,
        }
        return JsonResponse(data)

# orderplaced view 
@login_required(login_url='signin')
def order_placed(request):
    op = Orderplaced.objects.filter(user=request.user)
    print(op)
    return render(request, 'orders.html', {'op':op})

# Decrease Item view
@login_required(login_url='signin')
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user= request.user))
        c.quantity -=1
        c.save()
        amount = 0.0
        sheping_amount = 45
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = ( p.quantity * p.product.price )
            amount += tempamount
        data = {
            'quantity' : c.quantity,
            'price' : c.product.price,
            'amount' : c.product.price * c.quantity,
            'totalamount' : amount + sheping_amount,
        }
        return JsonResponse(data)  

# Remove cart view
@login_required(login_url='signin')
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.filter(Q(product=prod_id) & Q(user= request.user))
        c.delete()
        amount = 0.0
        sheping_amount = 45
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = ( p.quantity * p.product.price )
            amount += tempamount
        data = {
            'amount' : amount,
            'totalamount' : total_amount,
            }
        return JsonResponse(data)   

# Checkout page 
@login_required(login_url='signin')
def check_out_page(request):
    address = Customer.objects.filter(user=request.user)
    cart_item = Cart.objects.filter(user=request.user)
    print(address)
    print(cart_item)
    amount = 0.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = ( p.quantity * p.product.price )
            amount += tempamount
        total_amount = amount
    return render(request, 'about/checkout.html', context={'cart_item':cart_item, 'total_amount':total_amount, 'address':address})

# payment Done view
@login_required(login_url='signin')
def payment_done(request):
    try:
        user = request.user
        custid = request.GET.get('custid')
        customer = CustomUser.objects.get(id=custid)
        cart = Cart.objects.filter(user=user)
        for c in cart:
            Orderplaced(user=user,customer=customer, product=c.product,quantity=c.quantity).save()
            c.delete()
    except Exception as e:
        print(e)
    return redirect('orderplaced')

# Contact page
@login_required(login_url='signin')
def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        reg=Contact(name=name,email=email,phone=phone,
        subject=subject,message=message)
        reg.save()
        messages.success(request, 'Your contact form has save successfully..')
        return redirect('thankyou')
    else:
        return render(request, 'about/contact.html')

@login_required(login_url='signin')
def thankyou(request):
    return render(request, 'thankyou.html')

# News page
@login_required(login_url='signin')
def news_page(request):
    news = News.objects.all()
    return render(request, 'about/news.html', context={'news':news})

# Shop page
@login_required(login_url='signin')
def shop_page(request, data=None):
    item = None
    if item == None:
        item = Product.objects.all()
    elif data == "St" or data == 'Ba' or data == 'Lem':
        item = Product.objects.all().filter(cetetory=item)        
    return render(request, 'about/shop.html', context={'items':item})

# Single news page 
@login_required(login_url='signin')
def single_news(request, pk):
    new1 = News.objects.get(pk=pk)
    return render(request, 'single-news.html', context={'news1':new1})

# Single product page
@login_required(login_url='signin')
def single_product(request, pk):
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    item_already_in_cart = Cart.objects.filter(Q(product=product.id) &Q(user=request.user)).exists()
    return render(request, 'shop/single-product.html',context={'product':product,'item_already_in_cart':item_already_in_cart})

# Profile page view
@login_required(login_url='signin')
def profile_form(request):
    if request.method == 'POST':
        profiles = ProfileForm(request.POST)
        if profiles.is_valid():
            user = request.user
            name = profiles.cleaned_data['Name']
            city = profiles.cleaned_data['city']
            state = profiles.cleaned_data['state']
            zipcode = profiles.cleaned_data['zipcode']
            locality = profiles.cleaned_data['locality']
            if Customer.objects.filter(Name=name).exists():
                messages.warning(request, 'This Name or email is already taken!')
                return HttpResponseRedirect(request.path_info)
            reg = Customer.objects.create(user=user,Name=name,city=city,state=state,zipcode=zipcode,locality=locality)
            messages.success(request, 'profile created succesfully..')
            reg.save()
            return redirect('/address')
        return render(request, 'profile.html', context={'profiles': profiles, 'active': 'btn btn-secondary'})
    else:
        profiles = ProfileForm()
    context = {'profiles': profiles}
    return render(request, 'profile.html', context)

# address view
@login_required(login_url='signin')
def address_page(request):
    address = Customer.objects.filter(user = request.user)
    context = {'address':address,'active':'btn btn-primary'}
    return render(request, 'address.html', context)

############## STRIPE PAYMENT SECTION ############ 
             
# STRIPE VIEW
@login_required(login_url='signin')
def stripe_payment(request):
    carts = Cart.objects.filter(user=request.user)
    total_price = 0
    for cart_item in carts:
        item_price = cart_item.product.price * cart_item.quantity
        total_price += item_price
    return render(request, 'stripe.html', context={'carts': carts, 'total_price': total_price})

# Checkout session view 
stripe.api_key = settings.STRIPE_SECRET_KEY
@login_required(login_url='signin')
def checkout_session(request):
    carts = Cart.objects.filter(user=request.user)
    price = 0
    total_quantity = 0
    for cart in carts:
        total_quantity += cart.quantity
        price += cart.product.price 
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Invoice',
                    },
                    'unit_amount': int(price) * 100,
                },
                'quantity': total_quantity,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('success')) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('cancel')),
    )
    return redirect(checkout_session.url, code=303)

# Success payment 
@login_required(login_url='signin')
def success(request):
    return render(request, 'success.html')

# Cancel payment
@login_required(login_url='signin')
def cancel(request):
    return render(request, 'cancel.html')
