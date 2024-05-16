from django.contrib import admin
from .models import * 


class RegistroAdmin(admin.ModelAdmin):
    list_display=('num_registro','datos','procesado','hash','salt','comprobante','estado')

# Register your models here.
admin.site.register(Registro,RegistroAdmin)
admin.site.register(Estado)