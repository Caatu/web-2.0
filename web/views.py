import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core import serializers
from django.core.serializers.json import Serializer
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

import web.models as models


class CustomSerializer(Serializer):
    def get_dump_object(self, obj):
        return self._current


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
def sensors(request, unidade_pk, local_pk):
    unidade = get_object_or_404(models.Unit, pk=unidade_pk)
    local = get_object_or_404(models.Local, pk=local_pk)
    if unidade.user != request.user:
        return HttpResponseForbidden()
    collectors = models.Colector.objects.filter(local=local)
    sensors_list = []
    for index, collector in enumerate(collectors):
        sensors = models.Sensor.objects.filter(colector=collector)
        sensors_list.extend(sensors)
        setattr(collector, 'quantity', len(collector.sensors.all()))
    param = {
        'unit': unidade,
        'local': local,
        'colectors': collectors,
        'sensors': sensors_list,
    }
    return render(request, 'sensors.html', param)


@login_required
def measurements_sensor_ajax(request,sensor_pk):
    """
        Eu sei que esta uma porra.. mas funciona.
    """
    measurements = models.SensorMeasure.objects.filter(sensor=sensor_pk)
    data = json.loads(
        serializers.serialize(
            'json',
            measurements,
            fields=('unit_of_measurement',
                    'measurement_value', 'created_at')
        )
    )

    return_data = []

    for d in data:
        return_data.append(d['fields'])

    return JsonResponse(
        return_data,
        safe=False
    )


@login_required
def measurements_sensor(request, unidade_pk, local_pk, sensor_pk):
    unidade = get_object_or_404(models.Unit, pk=unidade_pk)
    local = get_object_or_404(models.Local, pk=local_pk)
    if unidade.user != request.user:
        return HttpResponseForbidden()
    collectors = models.Colector.objects.filter(local=local)
    sensors_list = []
    for index, collector in enumerate(collectors):
        sensors = models.Sensor.objects.filter(colector=collector)
        sensors_list.extend(sensors)
        setattr(collector, 'quantity', len(collector.sensors.all()))
    param = {
        'unit': unidade,
        'local': local,
    }
    return render(request, 'measurements_sensor.html', param)

# @login_required
# def measurements_all(request, unidade_pk, local_pk):
#     unidade = get_object_or_404(models.Unit, pk=unidade_pk)
#     local = get_object_or_404(models.Local, pk=local_pk)
#     if(unidade.user != request.user):
#         return HttpResponseForbidden()
#     measurements = []
#     collectors = models.Colector.objects.filter(local=local)
#     for collector in collectors:
#         sensors = models.Sensor.objects.filter(colector=collector)
#         for sensor in sensors:
#             measurements.extend(models.SensorMeasure.objects.filter(sensor=sensor))
#     data = serializers.serializer('json', measurements)
#     return data
