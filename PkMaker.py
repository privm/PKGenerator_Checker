#!/usr/bin/env python

import os
import ecdsa
import hashlib
import base58
import requests
from time import sleep



while True:
	pk = os.urandom(32).encode("hex")
	print pk
	sk = ecdsa.SigningKey.from_string(pk.decode("hex"), curve = ecdsa.SECP256k1)
	vk = sk.verifying_key
	publicKey = ("\04" + vk.to_string())
	ripemd160 = hashlib.new('ripemd160')
	ripemd160.update(hashlib.sha256(publicKey).digest())
	networkAppend = '\00' + ripemd160.digest()
	checksum = hashlib.sha256(hashlib.sha256(networkAppend).digest()).digest()[:4]
	binary_address = networkAppend + checksum
	publicAddress = base58.b58encode(binary_address)
	print publicAddress
	
# Main one is blockexplorer - seems to be UNLIMITED...using chain.so has a rate limiter
# https://blockexplorer.com/api/addr/
# https://chain.so/api/v2/get_address_balance/BTC/
# balance =  pmts['data']['confirmed_balance']
	req = requests.get("https://blockexplorer.com/api/addr/"+publicAddress)
	pmts = req.json()
	balance =  pmts['balance']
	print balance
	

# msg = "I own your Private Key for %s" %(publicAddress)
# signed_msg = sk.sign(msg)
# encoded_msg = signed_msg.encode("hex")