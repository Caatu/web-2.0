from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
import web.models as models

@login_required
def home(request):
    param = {
        'units': models.Unit.objects.filter(user=request.user)
    }
    return render(request, 'home.html', param)

@login_required
def local(request, pk):
    unidade = get_object_or_404(models.Unit, pk=pk)
    if unidade.user != request.user:
        return HttpResponseForbidden()
    param = {
        'unit': unidade,
        'locals': models.Local.objects.filter(unit=pk)
    }
    return render(request, 'locals.html', param)

@login_required
def sensors(request, unidade_pk ,local_pk):
    unidade = get_object_or_404(models.Unit, pk=unidade_pk)
    local = get_object_or_404(models.Local, pk=local_pk)
    if unidade.user != request.user:
        return HttpResponseForbidden()
    collectors = models.Colector.objects.filter(local=local)
    sensors_list = []
    for collector in collectors:
        sensors = models.Sensor.objects.filter(colector=collector)
        sensors_list.extend(sensors)
    param = {
        'unit': unidade,
        'local': local,
        'colectors': collectors,
        'sensors': sensors_list,
    }
    return render(request, 'sensors.html', param)