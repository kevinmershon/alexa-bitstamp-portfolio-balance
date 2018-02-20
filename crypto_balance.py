#!/usr/bin/env python2
import os

# Configure in AWS LAMBDA settings or system environment
client_id = os.environ["client_id"]
pairs    = [
  {"name": "Bitcoin",      "ticker": "btcusd"},
  {"name": "Ethereum",     "ticker": "ethusd"},
  {"name": "Bitcoin Cash", "ticker": "bchusd"},
  {"name": "Ripple",       "ticker": "xrpusd"}
]
api_keys = {
  "btcusd": {"api_key": os.environ["btc_api_key"], "api_secret": os.environ["btc_api_secret"]},
  "ethusd": {"api_key": os.environ["eth_api_key"], "api_secret": os.environ["eth_api_secret"]},
  "bchusd": {"api_key": os.environ["bch_api_key"], "api_secret": os.environ["bch_api_secret"]},
  "xrpusd": {"api_key": os.environ["xrp_api_key"], "api_secret": os.environ["xrp_api_secret"]}
}

################################################################################

import uuid
import datetime
import threading

from pyalgotrade.bitstamp import httpclient
from urllib import urlopen
import json


# use CryptoWatch to read each coin's price data
class priceThread(object):
  def __init__(self, pair):
    self.pair = pair
    self.thread = threading.Thread(target=self.run, args=())
    self.thread.daemon = True
    self.thread.start()
  def run(self):
    pair = self.pair

    url = "https://api.cryptowat.ch/markets/bitstamp/" + pair["ticker"] + "/summary"
    response = urlopen(url)
    response_body = response.read().decode('utf-8')
    response_json = json.loads(response_body)

    self.price = response_json["result"]["price"]
    self.response = "%s is currently $%.2f." % (pair["name"], self.price["last"])
  def join(self):
    self.thread.join()


# Use API credentials to get the current balance info
class balanceThread(object):
  def __init__(self, pair):
    self.pair = pair
    self.thread = threading.Thread(target=self.run, args=())
    self.thread.daemon = True
    self.thread.start()

  # function for getting Bitstamp balance for the specified account
  def get_balance(self, pair, api_key, api_secret):
    cli = httpclient.HTTPClient(client_id, api_key.encode(), api_secret.encode())
    url = "https://www.bitstamp.net/api/v2/balance/" + pair + "/"
    jsonResponse = cli._post(url, {})
    return httpclient.AccountBalance(jsonResponse).getDict()

  def run(self):
    pair = self.pair

    api_credentials = api_keys[pair["ticker"]]
    results = self.get_balance(pair["ticker"], api_credentials["api_key"], api_credentials["api_secret"])

    self.usd_balance = float(results["usd_balance"])
    self.coin_balance = float(results[str(pair["ticker"][0:3] + "_balance")])
  def join(self):
    self.thread.join()


def lambda_fn(event, context):
  threads = []
  # kickoff background price and balance threads concurrently
  for pair in pairs:
    threads.append({
      "pt": priceThread(pair),
      "bt": balanceThread(pair)
    })

  # collect price and balance information
  balance = 0.0
  for x in threads:
    pt = x["pt"]
    bt = x["bt"]
    pt.join()
    bt.join()

    balance = balance + bt.usd_balance + (float(pt.price["last"]) * bt.coin_balance)

  # prepare summary
  summary = "Your crypto portfolio is currently valued at $%.2f." % balance

  # format results for Lambda
  return {
    "statusCode": 200,
    "body": json.dumps({
        "uid": str(uuid.uuid4()),
        "updateDate": str(datetime.datetime.now().replace(microsecond=0).isoformat())+".0Z",
        "titleText": "Bitstamp Portfolio",
        "mainText": summary
    }),
    "headers": {
      "content-type": "application/json"
    },
    "isBase64Encoded": False
  }
