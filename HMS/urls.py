"""HMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from hotel import views, AccountViews

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',include('hotel.urls')),
    path('accounts/', include('allauth.urls')), 
    path('home', views.HomeView, name='HomeView'),

    path('', AccountViews.MainView, name='MainView'),
    path('accounts/profile/', AccountViews.ProfileView, name='ProfileView'),

    path('room_list/', views.RoomListView, name='RoomListView'),
    path('booking_list/', views.BookingListView.as_view(), name='BookingListView'),
    path('meal_list/', views.MealListView, name='MealListView'),
    path('meal_selection_list/', views.MealSelectionList.as_view(), name='MealSelectionList'),
    path('service_list/', views.ServiceListView, name='ServiceListView'),
    path('service_selection_list/', views.ServiceSelectionList.as_view(), name='ServiceSelectionList'), 


    path('room/<category>', views.RoomDetailView.as_view(), name='RoomDetailView'),
    path('meal/<meal_type>', views.MealDetailView.as_view(), name='MealDetailView'),
    path('service/<service_type>', views.ServiceDetailView.as_view(), name='ServiceDetailView'),

    path('booking/cancel/<pk>', views.CancelBookingView.as_view(), name='CancelBookingView'),

    path('payment_add/', views.PaymentCreateView.as_view(), name='PaymentCreateView'),  
    path('payment_list', views.PaymentListView.as_view(), name='PaymentListView'),    

    path('ajax/load-mealcharges/', views.load_mealcharges, name='ajax_load_mealcharges'),
    path('ajax/load-servicecharges/', views.load_servicecharges, name='ajax_load_servicecharges'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
