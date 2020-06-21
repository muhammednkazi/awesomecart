from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"),#homepage
    path('aboutus/', views.aboutus,name="aboutus"),
    path('contactus/', views.contactus,name="contactus"),
    path('checkout/', views.checkout,name="checkout"),
    path('productview/<int:myid>', views.productview,name="productview"),
    path('search/', views.search,name="search"),
    path('track/', views.track,name="track")
]