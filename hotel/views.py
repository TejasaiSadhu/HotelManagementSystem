from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, FormView, View, DeleteView, CreateView
from django.urls import reverse, reverse_lazy
from .models import Room, Booking, Meal, MealSelection, Service, ServiceSelection, MealCharge, ServiceCharge, Payment
from .forms import AvailabilityForm, MealSelectionForm, ServiceSelectionForm, PaymentForm
from hotel.booking_functions.availability import check_availability

# Create your views here.

def HomeView(request):
    return render(request, 'home_view.html')

def RoomListView(request):
    room = Room.objects.all()[0]
    room_categories = dict(room.ROOM_CATEGORIES)

    room_values = room_categories.values()
    room_list = []

    for room_category in room_categories:
        room = room_categories.get(room_category)
        room_url = reverse('RoomDetailView', kwargs={'category':room_category})
    
        room_list.append((room, room_url)) 
    context = {
        "room_list": room_list,
        'self' : request.user
    }
    return render(request, 'room_list_view.html', context)

class BookingListView(ListView):
    model = Booking
    template_name="booking_list_view.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list

def MealListView(request):
    meal = Meal.objects.all()[0]
    meal_categories = dict(meal.MEAL_CATEGORIES)

    meal_values = meal_categories.values()
    meal_list = []

    for meal_category in meal_categories:
        meal = meal_categories.get(meal_category)
        meal_url = reverse('MealDetailView', kwargs={'meal_type':meal_category})
    
        meal_list.append((meal, meal_url)) 
    context = {
        "meal_list": meal_list,
        'self' : request.user
    }
    return render(request, 'meal_list_view.html', context)

class MealSelectionList(ListView):
    model = MealSelection
    template_name="mealselection_list_view.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            mealselection_list = MealSelection.objects.all()
            return mealselection_list
        else:
            mealselection_list = MealSelection.objects.filter(user=self.request.user)
            return mealselection_list

def ServiceListView(request):
    service = Service.objects.all()[0]
    service_categories = dict(service.SERVICE_CATEGORIES)

    service_values = service_categories.values()
    service_list = []

    for service_category in service_categories:
        service = service_categories.get(service_category)
        service_url = reverse('ServiceDetailView', kwargs={'service_type':service_category})
    
        service_list.append((service, service_url)) 
    context = {
        "service_list": service_list,
        'self' : request.user
    }
    return render(request, 'service_list_view.html', context)

class ServiceSelectionList(ListView):
    model = ServiceSelection
    template_name="serviceselection_list_view.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            serviceselection_list = ServiceSelection.objects.all()
            return serviceselection_list
        else:
            serviceselection_list = ServiceSelection.objects.filter(user=self.request.user)
            return serviceselection_list

##########################################

class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        form = AvailabilityForm()
        room_list = Room.objects.filter(category=category)
        
        if len(room_list)>0:
            room = room_list[0]
            room_category = dict(room.ROOM_CATEGORIES).get(room.category, None)
            context = {
                'room_category' : room_category,
                'form' : form,
                'self': request.user
            }
            return render(request, 'room_detail_view.html', context)
        else:
            return HttpResponse('No Rooms Of This Category.')

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        room_list = Room.objects.filter(category=category)
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        available_rooms=[]
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

            if len(available_rooms)>0: 
                room = available_rooms[0]
                booking = Booking.objects.create(
                    user = self.request.user,
                    room = room,
                    check_in = data['check_in'],
                    check_out = data['check_out']
                )
                booking.save()
                # return HttpResponse(booking)
                return HttpResponseRedirect(reverse("BookingListView"))
            else:
                return HttpResponse('Room Is Not Available From Selected Date. Try Another One.')

