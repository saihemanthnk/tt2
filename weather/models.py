from django.db import models

# Create your models here. 


class WeatherForecast(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    detailing_type= models.CharField(max_length=55)
    forecast_data = models.TextField()
    last_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.latitude},{self.longitude}--{self.forecast_data}"


