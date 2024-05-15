from django.db import models
from web3 import Web3 
import datetime
from django.utils import timezone
from .abi import *
from web3.middleware import geth_poa_middleware
from django.conf import settings
from eth_account import Account
from hexbytes import HexBytes
import hashlib
from urllib.request import urlopen
from py_essentials import hashing as hs
import requests
import os
from .functions import *
from .tasks import sendRecordToAlastria

class Estado(models.Model):
    estado= models.CharField(max_length=20)
    contador= models.IntegerField(default=0)

# Create your models here.
class RegistroManager(models.Manager):
    def no_procesados(self):
        return self.filter(procesado=False)

class Registro(models.Model):
    num_registro = models.IntegerField(unique=True)
    datos= models.TextField()
    archivos= models.TextField(blank=True,null=True)
    salt= models.CharField(max_length=40)
    fecha= models.DateTimeField(blank=True)
    procesado= models.BooleanField(default=False)
    hash= models.CharField(max_length=400,null=True,blank=True)
    comprobante= models.CharField(max_length=400,null=True,blank=True)
    callback_url= models.CharField(max_length=400,null=True,blank=True)
    estado= models.CharField(max_length=20,default="pendiente")
    manager=RegistroManager

    def calcularHash(self):
        return calcular_hash(self.salt,self.datos,self.archivos)

    def save(self,*args,**kwargs):
        if self.datos=="error":
            raise ValueError("Hash en blanco")
        if self.callback_url is None:
            raise ValueError("Callback en blanco")
        #obtenemos el hash de los archivos de texto   
        self.hash=self.calcularHash()
        self.fecha=timezone.now()
        super().save(*args,**kwargs)
        #ingresamos la transaccion correspondiente al contrato



    def obtenerAntiguedad(self):
        w3 = Web3(Web3.HTTPProvider("http://alastriat.citymis.co/rpc"))
        w3.middleware_onion.inject(geth_poa_middleware,layer=0)
        #obtenemos la transaccion
        if Web3.is_hex(self.comprobante)==False:
            transaccion = w3.eth.get_transaction(Web3.to_hex(self.comprobante))
        else:
            transaccion = w3.eth.get_transaction(self.comprobante)
        bloque= transaccion['blockNumber']
        #obtenemos la informacion del bloquefge
        reciboBloque= w3.eth.get_block(bloque)
        timestamp = reciboBloque.timestamp
        #buscamos el bloque actual
        bloqueActual= w3.eth.block_number
        confirmaciones= bloqueActual-bloque
        fecha_actual = datetime.datetime.now()
        fecha_bloque = datetime.datetime.fromtimestamp(timestamp)
        tiempo_confirmacion = (fecha_actual - fecha_bloque)
        dias_confirmacion = tiempo_confirmacion.days
        salida= {}
        salida['comprobante'] = self.comprobante
        salida['fecha_ingreso'] = fecha_bloque.strftime("%d/%M/%Y %H:%M:%S")
        salida['dias_confirmacion']=dias_confirmacion
        salida['bloques_confirmacion']=confirmaciones
        salida['link_confirmacion']="https://blkexplorer1.telsius.alastria.io/transaction/"+self.comprobante 
        return salida
