import json
import datetime
from dateutil import parser
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core import serializers
from django.core.serializers.json import Serializer
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Max, Min, Avg
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
def new_unit(request):
    if request.method == 'POST':
        form = UnitForm(request.form)
        if form.is_valid():
            unit = Unit.create(request.user, form.data['name'])
            unit.save()
            param = {
                'units': models.Unit.objects.filter(user=request.user)
            }
            return render(request, 'home.html', param)
        else:
            return HttpResponse(status=406)
    else:
        return HttpResponse(status=405)


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
def measurements_sensor_ajax(request, sensor_pk):
    """
        Eu sei que esta uma porra.. mas funciona.
    """
    measurements = models.SensorMeasure.objects.filter(sensor=sensor_pk)
    return JsonResponse(
        get_sensor_data(measurements),
        safe=False
    )


def get_sensor_data(measurements):
    data = json.loads(
        serializers.serialize('json', measurements, fields=(
            'unit_of_measurement', 'measurement_value', 'created_at'))
    )
    return_data = {
        'label': 'Ultimos Dados',
        'data': [],
        'backgroundColor': 'rgba(54, 162, 235, 0.2)',
        'borderColor': 'rgba(54, 162, 235, 0.2)',
    }
    for d in data:
        json_dict = {
            'y': float(d['fields']['measurement_value']),
            'x': unix_time_millis(
                parser.parse(d['fields']['created_at']).replace(tzinfo=None)
            )
        }
        print("chamou aqui")
        return_data['data'].append(json_dict)
    return {'datasets': [return_data]}


def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0


@login_required
def measurements_sensor(request, unidade_pk, local_pk, sensor_pk):
    unidade = get_object_or_404(models.Unit, pk=unidade_pk)
    local = get_object_or_404(models.Local, pk=local_pk)
    sensor = get_object_or_404(models.Sensor, pk=sensor_pk)

    measurements = models.SensorMeasure.objects.filter(sensor=sensor_pk)
    param = {
        'unit': unidade,
        'local': local,
        'sensor': sensor,
        'max': measurements.aggregate(Max('measurement_value'))['measurement_value__max'],
        'min': measurements.aggregate(Min('measurement_value'))['measurement_value__min'],
        'avg': measurements.aggregate(Avg('measurement_value'))['measurement_value__avg'],
        'data': json.dumps(get_sensor_data(measurements))
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
