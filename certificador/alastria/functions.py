from web3 import Web3 
import datetime
from .abi import *
from web3.middleware import geth_poa_middleware
from django.conf import settings
import requests
from py_essentials import hashing as hs
import os

def calcular_hash(salt,texto,archivos):
    print(texto)
    if len(archivos)>1:
        archivos  = archivos.split(",") 
        hashes_archivos= ""
        for archivo in archivos:
            r = requests.get(archivo,allow_redirects=True)
            open('file.tmp','wb').write(r.content)
            file_hash = hs.fileChecksum('file.tmp',"sha256")
            hashes_archivos = hashes_archivos + str(file_hash)
            os.remove("file.tmp")
        hash= str(Web3.to_hex(Web3.solidity_keccak(['string'],[clean_text(texto)+hashes_archivos+salt])))
    else:
        hash= str(Web3.to_hex(Web3.solidity_keccak(['string'],[clean_text(texto)+salt])))
    print(clean_text(texto))
    print(hash)
    return hash

def obtener_hash(salt):
    w3 = Web3(Web3.HTTPProvider(settings.RPC_URL))
    w3.middleware_onion.inject(geth_poa_middleware,layer=0)
    contrato = w3.eth.contract(address=settings.ADDRESS_CERTIFICADOR,abi=abi_certificador)
    datos=  contrato.functions.getHash(salt).call()
    return Web3.toHex(datos)

def clean_text(texto):
    salida = texto.replace(r'\r',"")
    salida = salida.replace(r'\n',"")
    salida = salida.replace('\n',"")
    salida = salida.replace('\r',"")
    return salida