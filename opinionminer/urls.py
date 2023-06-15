from django.urls import path
from .views import home_view, opinions_view, ViewPDF
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('', home_view, name='home'),
    path('opinions/', opinions_view, name='opinions'),
    path('opinions/pdf/', ViewPDF.as_view(), name="opinions_pdf"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)