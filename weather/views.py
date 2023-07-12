from django.shortcuts import render
import requests 
from django.conf import settings
from django.http import JsonResponse
from .models import WeatherForecast 
from django.views.decorators.csrf import csrf_exempt 
from .forms import ForecastForm
from  django.utils import timezone
import datetime
import json

# Create your views here. 


def get_curr_usefuldata1(weather):
            
            
            forecast_data = json.loads(weather.forecast_data.replace("'",'"'))
            
            temp = round(forecast_data['main']['temp'] - 273.15,1)
            feels_like = round(forecast_data['main']['feels_like']-273.15,2)
            humidity = forecast_data['main']['humidity']
            description = forecast_data['weather'][0]['description']
            icon = forecast_data['weather'][0]['icon'] 
            # lat = weather.forecast_data['coord']['lat']
            # lon = weather.forecast_data['coord']['lon']
            pressure = forecast_data['main']['pressure']
            speed = forecast_data['wind']['speed'] 
           
            data = {'temp':temp,'description':description,'icon':icon,'feels_like':feels_like,'humidity':humidity,'speed':speed,'pressure':pressure}
            return data







def get_curr_usefuldata(weather):
            
            
            temp = round(weather.forecast_data['main']['temp'] - 273.15,1)
            feels_like = round(weather.forecast_data['main']['feels_like']-273.15,2)
            humidity = weather.forecast_data['main']['humidity']
            description = weather.forecast_data['weather'][0]['description']
            icon = weather.forecast_data['weather'][0]['icon'] 
            # lat = weather.forecast_data['coord']['lat']
            # lon = weather.forecast_data['coord']['lon']
            # min_temp = weather.forecast_data['main']['temp_min'] - 273.15 
            # max_temp = weather.forecast_data['main']['temp_max'] - 273.15 
            pressure = weather.forecast_data['main']['pressure']
            speed = weather.forecast_data['wind']['speed'] 
           
            data = {'temp':temp,'description':description,'icon':icon,'feels_like':feels_like,'pressure':pressure,'speed':speed,'humidity':humidity}
            return data


def get_3hrs_usefuldata1(weather):
     
            context1 = []

            forecast_data = json.loads(weather.forecast_data.replace("'",'"'))
     
            for data in forecast_data['list']:
                temp = round(data['main']['temp'] - 273.15,1)
                feels_like = round(data['main']['feels_like']-273.15,2)
                humidity = data['main']['humidity']
                description = data['weather'][0]['description']
                icon = data['weather'][0]['icon'] 
                min_temp = round(data['main']['temp_min'] - 273.15,2)
                max_temp = round(data['main']['temp_max'] - 273.15,2)
                pressure = data['main']['pressure']
                speed = data['wind']['speed']
                day = datetime.datetime.fromtimestamp(data['dt']).strftime('%A')
                time = data['dt_txt']
                context1.append({'temp':temp,'feels_like':feels_like,"description":description,'humidity':humidity,'icon':icon,'min_temp':min_temp,'max_temp':max_temp,'day':day,'time':time})
            return context1 
        
        

def get_3hrs_usefuldata(weather):
     
            context1 = []
     
            for data in weather.forecast_data['list']:
                temp = round(data['main']['temp'] - 273.15,1)
                feels_like = round(data['main']['feels_like']-273.15,2)
                humidity = data['main']['humidity']
                description = data['weather'][0]['description']
                icon = data['weather'][0]['icon'] 
                min_temp = round(data['main']['temp_min'] - 273.15 ,2)
                max_temp = round(data['main']['temp_max'] - 273.15,2)
                pressure = data['main']['pressure']
                speed = data['wind']['speed']
                time = data['dt_txt']
                day = datetime.datetime.fromtimestamp(data['dt']).strftime('%A')
                context1.append({'temp':temp,'feels_like':feels_like,"description":description,'humidity':humidity,'icon':icon,'min_temp':min_temp,'max_temp':max_temp,'day':day,'time':time})
            return context1 
     



          
          



def get_3hours_weather(lat,lon,api_key):
     url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}'
     response = requests.get(url)
     if response.status_code == 200:
        return response.json()
     else:
        return None
     
     
     


