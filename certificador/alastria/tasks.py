from celery import Celery,shared_task
from celery.schedules import crontab
from web3 import Web3
from web3.middleware import geth_poa_middleware
from django.conf import settings
from eth_account import Account
from .abi import *
from datetime import timedelta
from django.utils import timezone
import logging
import boto3
import requests

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


aws_access_key_id = settings.AWS_ACCESS_KEY
aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
region_name = settings.REGION_NAME

app = Celery('tasks', broker='pyamqp://guest@0.0.0.0:5672//')
session = boto3.Session(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
sns_client = session.client('sns')

@app.task(name="sendRecordToAlastria")
def sendRecordToAlastria():
    from .models import Registro, Estado
    w3 = Web3(Web3.HTTPProvider(settings.RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware,layer=0)

    if Estado.objects.count()==0:
        estado = Estado(estado="online",contador=0)
        estado.save()

    estado = Estado.objects.first()
    #revisamos el estado actual del nodo
    try:
        chainId= w3.eth.chain_id
    except Exception as e:
        logger.error("Error en la conexion con el nodo")
        estado.estado="offline"
        #nodo fuera de linea
        if estado.estado == "offline":
            estado.contador=estado.contador+1
            estado.save()
            if estado.contador > 1440:
                mensaje = 'Nodo Citymis fuera de linea'
                estado.contador=0
                estado.save()
                response = sns_client.publish(TopicArn=settings.CITYMIS_AWS_TOPIC,
                                            Message=mensaje,
                                            Subject='Nodo fuera de linea')
                return Exception("Node offline")
    
    sync = w3.eth.syncing
    if sync:
        #nodo fuera de sincronia
        logger.error("Node out of sync")
        estado.estado="no_sync"
        if estado.estado == "no_sync":
            estado.contador=estado.contador+1
            estado.save()
            if estado.contador > 1440:
                mensaje = 'Nodo Citymis fuera de sincronia'
                estado.contador=0
                estado.save()
                response = sns_client.publish(TopicArn=settings.CITYMIS_AWS_TOPIC,
                                            Message=mensaje,
                                            Subject='Nodo fuera de sincronia')
                return Exception("Node out of sync")
            
    estado.estado="online"
    estado.contador=0
    estado.save()

    #nodo OK para ejecutar una tx
    contrato = w3.eth.contract(address=settings.ADDRESS_CERTIFICADOR,abi=abi_certificador)
    pk=settings.PK
    acct= Account.from_key(pk)

    if Registro.objects.filter(estado="pendiente").exists():
        #si no hay registro en proceso, tomamos el primer registro pendiente
        logger.info("enviando registro a alastria")
        registro = Registro.objects.filter(estado="pendiente").first()
        registro.estado="procesando"
        registro.save()

        try:
            nonce = w3.eth.get_transaction_count(acct.address) 
            logger.info("Wallet Nonce:" + str(nonce))
            tx = contrato.functions.setHash(registro.salt,registro.hash).build_transaction({'from':acct.address,'nonce':nonce,'gasPrice':0,'gas':30000000})
            signed_tx= acct.sign_transaction(tx)
            tx_hash= w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            registro = Registro.objects.filter(estado="procesando").first()
            registro.estado="listo"
            registro.procesado=True
            registro.comprobante=tx_hash
            registro.save()
            logger.info(receipt)
            call= requests.post(registro.callback_url,data={"estado":"ok"})
            return receipt
        except Exception as e:
            #Falla dura, no es posible reintentar
            logger.error("Error en la transaccion")
            registro.estado="falla"
            registro.save()
            call= requests.post(registro.callback_url,data={"estado":"falla"})
            return "falla"

    logger.info("No hay registros pendientes")