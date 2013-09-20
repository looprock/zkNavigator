zkNavigator
===========

A lightweight browser/editor for zookeeper

== Usage

zkNavigator is a bottle based application that gives you a quick and dirty zookeeper viewer/editor in your browser. It requires python kazoo to function, but everything beyond that is packaged here.  Once you install kazoo, to get started just configure zk.conf for your environment, launch ./fe.py and point your browser at localhost:8080

== Configuration

=== default section
env - defines what zookeeper configuration to use below RE: alpha
apptype - to use as described above, set to standalone but can also be used under wsgi - options: standalone, wsgi
rootdir = - path your running this from
templatedir - path to your views directory
virtualenv - running under virtualenv?: True/False
activate_this - if True above, this is your path to activate_this.py

These are examples multiple environment configurations. You need to have at least one section that maps to env in the default section:

[local]
server = localhost
port = 2181
root = /

[alpha]
server = alpha.zk.server.com
port = 2181
root = /

[beta]
server = beta.zk.server.com
port = 2181
root = /

=== fe section
baseurl - where do you hit / for this app?
enabledelete - enable the delete link on all the zNodes, kinda dangerous - options: T/F
