from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from alastria.views import *

router= routers.DefaultRouter()
router.register(r'registro',RegistroViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    path('confirmaciones/<str:key>',confirmaciones),
    path('verificar',verificar,name="verificar"),
    path('iframe/confirmaciones/<str:salt>',iframe_confirmaciones,name="iframe_confirmaciones"),
]
