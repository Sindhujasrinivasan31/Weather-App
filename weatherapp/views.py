from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'chennai'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=8a28ec557d8e0ae5f9110d17a7d30eae'
    PARAMS = { 'units' : 'metric' }
    API_KEY='AIzaSyAG41C498P_BgKP7xI8gHUQWRptNTHIJd0'
    SEARCH_ENGINE_ID='d27f0459332264593'
    query = city + "1920x1080"
    page= 1
    start= (page-1)*10+1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"
    data = requests.get(city_url).json()
    count = 1
    search_items = data.get("items")
    image_url=[]
    print("search_items",search_items)
    if search_items:
        print("image",image_url)
        image_url = search_items[1]['link']
        
        
    else:
        print('error')
    exception_occurred = False
    
    try:
        response = requests.get(url, params=PARAMS)
        data = response.json()
      
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()
    
    except KeyError:
        exception_occurred = True
        messages.error(request, 'Entered data is not available to API')
        day = datetime.date.today()
        # Optionally set default values in case of an exception
        description = icon = temp = None

    return render(request, 'weather.html', {
        'description': description,
        'icon': icon,
        'temp': temp,
        'day': day,
        'city': city,
        'exception_occurred': exception_occurred,
        'image_url':image_url,
        'search_items':search_items,
    })
