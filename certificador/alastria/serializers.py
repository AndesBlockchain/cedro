from .models import Registro
from rest_framework import serializers

class RegistroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= Registro
        fields=['num_registro','datos','archivos','fecha','procesado','hash','salt','comprobante','callback_url']