def get_current_weather(lat,lon,api_key):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_minutely_forecast(lat, lon, api_key):
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,hourly,daily&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('minutely')
        
    else:
         return None 

def get_hourly_forecast(lat, lon, api_key):
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,daily&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('hourly')
    else:
         return None 


def get_daily_forecast(lat, lon, api_key):
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('daily')
    else:
         return None 
    
  



@csrf_exempt

def weather_forecast(request):
    if request.method == "POST":

        form = ForecastForm(request.POST) 
    
        if form.is_valid():
            latitude = form.cleaned_data.get("latitude") 
            longitude = form.cleaned_data.get("longitude")
            detailing_type = form.cleaned_data.get("detailing_type")

         

             # check if forecast exists in db 

            try:

                weather = WeatherForecast.objects.get(latitude=latitude,longitude=longitude,detailing_type=detailing_type)
                

                 # check if the stored data is still relevant 

                delta = timezone.now() - weather.last_updated 

                
               
                if int(delta.total_seconds()/60) > settings.TIME_SENSITIVITY:  # no longer relevant 
                    # then fetch data from OpenWeather Api 
                    api_key = 'e1c965c359dafa95a21de1b1ffe4b766'
                    forecast_data = None
                    if detailing_type == 'minutely':
                        forecast_data = get_minutely_forecast(latitude, longitude, api_key)
            
                    elif detailing_type == 'hourly':
                        forecast_data = get_hourly_forecast(latitude, longitude, api_key)

                    elif detailing_type == 'daily':
                        forecast_data = get_daily_forecast(latitude, longitude, api_key)
            
                    elif detailing_type == 'current':
                        forecast_data = get_current_weather(latitude,longitude,api_key)

                    elif detailing_type == '3hours':
                        forecast_data = get_3hours_weather(latitude,longitude,api_key)
                    
                

                    # update local db
                    if forecast_data is not None:
                        weather.forecast_data = forecast_data 
                        weather.save(update_fields=['forecast_data'])

                         # current weather 
                        context = None
                        context2 = None

                        if detailing_type == 'current':
                            context = get_curr_usefuldata(weather)
                        elif detailing_type == '3hours':
                            context2 = get_3hrs_usefuldata(weather)

                        return render(request,'weather/data.html',{"context1":context,'context2':context2,'text':'Not Relavent'})

                    else:
                         return JsonResponse({"error":"Failed to fetch"})
                    
                    
                     
                else: # relevant
                    context = None
                    context2 = None

                    
                    if detailing_type == 'current':
                        context = get_curr_usefuldata1(weather)


                    elif detailing_type == '3hours':
                          context2 = get_3hrs_usefuldata1(weather)


                    return render(request,'weather/data.html',{"context1":context,'context2':context2,'text':'Relavent'})
                    

            
            except WeatherForecast.DoesNotExist:

                api_key = 'e1c965c359dafa95a21de1b1ffe4b766'
                forecast_data = None 
                 
                
                if detailing_type == 'minutely':
                        forecast_data = get_minutely_forecast(latitude, longitude, api_key)
            
                elif detailing_type == 'hourly':
                        forecast_data = get_hourly_forecast(latitude, longitude, api_key)

                elif detailing_type == 'daily':
                        forecast_data = get_daily_forecast(latitude, longitude, api_key)
            
                elif detailing_type == 'current':
                        forecast_data = get_current_weather(latitude,longitude,api_key)
                
                elif detailing_type == '3hours':
                        forecast_data = get_3hours_weather(latitude,longitude,api_key)


                # save to our local db
                if forecast_data is not None:
                    weather1 = WeatherForecast(latitude=latitude,longitude=longitude,detailing_type=detailing_type,forecast_data=forecast_data)
                    weather1.save()

                    context = None
                    context2 = None

                    # current weather 
                    if detailing_type == 'current':
                        context = get_curr_usefuldata(weather1)
                    elif detailing_type == '3hours':
                         context2 = get_3hrs_usefuldata(weather1)


                    return render(request,'weather/data.html',{"context1":context,'context2':context2,'text':'Hello'})

                else:
                    return JsonResponse({"error":"Failed to fetch"})


        else:
            return render(request,'weather/details.html',{'form':form})
        
    else:
        form = ForecastForm() 
        return render(request,'weather/details.html',{'form':form})


                  

    

        





