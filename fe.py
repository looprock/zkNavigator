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
	return template('list', res=b)

@route('/json/')
@route('/json/<root>')
def list(root=defaultroot):
	response.content_type = 'application/json'
	rr = root.replace("|","/")
	if rr:
		if rr != "favicon.ico":
			x = kr(zk.get_children, rr)
			return json.dumps(x)

@route('/edit/<path>')
def edit(path):
	p = path.replace("|","/")
	x = kr(zk.get,p)[0]
	y = [ p, x]
	return template('edit', res=y)

@post('/editsub')
def editsub():
	node = request.forms.get('node').replace("|","/")
	# if we're modifying to /vast/envs/.*/sites/*, update /vast/envs/.*/sites
	if re.search('/vast/envs/.*/sites', node, re.IGNORECASE):
		fp = node.split('/')
		print fp
		sites = '/%s/%s/%s/%s' % (fp[1],fp[2],fp[3],fp[4])
		ts = strftime('%Y-%m-%dT%H:%M:%S%Z', localtime())
		try:
			kr(zk.set, sites, ts)
		except:
			return "ERROR: unable to update %s!" % sites
	uf = node.replace("/","|")
	rp = node.replace("|","/")
	content = request.forms.get('content')
	try:
		kr(zk.set,rp,content)
		x = [ uf, rp ]	
		return template('editsub', res=x)
	except:
		return "ERROR: unable to update %s" % node

@route('/create/<path>')
def create(path):
        return template('create', res=path)

@post('/createsub')
def createsub():
	path = request.forms.get('path').replace("|","/")
	# if we're modifying to /vast/envs/.*/sites/*, update /vast/envs/.*/sites
        if re.search('/vast/envs/.*/sites', path, re.IGNORECASE):
                fp = path.split('/')
		print fp
		sites = '/%s/%s/%s/%s' % (fp[1],fp[2],fp[3],fp[4])
		ts = strftime('%Y-%m-%dT%H:%M:%S%Z', localtime())
                try:
                        kr(zk.set, sites, ts)
                except:
                        return "ERROR: unable to update %s!" % sites
	node = request.forms.get('node')
	content = request.forms.get('content')
	fpath = "%s/%s" % (path,node)
	try:
		if content:
			kr(zk.create,fpath,value=content,makepath=True)
		else:
			kr(zk.create,fpath,makepath=True)
		return template('createsub', res=fpath)
	except:
		return "ERROR: unable to create %s!" % fpath

@route('/delete/<path>')
def delete(path):
	p = path.replace("|","/")
	# if we're modifying to /vast/envs/.*/sites/*, update /vast/envs/.*/sites
        if re.search('/vast/envs/.*/sites', p, re.IGNORECASE):
                fp = p.split('/')
		print fp
		sites = '/%s/%s/%s/%s' % (fp[1],fp[2],fp[3],fp[4])
		ts = strftime('%Y-%m-%dT%H:%M:%S%Z', localtime())
		print sites
                try:
                        kr(zk.set, sites, ts)
                except:
                        return "ERROR: unable to update %s!" % sites
	try:
		p = path.replace("|","/")
		kr(zk.delete,p,recursive=True)
        	return template('delete', res=p)
	except:
		return "ERROR: unable to delete %s!" % p


#run(host='0.0.0.0', port=8080, debug=True)
run(port=8080, debug=True)
