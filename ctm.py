# -*- coding: utf-8 -*-
# when testing if you want to point to a separate ctm domain export CTM_HOST
import ssl
import socket
import os
import http.client
from base64 import b64encode
import json
import urllib
import uuid

class Client:
  """
    A client for accessing the CTM REST API
  """
  def __init__(self, account=None, token=None, secret=None,
               timeout=30, host="api.calltrackingmetrics.com",
               version="v1", debug=(os.environ['CTM_ENV'] == 'development')):
    """
      Create a CallTrackingMetrics REST Client
    """
    self.debug   = debug
    self.account = int(account)
    self.auth    = b64encode( ('%s:%s' % (token, secret)).encode('ascii') ).decode("ascii")
    self.host    = host
    self.base    = "/api/%s/" % version
    self.version = version

    if self.debug:
      print("%s %s" % (self.host, self.account))

  def set_account(self, account):
    self.account = int(account)

  def _get_http_conn(self):
    return http.client.HTTPSConnection(self.host)

  def _request(self, method, path, data={}):
    path    = path.rstrip('/')
    url     = self.base + path
    headers = {
                'Authorization' : 'Basic %s' % self.auth,
                'Content-Type'  : 'application/json'
              }
    conn    = self._get_http_conn()
    if self.debug: 
      print("request: https://%s%s" % (self.host, url))

    if method == 'POST':
      body = json.dumps(data)
      if self.debug:
        print(body)
      conn.request("POST", url, body=body, headers=headers)
    elif method == 'GET':
      conn.request("GET", url + "?" + urllib.parse.urlencode(data,True), headers=headers)
    elif method == 'DELETE':
      conn.request("DELETE", url + "?" + urllib.parse.urlencode(data,True), headers=headers)
    elif method == 'UPLOAD':
      headers.pop('Content-Type', None)
      conn.request("PUT", url, body=data, headers=headers)
    elif method == 'PUT':
      data['_method'] = 'PUT'
      conn.request("POST", url, body=urllib.parse.urlencode(data,True), headers=headers)

    r = conn.getresponse()
    if r.status == 200:
      try:
        response = json.load(r)
      except ValueError:
        print("error parsing response")
        response = r.read()
    else:
      response = r.read()
    return (r.status, response)

  def calls(self, options={}):
    return self._request('POST', 'accounts/%d/calls/search.json' % self.account, options)

  def call(self, call_id):
    return self._request('GET', 'accounts/%d/calls/%d' % (self.account, call_id))

  def sale(self, call_id, name=None, score=None, conversion=None, value=None):
    data = {
      "name":       name,
      "score":      score,
      "conversion": conversion,
      "value":      value
    }
    return self._request('POST', 'accounts/%d/calls/%d/sale' % (self.account, call_id), data)

  def modify(self, call_id, options={}):
    return self._request('POST', 'accounts/%d/calls/%d/modify' % (self.account, call_id), {"call": options})

  def forms(self, options={}):
    return self._request('GET', 'accounts/%d/form_reactors' % self.account, options)

  def postform(self, form_id, options={}):
    return self._request('POST', 'formreactor/%s' % form_id, options)

  def webhooks(self, options={}):
    return self._request('GET', 'accounts/%d/form_reactors' % self.account, options)

  # agency api
  def googlelinks(self):
    return self._request('GET', 'accounts/%d/ga/link' % self.account)

  def numbers(self, options={}):
    return self._request('GET', 'accounts/%d/numbers' % self.account, options)

  def search_numbers(self, searchby, country, pattern):
    options = {
      "searchby": searchby,
      "country": country,
      "pattern": pattern
    }
    return self._request('GET', 'accounts/%d/numbers/search' % self.account, options)

  def buy_number(self, phone_number):
    return self._request('POST', 'accounts/%d/numbers' % self.account, {"phone_number": phone_number})

  def update_number(self, number_id, options):
    return self._request('POST', 'accounts/%d/numbers/%s/update_number' % (self.account, number_id), options)

  def call_settings(self, options={}):
    return self._request('GET', 'accounts/%d/call_settings' % self.account, options)

  def create_call_settings(self, options={}):
    return self._request('POST', 'accounts/%d/call_settings' % self.account, options)

  def update_call_settings(self, call_setting_id, options={}):
    return self._request('PUT', 'accounts/%d/call_settings/%s' % (self.account, call_setting_id), options)

  def delete_call_settings(self, call_setting_id):
    return self._request('DELETE', 'accounts/%d/call_settings/%s' % (self.account, call_setting_id))

  def receiving_numbers(self, options={}):
    return self._request('GET', 'accounts/%d/receiving_numbers' % self.account, options)

  def create_receiving_number(self, options={}):
    return self._request('POST', 'accounts/%d/receiving_numbers' % self.account, options)

  def update_receiving_number(self, number_id, options={}):
    return self._request('PUT', 'accounts/%d/receiving_numbers/%s' % (self.account, number_id), options)

  def delete_receiving_number(self, number_id):
    return self._request('DELETE', 'accounts/%d/receiving_numbers/%s' % (self.account, number_id))

  def sources(self, options={}):
    return self._request('GET', 'accounts/%d/sources' % self.account, options)

  def create_source(self, options={}):
    return self._request('POST', 'accounts/%d/sources' % self.account, options)

  def update_source(self, source_id, options={}):
    return self._request('PUT', 'accounts/%d/sources/%s' % (self.account, source_id), options)

  def delete_source(self, source_id):
    return self._request('DELETE', 'accounts/%d/sources/%s' % (self.account, source_id))

  def accounts(self, options={}):
    return self._request('GET', 'accounts', options)

  # create a new account using an agency 
  # ```
  #   status, account = client.create_account({
  #    "account": {
  #       "name": "Test Account"
  #     },
  #     "billing_type": "existing"
  #   })
  # -- {u'status': u'success', u'id': 18692, u'name': u'Test Account'}
  # ```
  def create_account(self, options={}):
    return self._request('POST', 'accounts', options)

  def cancel_account(self):
    return self._request('DELETE', 'accounts/%d' % self.account)

  def geo_routers(self, options={}):
    return self._request('GET', 'accounts/%d/geo_routes' % self.account)

  def create_geo_router(self, options={}):
    return self._request('POST', 'accounts/%d/geo_routes' % self.account, options)

  def update_geo_router(self, geo_id, options={}):
    return self._request('PUT', 'accounts/%d/geo_routes/%s' % (self.account, geo_id), options)

  # number, zip, zip
  def update_numbers_geo_router(self, geo_id, locations=[]):
    commands = []
    for loc in locations:
      for number in loc['numbers']:
        command = ['create']
        command.append(number)
        command.append(loc['name'])
        commands.append(' '.join(command))
        command = ['mark']
        command.append(number)
        commands.append(' '.join(command))
        command = ['addzip']
        command.append(number)
        for zip in loc['zips']:
          command.append(zip)
        commands.append(' '.join(command))

    if len(commands) > 0:
      commands.append('purge remove')

    return self._request('UPLOAD', 'accounts/%d/geo_routes/%s/batch' % (self.account, geo_id), "\n".join(commands))
