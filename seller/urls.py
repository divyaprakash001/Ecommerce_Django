from django.urls import path
from . import views
from accounts import views as AccountViews

urlpatterns = [
    path('', AccountViews.sellerDashboard,name="seller"),
    path('profile', views.seller_profile,name="seller_profile"),
]
