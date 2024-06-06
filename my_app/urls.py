from django.urls import path
from .import views

urlpatterns = [
    path("",views.index,name="index"),
    path("shop/",views.shop,name="shop"),
    path("<int:id>",views.details,name="details"),
    path("addcart/<int:id>",views.add_to_cart,name="add_to_cart"),
    path("removecart/<int:id>",views.remove_from_cart,name="remove_from_cart"),
    path("cart/",views.cart,name="cart"),
    path("order_summary/",views.order_summary,name="order_summary"),
    path("order_summary_new/",views.order_summary_new,name="order_summary_new"),
    path("delivery_details/",views.delivery_details,name="delivery_details"),

    path("register_user/",views.register_user,name="register_user"),
    path("registration_confirmation/",views.registration_confirmation,name="registration_confirmation"),
    path("otp_failed/",views.otp_failed,name="otp_failed"),
    path("login_user/",views.login_user,name="login_user"),
    path("logout_user/",views.logout_user,name="logout_user"),
]