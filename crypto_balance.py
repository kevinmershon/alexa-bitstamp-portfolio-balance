#!/usr/bin/env python2

# CONFIGURE THESE AS DESIRED
client_id = "CLIENT_ID"
pairs    = [
  {"name": "Bitcoin",      "ticker": "btcusd"},
  {"name": "Ethereum",     "ticker": "ethusd"},
  {"name": "Bitcoin Cash", "ticker": "bchusd"},
  {"name": "Ripple",       "ticker": "xrpusd"}
]
api_keys = {
  "btcusd": {"api_key": "API_KEY", "api_secret": "API_SECRET"},
  "ethusd": {"api_key": "API_KEY", "api_secret": "API_SECRET"},
  "bchusd": {"api_key": "API_KEY", "api_secret": "API_SECRET"},
  "xrpusd": {"api_key": "API_KEY", "api_secret": "API_SECRET"}
}

################################################################################

import threading
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import uuid
import datetime

from pyalgotrade.bitstamp import httpclient
from urllib import urlopen
import json

# function for getting Bitstamp balance for the specified account
def get_balance(pair, api_key, api_secret):
  cli = httpclient.HTTPClient(client_id, api_key.encode(), api_secret.encode())
  url = "https://www.bitstamp.net/api/v2/balance/" + pair + "/"
  jsonResponse = cli._post(url, {})
  return httpclient.AccountBalance(jsonResponse).getDict()

global summary

class BalanceUpdateThread(object):
  def __init__(self, interval=60):
    self.interval = interval

    thread = threading.Thread(target=self.run, args=())
    thread.daemon = True
    thread.start()

  def run(self):
    while True:
      # use CryptoWatch to read each coin's price data
      balance = 0.0
      responses = []
      for pair in pairs:
        url = "https://api.cryptowat.ch/markets/bitstamp/" + pair["ticker"] + "/summary"
        response = urlopen(url)
        response_body = response.read().decode('utf-8')
        response_json = json.loads(response_body)

        price = response_json["result"]["price"]
        responses.append("%s is currently $%.2f." % (pair["name"], price["last"]))

        # Use API credentials to get the current balance info
        api_credentials = api_keys[pair["ticker"]]
        results = get_balance(pair["ticker"], api_credentials["api_key"], api_credentials["api_secret"])
        usd_balance = float(results["usd_balance"])
        coin_balance = float(results[str(pair["ticker"][0:3] + "_balance")])
        balance = balance + usd_balance + (float(price["last"]) * coin_balance)

      global summary
      summary = "Your crypto portfolio is currently valued at $%.2f." % balance
      print(summary)
      time.sleep(self.interval)

class S(BaseHTTPRequestHandler):
  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()

  def do_GET(self):
    self._set_headers()

    global summary
    body_data = {
      "uid": str(uuid.uuid4()),
      "updateDate": str(datetime.datetime.now().replace(microsecond=0).isoformat())+".0Z",
      "titleText": "Bitstamp Portfolio",
      "mainText": summary
    }
    self.wfile.write(json.dumps(body_data))

  def do_HEAD(self):
    self._set_headers()

def run(server_class=HTTPServer, handler_class=S, port=8081):
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  background = BalanceUpdateThread()
  print 'Starting httpd...'
  httpd.serve_forever()

if __name__ == "__main__":
  from sys import argv

  if len(argv) == 2:
    run(port=int(argv[1]))
  else:
    run()
