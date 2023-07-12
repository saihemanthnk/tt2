from django import forms
from .models import WeatherForecast

class ForecastForm(forms.ModelForm):
    class Meta:
        model = WeatherForecast 
        fields = ['latitude','longitude','detailing_type']

    def __init__(self,*args,**kwargs):
        super(ForecastForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['placeholder'] = f'Enter {field}'

        
