import os
import OpenSSL
os.system("openssl req -new -x509 -key privkey.pem -out cacert.pem -days 1095")
