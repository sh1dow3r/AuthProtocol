from flask import *
import requests
import json
import hashlib
import base64
from cryptography.fernet import Fernet
app = Flask(__name__)
AuthServerIP = "10.150.32.2"
AppServerIP = "10.150.32.3"


def dec(token, passwd):
    """
    takes  the tokens with predeterminde key and decrypt the message
    """
    passenc = passwd.encode() 
    passHash = hashlib.sha256(passenc)  #hashing the password using sha256
    passHash = passHash.digest()  # to obtain the digest of the byte string 
    key = base64.urlsafe_b64encode(passHash) # Encode the bytes-like object s using Base64 and return the encoded bytes
    f = Fernet(key) #cipher text
    decrypted = f.decrypt(token)  #decrypting the token
    return decrypted

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth', methods=["POST"])
def passCreds():
    user = request.form['username']
    passwd = request.form['password']
    req = requests.post('http://'+AuthServerIP+'/auth',  json={"username": user, "password":passwd})
    result = req.json()
    checkFail_1 = result["auth"] == "fail"
    checkFail_2 = result["auth"] == "success"
    if "auth" in result and checkFail_1:
        return "Wrong Creds, try again! "

    elif 'auth' in result and checkFail_2:
        token = result['token']
        dec(token, passwd)
        r = requests.post('http://'+AppServerIP+'/auth', json={ 'token': token })
        return r.text
    else:
        return 'Error Unknown'
    

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=5000, debug=True)