class MealDetailView(View):
    def get(self, request, *args, **kwargs):
        # meal_type = self.kwargs.get('meal_type',None)           ==same
        # meal_list = Meal.objects.filter(meal_type=meal_type)    ==same
        
        meal_type = self.kwargs.get('meal_type',None)
        meal_list = Meal.objects.filter(meal_type=meal_type)
        mealselectionform = MealSelectionForm()
         
        if len(meal_list)>0:
            meal = meal_list[0]
            meals = Meal.objects.filter(meal_type=meal_type)
            meal_category = dict(meal.MEAL_CATEGORIES).get(meal.meal_type, None)
            context = {
                'meal_category' : meal_category,
                'meals' : meals,
                'self' : request.user,
                'mealselectionform' : mealselectionform,
            }
            return render(request, 'meal_detail_view.html', context)
        else:
            return HttpResponse('No Meals Of This Category.')

    def post(self, request, *args, **kwargs): 
        meal_date=request.POST.get("meal_date")
        meal_id=request.POST.get("meal")
        mealcharge_id=request.POST.get("mealcharge") 
        user = self.request.user.id

        mealselection=MealSelection(meal_date=meal_date,meal_id=meal_id,mealcharge_id=mealcharge_id,user_id=user)
        mealselection.save()
        # return HttpResponse(mealselection)
        return HttpResponseRedirect(reverse("MealSelectionList"))

def load_mealcharges(request):
    meal_id = request.GET.get('meal')
    mealcharges = MealCharge.objects.filter(meal_id=meal_id)
    return render(request, 'mealcharge_dropdown_list_options.html', {'mealcharges': mealcharges})

class ServiceDetailView(View):
    def get(self, request, *args, **kwargs):
        service_type = self.kwargs.get('service_type',None)
        service_list = Service.objects.filter(service_type=service_type)
        serviceselectionform = ServiceSelectionForm()
        
        if len(service_list)>0:
            service = service_list[0]
            services = Service.objects.filter(service_type=service_type)
            service_category = dict(service.SERVICE_CATEGORIES).get(service.service_type, None)
            context = {
                'service_category' : service_category,
                'services' : services,
                'self' : request.user,
                'serviceselectionform' : serviceselectionform,
            }
            return render(request, 'service_detail_view.html', context)
        else:
            return HttpResponse('No Services Of This Category')

    def post(self, request, *args, **kwargs):
        service_date=request.POST.get("service_date")
        service_id=request.POST.get("service")
        servicecharge_id=request.POST.get("servicecharge") 
        user = self.request.user.id

        serviceselection=ServiceSelection(service_date=service_date,service_id=service_id,servicecharge_id=servicecharge_id,user_id=user)
        serviceselection.save()
        # return HttpResponse(serviceselection)
        return HttpResponseRedirect(reverse("ServiceSelectionList"))

def load_servicecharges(request):
    service_id = request.GET.get('service')
    servicecharges = ServiceCharge.objects.filter(service_id=service_id)
    return render(request, 'servicecharge_dropdown_list_options.html', {'servicecharges': servicecharges})


##########################################

class PaymentCreateView(View):  
    def get(self, request, *args, **kwargs):  
        paymentform = PaymentForm()
          
        context = {
            'self' : request.user,
            'paymentform' : paymentform, 
        }
        return render(request, 'payment_view.html', context)
    
    def post(self, request, *args, **kwargs): 
        payment_date=request.POST.get("payment_date")
        meal_id=request.POST.get("meal")
        mealcharge_id=request.POST.get("mealcharge") 
        service_id=request.POST.get("service")
        servicecharge_id=request.POST.get("servicecharge") 
        user = self.request.user.id

        payment=Payment(payment_date=payment_date,meal_id=meal_id,mealcharge_id=mealcharge_id,service_id=service_id,servicecharge_id=servicecharge_id,user_id=user)
        payment.save()
        # return HttpResponse(payment)
        return HttpResponseRedirect(reverse("PaymentListView"))

class PaymentListView(ListView):
    # model = Payment
    # context_object_name = 'payments'
    # template_name = 'payment_list.html'

    model = Payment
    template_name="payment_list.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            payment_list = Payment.objects.all()
            return payment_list
        else:
            payment_list = Payment.objects.filter(user=self.request.user)
            return payment_list
 
##########################################

class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('BookingListView')
