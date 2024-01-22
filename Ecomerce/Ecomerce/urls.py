from django.contrib import admin
from django.urls import path
from product import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from product.forms import PasswordChange, PasswordResetFormView, MySetPasswordForm
# from product.views import charge
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='index'),
    path('about/', views.about_page, name='about'),
    path('index2/', views.index_2_page, name='index2'),
    path('notfount/', views.NotFound, name='notfound'),
    path('cart/', views.cart_page, name='cart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('showcart/', views.show_cart, name='showcart'),
    path('checkout/', views.check_out_page, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    # path('placeorder/', views.orderplaced, name='orderplaced'),
    path('contact/', views.contact_page, name='contact'),
    # path('news/<int:pk>', views.news_page, name='news'),
    path('news/', views.news_page, name='news'),
    path('shop/', views.shop_page, name='shop'),
    path('shop/<slug:data>', views.shop_page, name='shopnow'),
    path('singlenews/<int:pk>/', views.single_news, name='singlenews'),
    path('singleproduct/<int:pk>/',views.single_product, name='singleproduct'),
    path('register/', views.register_page, name='register'),
    path('signin/', views.signin_page, name='signin'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_form,name='profile'),
    path('address/', views.address_page,name='address'),
    path('orderplaced/', views.order_placed,name='orderplaced'),
    path('stripe/', views.stripe_payment,name='stripe'),
    # path('charge/', charge, name='charge'),
    path('checkoutsession/', views.checkout_session,name='checkoutsession'),
    path('success/', views.success,name='success'),
    path('cancel/', views.cancel,name='cancel'),
    path('thankyou/', views.thankyou,name='thankyou'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='passwordchange.html',form_class=PasswordChange, success_url='/passwordchangedone/'),name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='passchangedone.html'), name='passwordchangedone'),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='password_reset.html', form_class=PasswordResetFormView), name='passwordreset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-conferm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    