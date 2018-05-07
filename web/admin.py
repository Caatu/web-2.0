from django.contrib import admin

# Register your models here.
from web.models import *

class UnitAdmin(admin.ModelAdmin):
    pass
admin.site.register(Unit, UnitAdmin)

class LocalAdmin(admin.ModelAdmin):
    pass
admin.site.register(Local, LocalAdmin)

class ColectorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Colector, ColectorAdmin)

class SensorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Sensor, SensorAdmin)

class AlertAdmin(admin.ModelAdmin):
    pass
admin.site.register(Alert, AlertAdmin)

class SensorTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(SensorType, SensorTypeAdmin)

class SensorMeasureAdmin(admin.ModelAdmin):
    pass
admin.site.register(SensorMeasure, SensorMeasureAdmin)