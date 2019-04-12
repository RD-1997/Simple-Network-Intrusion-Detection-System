#!/bin/bash

openssl genrsa -des3 -out test.key 4096
openssl req -new -x509 -days 3650 -key ../ssl/test.key -out ../ssl/test.cert
