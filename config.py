# -*- coding: utf-8 -*-

import socket

DEBUG = False

if socket.gethostname() == 'zub':
    DEBUG = True
