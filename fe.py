#!/usr/bin/env python
import sys
import os
import json
import re
from ConfigParser import SafeConfigParser
from bottle import route, run, get, abort, post, request, template, redirect, default_app, debug, TEMPLATE_PATH, response
from kazoo.client import KazooClient
from kazoo.retry import KazooRetry
from time import time, localtime, strftime

if os.path.exists('./zk.conf'):
   parser = SafeConfigParser()
   parser.read('./zk.conf')
elif os.path.exists('/etc/zktools/zk.conf'):
   parser = SafeConfigParser()
   parser.read('/etc/zktools/zk.conf')
else:
   print "No config file found! Please create: ./zk.conf or /etc/zktools/zk.conf"
   sys.exit(1)

bind = parser.get('default', 'bind').strip()
env = parser.get('default', 'env').strip()
zkserver = parser.get(env, 'server').strip()
zkport = parser.get(env, 'port').strip()
defaultroot = parser.get(env, 'root').strip().replace("/","|")
enabledelete = parser.get('fe', 'enabledelete').strip()
# these don't do anything yet
enableedit = parser.get('fe', 'enabledelete').strip()
enablecreate = parser.get('fe', 'enabledelete').strip()
enablerename = parser.get('fe', 'enabledelete').strip()
enabledenvs = parser.get('fe', 'enabledelete').strip()

server = "%s:%s" % (zkserver,zkport)

kr = KazooRetry(max_tries=3)
zk = KazooClient(hosts=server)
zk.start()

def tpl(name, **kwargs):
  html = template(name, kwargs)
  return template('layout', html=html)


@route('/')
@route('/<root>')
def list(root=defaultroot):
        d = {}
	rr = root.replace("|","/")
	if rr:
		if rr != "favicon.ico":
			x = kr(zk.get_children, rr)
			for i in x:
				try:
					p = "%s/%s" % (rr,i)
					y = kr(zk.get,p)[0]
					d[i] = y
				except:
					print "Couldn't get child from: %s" % p
	b = [ rr, d, enabledelete ]
	return tpl('list', res=b)

@route('/json/')
@route('/json/<root>')
def list(root=defaultroot):
	response.content_type = 'application/json'
	rr = root.replace("|","/")
	if rr:
		if rr != "favicon.ico":
			x = kr(zk.get_children, rr)
			return json.dumps(x)

@route('/content/')
@route('/content/<root>')
def list(root=defaultroot):
        rr = root.replace("|","/")
        if rr:
                if rr != "favicon.ico":
                        x = kr(zk.get, rr)[0]
                        return x

@route('/edit/<path>')
def edit(path):
	p = path.replace("|","/")
	x = kr(zk.get,p)[0]
	y = [ p, x]
	return tpl('edit', res=y)

@post('/editsub')
def editsub():
	node = request.forms.get('node').replace("|","/")
	uf = node.replace("/","|")
	rp = node.replace("|","/")
	content = request.forms.get('content')
	try:
		kr(zk.set,rp,content)
		x = [ uf, rp ]
		return tpl('editsub', res=x)
	except:
		return "ERROR: unable to update %s" % node

@route('/create/<path>')
def create(path):
        return tpl('create', res=path)

@post('/createsub')
def createsub():
	path = request.forms.get('path').replace("|","/")
	node = request.forms.get('node')
	content = request.forms.get('content')
	fpath = "%s/%s" % (path,node)
	try:
		if content:
			kr(zk.create,fpath,value=content,makepath=True)
		else:
			kr(zk.create,fpath,makepath=True)
		return tpl('createsub', res=fpath)
	except:
		return "ERROR: unable to create %s!" % fpath

@route('/delete/<path>')
def delete(path):
	p = path.replace("|","/")
	try:
		p = path.replace("|","/")
		kr(zk.delete,p,recursive=True)
        	return tpl('delete', res=p)
	except:
		return "ERROR: unable to delete %s!" % p


run(host=bind, port=8080, debug=True)
