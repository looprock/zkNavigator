#!/usr/bin/env python
import sys
import os
import json
import re
from ConfigParser import SafeConfigParser
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

eo = './env-override.conf'
if os.path.exists(eo):
	try:
		fo = open(eo, "r+")
		env = fo.read(1).strip
	except:
		sys.exit("ERROR: environmen override present, but unable to read it!")
else:
	env = parser.get('default', 'env').strip()

apptype = parser.get('default', 'apptype').strip()
virtualenv = parser.get('default', 'virtualenv').strip()
activate_this = parser.get('default', 'activate_this').strip()
rootdir = parser.get('default', 'rootdir').strip()
templatedir = parser.get('default', 'templatedir').strip()
zkserver = parser.get(env, 'server').strip()
zkport = parser.get(env, 'port').strip()
defaultroot = parser.get(env, 'root').strip().replace("/","|")
baseurl = parser.get('fe', 'baseurl').strip()
enabledelete = parser.get('fe', 'enabledelete').strip()
watchpaths = parser.get('fe', 'watchpaths').strip()
# these don't do anything yet
#enableedit = parser.get('fe', 'enableedit').strip()
#enablecreate = parser.get('fe', 'enablecreate').strip()
#enablerename = parser.get('fe', 'enablerename').strip()
#enabledenvs = parser.get('fe', 'enabledenvs').strip()
server = "%s:%s" % (zkserver,zkport)

if virtualenv == "True":
        execfile(activate_this, dict(__file__=activate_this))

from kazoo.client import KazooClient
from kazoo.retry import KazooRetry

root = os.path.join(rootdir)
sys.path.insert(0, root)

from bottle import route, run, get, abort, post, request, template, redirect, default_app, debug, TEMPLATE_PATH, response

TEMPLATE_PATH.insert(0,templatedir)

kr = KazooRetry(max_tries=3)
zk = KazooClient(hosts=server)
zk.start()

def notifypath(node):
        for watch in watchpaths.split(","):
                if re.search(watch, node, re.IGNORECASE):
                        w = watch.split('/')
                        wl = len(w)
                        fp = node.split('/')
                        sites = ''
                        for i in range(1,wl):
                                sites += "/%s" % (fp[i])
                        ts = strftime('%Y-%m-%dT%H:%M:%S%Z', localtime())
                        try:
                                kr(zk.set, sites, ts)
                        except:
                                return "ERROR: unable to update %s!" % sites

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
	b = [ rr, d, enabledelete, baseurl ]
	return template('list', res=b)

@route('/json/')
@route('/json/<root>')
def list(root=defaultroot):
        response.content_type = 'application/json'
        rr = root.replace("|","/")
        if rr:
                if rr != "favicon.ico":
                        x = kr(zk.get_children, rr)
                        return json.dumps(sorted(x))

@route('/edit/<path>')
def edit(path):
	p = path.replace("|","/")
	x = kr(zk.get,p)[0]
	y = [ p, x, baseurl ]
	return template('edit', res=y)

@post('/editsub')
def editsub():
	node = request.forms.get('node').replace("|","/")
	notifypath(node)
	uf = node.replace("/","|")
	rp = node.replace("|","/")
	content = request.forms.get('content')
	try:
		kr(zk.set,rp,content)
		x = [ uf, rp, baseurl ]
		return template('editsub', res=x)
	except:
		return "ERROR: unable to update %s" % node

@route('/create/<path>')
def create(path):
	x = [ path, baseurl ]
        return template('create', res=x)

@post('/createsub')
def createsub():
	path = request.forms.get('path').replace("|","/")
	notifypath(path)
	node = request.forms.get('node')
	content = request.forms.get('content')
	fpath = "%s/%s" % (path,node)
	x = [ fpath, baseurl ]
	try:
		if content:
			kr(zk.create,fpath,value=content,makepath=True)
		else:
			kr(zk.create,fpath,makepath=True)
		return template('createsub', res=x)
	except:
		return "ERROR: unable to create %s!" % fpath

@route('/delete/<path>')
def delete(path):
	p = path.replace("|","/")
	x = [ p, baseurl ]
	notifypath(p)
	try:
		p = path.replace("|","/")
		kr(zk.delete,p,recursive=True)
        	return template('delete', res=x)
	except:
		return "ERROR: unable to delete %s!" % p

if apptype == "wsgi":
	application = default_app()
else:
	run(port=8080, debug=True)
