from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from .models import Station, Device, Turnstile
from .forms import StationForm
from datetime import datetime, timedelta
import json

# Create your views here.
def index(request):
    start_date = '2018-01-01 00:00:00'
    end_date = '2018-02-01 00:00:00'
    start_dt = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    start_ts = int((start_dt - datetime(1970, 1, 1)) / timedelta(seconds=1))
    end_ts = int((end_dt - datetime(1970, 1, 1)) / timedelta(seconds=1))

    station_data = Turnstile.objects.using('turnstile') \
        .filter(timestamp__gte=start_ts, timestamp__lte=end_ts) \
        .values('device__station__name') \
        .annotate(entry=Sum('entry'), exit=Sum('exit')) \
        .exclude(device__station__name__isnull=True)
    #    .order_by('-entry')
    formatted_data = json.dumps([dict(item) for item in list(station_data)])
    #if request.method == 'POST':
    #    form = StationForm(request.POST)
        

    #form = StationForm()
    
    context = {'station_data': station_data, 'formatted_data': formatted_data}
    return render(request, 'turnstile/index.html', context)
    #return JsonResponse({'data': list(data)})