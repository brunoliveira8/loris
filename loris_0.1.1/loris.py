#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Loris is a simple micro-framework for small web applications written in a 
single file.

Dependencies: Python Standard Library and WebOb library.

Homepage and documentation: no available yet.

Copyright (c) 2015, Tarcisio Bruno C. Oliveira
"""

import re
import sys
from webob import Request, Response, exc
from paste import httpserver

#Run Server
def run(app, host='127.0.0.1', port='8080'):
	httpserver.serve(app, host, port)

#Templating
var_regex = re.compile(r'''
	\{          # The exact character "{"
	(\w+)       # The variable name (restricted to a-z, 0-9, _)
	(?::([^}]+))? # The optional :regex part
	\}          # The exact character "}"
	''', re.VERBOSE)

def template_to_regex(template):
	regex = ''
	last_pos = 0
	for match in var_regex.finditer(template):
		regex += re.escape(template[last_pos:match.start()])
		var_name = match.group(1)
		expr = match.group(2) or '[^/]+'
		expr = '(?P<%s>%s)' % (var_name, expr)
		regex += expr
		last_pos = match.end()

	regex += re.escape(template[last_pos:])
	regex = '^%s$' % regex
	return regex

#Rounting 
def load_controller(string):
	module_name, func_name = string.split(':', 1)
	__import__(module_name)
	module = sys.modules[module_name]
	func = getattr(module, func_name)
	return func


class Router(object):
	def __init__(self):
		self.routes = []

	def add_route(self, template, controller, **vars):
		if isinstance(controller, basestring):
			controller = load_controller(controller)
		self.routes.append((re.compile(template_to_regex(template)),controller,vars))

	def __call__(self, environ, start_response):
		req = Request(environ)
		for regex, controller, vars in self.routes:
			match = regex.match(req.path_info)
			if match:
				req.urlvars = match.groupdict()
				req.urlvars.update(vars)
				return controller(environ, start_response)
		return exc.HTTPNotFound()(environ, start_response)

#Controller
def controller(func):
	def replacement(environ, start_response):
		req = Request(environ)
		try:
			resp = func(req, **req.urlvars)
		except exc.HTTPException, e:
			resp = e
		if isinstance(resp, basestring):
			resp = Response(body=resp)
		return resp(environ, start_response)
	return replacement

