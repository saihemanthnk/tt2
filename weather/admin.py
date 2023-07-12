from django.contrib import admin
from .models import WeatherForecast

# Register your models here.

class WeatherForecastAdmin(admin.ModelAdmin):
    list_display = ['latitude','longitude','detailing_type']
    readonly_fields = ['last_updated']

admin.site.register(WeatherForecast,WeatherForecastAdmin)
