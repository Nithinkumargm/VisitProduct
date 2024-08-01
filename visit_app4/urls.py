from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import DairyAPIView, TalukAPIView, VillageAPIView, EmployeeAPIView, VisitTypeAPIView, VisitAPIView, load_taluks, load_villages,load_dairies


urlpatterns = [
    path('load-taluks/', load_taluks, name='ajax_load_taluks'),
    path('load-villages/', load_villages, name='ajax_load_villages'),
    path('load-dairies/', load_dairies, name='load_dairies'),
    path('dairies/', DairyAPIView.as_view(), name='dairy-list'),
    path('dairies/<str:name>/', DairyAPIView.as_view(), name='dairy-detail'),
    path('taluks/', TalukAPIView.as_view(), name='taluk-list'),
    path('taluks/<str:name>/', TalukAPIView.as_view(), name='taluk-detail'),
    path('villages/', VillageAPIView.as_view(), name='village-list'),
    path('villages/<str:name>/<str:taluk_name>/', VillageAPIView.as_view(), name='village-detail'),
    path('employees/', EmployeeAPIView.as_view(), name='employee-list'),
    path('employees/<str:name>/<str:role>/', EmployeeAPIView.as_view()),
    path('visit_types/', VisitTypeAPIView.as_view(), name='visit-type-list'),
    path('visit_types/<str:name>/', VisitTypeAPIView.as_view(), name='visit-type-detail'),
    path('visits/', VisitAPIView.as_view(), name='visit-list'),
    path('visits/<str:employee_name>/', VisitAPIView.as_view(), name='visit-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
