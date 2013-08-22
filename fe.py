#!/usr/bin/env python
import sys
import os
import json
from ConfigParser import SafeConfigParser
from bottle import route, run, get, abort, post, request, template, redirect, default_app, debug, TEMPLATE_PATH
from kazoo.client import KazooClient

if os.path.exists('./zk.conf'):
   parser = SafeConfigParser()
   parser.read('./zk.conf')
elif os.path.exists('/etc/zktools/zk.conf'):
   parser = SafeConfigParser()
   parser.read('/etc/zktools/zk.conf')
else:
   print "No config file found! Please create: ./zk.conf or /etc/zktools/zk.conf"
   sys.exit(1)

env = parser.get('fe', 'defaultenv').strip()
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

zk = KazooClient(hosts=server)
zk.start()

@route('/')
@route('/<root>')
def list(root=defaultroot):
        d = {}
	rr = root.replace("|","/")
	if rr:
		if rr != "favicon.ico":
			x = zk.get_children(rr)
			for i in x:
				try:
					p = "%s/%s" % (rr,i)
					y = zk.get(p)[0]
					d[i] = y
				except:
					print "Couldn't get child from: %s" % p
	b = [ rr, d, enabledelete ]
	zk.stop()
	return template('list', res=b)

@route('/edit/<path>')
def edit(path):
	p = path.replace("|","/")
	x = zk.get(p)[0]
	y = [ p, x]
	zk.stop()
	return template('edit', res=y)

@post('/editsub')
def editsub():
	node = request.forms.get('node').replace("|","/")
	uf = node.replace("/","|")
	rp = node.replace("|","/")
	content = request.forms.get('content')
	try:
		zk.set(rp, content)
		x = [ uf, rp ]	
		zk.stop()
		return template('editsub', res=x)
		#return "OK: updated!<p><a href=\"/%s\">return to %s</a><p>" % (node,rp)
	except:
		return "ERROR: unable to update %s" % node

@route('/create/<path>')
def create(path):
        return template('create', res=path)

@post('/createsub')
def createsub():
	path = request.forms.get('path').replace("|","/")
	node = request.forms.get('node')
	content = request.forms.get('content')
	fpath = "%s/%s" % (path,node)
	try:
		if content:
			zk.create(fpath, value=content, makepath=True)
		else:
			zk.create(fpath, makepath=True)
		zk.stop()
		return template('createsub', res=fpath)
	except:
		return "ERROR: unable to create %s!" % fpath

@route('/delete/<path>')
def delete(path):
	p = path.replace("|","/")
	try:
		p = path.replace("|","/")
		zk.delete(p, recursive=True)
		zk.stop()
        	return template('delete', res=p)
	except:
		return "ERROR: unable to delete %s!" % p


#run(host='0.0.0.0', port=8080, debug=True)
run(port=8080, debug=True)
