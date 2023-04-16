from django.urls import path
from .views import home_view, opinions_view

urlpatterns = [
    path('', home_view, name='home'),
    path('opinions/', opinions_view, name='opinions')

]
