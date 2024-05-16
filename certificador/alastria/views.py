from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Registro
from rest_framework import viewsets
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from .serializers import RegistroSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .functions import *
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
class RegistroViewSet(viewsets.ModelViewSet):
    queryset= Registro.objects.all()
    serializer_class= RegistroSerializer
    permission_classes=[permissions.AllowAny]


@api_view(['GET'])
def confirmaciones(request,key):
    objeto = Registro.objects.get(salt=key)
    return Response(objeto.obtenerAntiguedad())

def iframe_confirmaciones(request,salt):
    objeto = Registro.objects.get(salt=salt)
    datos = objeto.obtenerAntiguedad()
    iframe_data={}
    iframe_data['dias_confirmacion'] = datos['dias_confirmacion']
    return render(request,"iframe_confirmaciones.html",datos)

@csrf_exempt
def verificar(request):
    salt= request.POST['salt']
    texto= request.POST['licencia']
    archivos= request.POST['archivos']
    hash_calculado= calcular_hash(salt,texto,archivos)
    try:
        hash_guardado= obtener_hash(salt)
        print(hash_guardado)
        print(hash_calculado)
        salida= {}
        if hash_guardado==hash_calculado:
            objeto = Registro.objects.get(salt=request.POST['salt'])
            datos = objeto.obtenerAntiguedad()
            iframe_data={}
            iframe_data['dias_confirmacion'] = datos['dias_confirmacion']
            return render(request,"iframe_confirmaciones.html",datos)
        else:
            return render(request,"iframe_error.html")
    except Exception as e:
        print(str(e))
        return HttpResponse("Debido a la sobrecarga de trabajo de la red Alastria, no es posible verificar la informacion ahora. Reintente en unos minutos")