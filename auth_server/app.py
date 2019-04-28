from flask import Flask, request
from cryptography.fernet import Fernet
import requests
import json
import hashlib
import base64

app = Flask(__name__)
OAUTH_SERV = "http://10.140.100.103:5000/auth"

def dec_pass(ct, key):
    cs = Fernet(key)
    pt = cs.decrypt(bytes(ct.encode()))
    return pt