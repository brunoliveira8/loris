#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Loris is a simple micro-framework for small web applications written in a 
single file.

Dependencies: Python Standard Library and WebOb library.

Homepage and documentation: no available yet.

Copyright (c) 2015, Tarcisio Bruno C. Oliveira
"""

def app(environ, start_response):
    start_response('200 OK', [('content-type', 'text/html')])
    return ['Hello world!']

if __name__ == '__main__':
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8080')