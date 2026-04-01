from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("", views.index, name="index"),
    
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("termsandconditions/", views.TermsNConditions, name="Terms"),


    path("shop/search/", views.search, name="search"),

    path("productview/<int:product_id>/", views.productView, name="ProductView"),
 
    path('cart/', views.cart, name='cart'),
    path('addtocart/<int:product_id>/', views.addtocart, name='addtocart'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),

    path("checkout/", views.checkout, name="Checkout"),
  
    path('login/', views.LoginView, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),

]