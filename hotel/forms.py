from django import forms

from .models import MealSelection, MealCharge, ServiceSelection, ServiceCharge, Payment

class AvailabilityForm(forms.Form):  
    check_in = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])
    check_out = forms.DateTimeField(required=True, input_formats=["%Y-%m-%dT%H:%M", ])


class MealSelectionForm(forms.ModelForm): 
    class Meta:
        model = MealSelection
        fields = ('meal','mealcharge', 'meal_date')
    meal_date = forms.DateField() 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mealcharge'].queryset = MealCharge.objects.none()
 
        if 'meal' in self.data:
            try:
                meal_id = int(self.data.get('meal'))
                self.fields['mealcharge'].queryset = MealCharge.objects.filter(meal_id=meal_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['mealcharge'].queryset = self.instance.meal.mealcharge_set

class ServiceSelectionForm(forms.ModelForm): 
    class Meta:
        model = ServiceSelection
        fields = ('service','servicecharge', 'service_date')
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servicecharge'].queryset = ServiceCharge.objects.none()
 
        if 'service' in self.data:
            try:
                service_id = int(self.data.get('service'))
                self.fields['servicecharge'].queryset = ServiceCharge.objects.filter(service_id=service_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['servicecharge'].queryset = self.instance.service.servicecharge_set

class PaymentForm(forms.ModelForm): 
    class Meta:
        model = Payment
        fields = ('meal','mealcharge', 'service', 'servicecharge', 'payment_date') 
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mealcharge'].queryset = MealCharge.objects.none()
 
        if 'meal' in self.data:
            try:
                meal_id = int(self.data.get('meal'))
                self.fields['mealcharge'].queryset = MealCharge.objects.filter(meal_id=meal_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['mealcharge'].queryset = self.instance.meal.mealcharge_set

