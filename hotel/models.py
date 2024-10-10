from django.db import models
from django.conf import settings
from django.urls import reverse_lazy

# Create your models here.

class Room(models.Model):
    ROOM_CATEGORIES=(
        ('AC', 'Air-Conditioned'),
        ('NAC', 'Non Air-Conditioned'),
        ('DEL', 'Deluxe'),
        ('KIN', 'King'),
        ('QUE', 'Queen'),
    )
    number = models.IntegerField()
    category = models.CharField(max_length=3, choices=ROOM_CATEGORIES)
    beds = models.IntegerField()
    capacity = models.IntegerField()
    room_charge = models.IntegerField()

    def __str__(self):
        return f'{self.number}. {self.category} with {self.beds} beds for {self.capacity} person(s) for {self.room_charge} Shillings'

class Meal(models.Model):
    MEAL_CATEGORIES=(
        ('BRE', 'Breakfast'),
        ('LUN', 'Lunch'),
        ('SUP', 'Supper'), 
    )
    meal_type = models.CharField(max_length=3, choices=MEAL_CATEGORIES)
    meal_name = models.CharField(max_length=20)  

    def __str__(self):
        return f'{self.meal_type}: {self.meal_name}'

class Service(models.Model): 
    SERVICE_CATEGORIES=(
        ('HSKP', 'House Keeping'),
        ('LAUN', 'Laundry'), 
    )
    service_type = models.CharField(max_length=4, choices=SERVICE_CATEGORIES)
    service_name = models.CharField(max_length=20) 

    def __str__(self):
        return f'{self.service_type}: {self.service_name}'

########################################################################################

class MealCharge(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    meal_charge = models.CharField(max_length=30)
 
    def __str__(self):
        return f'{self.meal.meal_name} for {self.meal_charge}'

class ServiceCharge(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    service_charge = models.CharField(max_length=30)
 
    def __str__(self):
        return f'{self.service.service_name} for {self.service_charge}'
   

########################################################################################

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def __str__(self):
        return f'{self.user} has booked room {self.room}; From {self.check_in} To {self.check_out}.' 

    def get_room_category(self):
        room_categories = dict(self.room.ROOM_CATEGORIES)
        room_category = room_categories.get(self.room.category)
        return room_category
    
    def get_cancel_booking_url(self):
        return reverse_lazy('CancelBookingView', args={self.pk, })

class MealSelection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    mealcharge = models.ForeignKey(MealCharge, on_delete=models.CASCADE) 
    meal_date = models.DateField()  

    def __str__(self):
        return f'{self.user} has selected {self.meal}; On {self.meal_date}.'  
    
    def get_meal_category(self):
        meal_categories = dict(self.meal.MEAL_CATEGORIES)
        meal_category = meal_categories.get(self.meal.meal_type)
        return meal_category

class ServiceSelection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    servicecharge = models.ForeignKey(ServiceCharge, on_delete=models.CASCADE)
    service_date = models.DateField() 

    def __str__(self):
        return f'{self.user} has selected {self.service}; On {self.service_date}.'  

    def get_service_category(self):
        service_categories = dict(self.service.SERVICE_CATEGORIES)
        service_category = service_categories.get(self.service.service_type)
        return service_category

########################################################################################

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.SET_NULL, null=True, blank=True, default='')
    mealcharge = models.ForeignKey(MealCharge, on_delete=models.SET_NULL, null=True, blank=True, default='')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, default='')
    servicecharge = models.ForeignKey(ServiceCharge, on_delete=models.SET_NULL, null=True, blank=True, default='')
    payment_date = models.DateField() 

    def __str__(self):
        return f'Payment By: {self.user} on: {self.payment_date}.'  

    # def get_service_category(self):
    #     service_categories = dict(self.service.SERVICE_CATEGORIES)
    #     service_category = service_categories.get(self.service.service_type)
    #     return service_category
  
