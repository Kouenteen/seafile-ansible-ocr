#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import hashlib
import base64

from os import urandom
from base64 import b64encode
from hashlib import pbkdf2_hmac

password='route'
salt=urandom(32)
hex = hashlib.pbkdf2_hmac('sha256', password, salt, 10000, 32)
print('PBKDF2SHA256$10000$' + salt.encode('hex') + '$' + hex.encode('hex'))