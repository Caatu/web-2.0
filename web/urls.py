from django.urls import include, path, re_path
import web.views as views
urlpatterns = [
    path('', views.home, name='home'),

    path('unidade', views.unit_stuff, name='nova_unidade'),

    path('unidade/<int:pk>/delete', views.del_unit, name='del_unidade'),

    path('unidade/<int:pk>/', views.local, name='locals'),

    path('local/<int:pk>/', views.novo_local, name='novo_local'),

    path('unidade/<int:pk_unit>/local/<int:pk_local>/delete', views.del_local, name='del_local'),

    path('unidade/<int:unidade_pk>/local/<int:local_pk>',
         views.sensors, name='sensors'),

    path('unidade/<int:unidade_pk>/local/<int:local_pk>/sensor/<int:sensor_pk>/measurements/',
         views.measurements_sensor, name='measurements_sensor'),

    path('ajax/sensor/<int:sensor_pk>',
         views.measurements_sensor_ajax, name='measurements_sensor_ajax')
]
