#!/usr/bin/python
# script: import gitlab projects into searchcode
# author: bert2002
# notes: 

import sys
import os
import json
import urllib2
from hashlib import sha1
from hmac import new as hmac
import pprint
import time

# Gitlab Settings
TOKEN = ''
GITLAB = 'https://gitlab.com/api/v4/'

# Searchcode Settings
publickey = ""
privatekey = ""

print "checking projects in gitlab"
req = urllib2.Request(GITLAB + 'projects?page=1&per_page=100')
req.add_header('Content-Type', 'application/json')
req.add_header('PRIVATE-TOKEN', TOKEN)
data = json.load(urllib2.urlopen(req))

for project in data:
  job_id = project['id']
  ssh_url_to_repo = project['ssh_url_to_repo']
  name_with_namespace = project['name_with_namespace']
  path_with_namespace = project['path_with_namespace']
  web_url = project['web_url']
  archived = project['archived']

  print("Repository: %s Archived: %s" % (name_with_namespace,archived))

  reponame = name_with_namespace
  repourl = ssh_url_to_repo
  repotype = "git"
  repousername = ""
  repopassword = ""
  reposource = web_url
  repobranch = "master"

  message = "pub=%s&reponame=%s&repourl=%s&repotype=%s&repousername=%s&repopassword=%s&reposource=%s&repobranch=%s" % (
    urllib.quote_plus(publickey),
    urllib.quote_plus(reponame),
    urllib.quote_plus(repourl),
    urllib.quote_plus(repotype),
    urllib.quote_plus(repousername),
    urllib.quote_plus(repopassword),
    urllib.quote_plus(reposource),
    urllib.quote_plus(repobranch)
  )

  sig = hmac(privatekey, message, sha1).hexdigest()
  url = "http://localhost:8080/api/repo/add/?sig=%s&%s" % (urllib.quote_plus(sig), message)
  data = urllib2.urlopen(url)
  data = data.read()
  data = json.loads(data)
  print data['sucessful'], data['message']

  sig = hmac(privatekey, message, sha1).hexdigest()
  url = "http://localhost:8080/api/repo/reindex/?sig=%s&%s" % (urllib.quote_plus(sig), message)
  data = urllib2.urlopen(url)
  data = data.read()
  time.sleep(1)
