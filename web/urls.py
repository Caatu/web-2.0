from django.urls import include, path, re_path
import web.views as views
urlpatterns = [
    path('', views.home, name='home'),
    path('unidade/<int:pk>/', views.local, name='locals'),
    path('unidade/<int:unidade_pk>/local/<int:local_pk>/', views.sensors, name='sensors'),
]