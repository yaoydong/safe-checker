import random
import time


from eth_account import Account
import requests
import pandas as pd
import json
from web3 import Web3
import certifi




end_point = ''
apikey = ''



def loadaccounts(filename):
    accounts = []
    try:
        txt_file = open(filename, "r")
        accounts = txt_file.read().splitlines()
        txt_file.close()
        for i in range(len(accounts)):
            if accounts[i].count('\t') > 0:
                accounts[i] = accounts[i].replace('\t', ' ')
    except Exception as e:
        print('load error', e)
        txt_file.close()
    finally:
        return accounts

def getcreator(addr):
    url = 'https://api.etherscan.io/api?module=contract&action=getcontractcreation&contractaddresses=' + addr + '&apikey=' + apikey
    response = requests.get(url, verify=certifi.where())
    creator = response.json()['result'][0]['contractCreator']
    return creator

def gettxsandexeced(addr):
    exec_list = []
    exec_times = []
    url = 'https://api.etherscan.io/api?module=account&action=txlist&address=' + addr + '&startblock=0&endblock=99999999&page=1&offset=0&sort=asc&apikey=' + apikey
    s = requests.get(url)
    txs = len(s.json()['result'])
    if txs > 10:
        return txs,exec_list,exec_times
    for j in range(txs):
        tx = s.json()['result'][j]
        if tx['functionName'].find('execTransaction') != -1:
            from_addr = tx['from']
            exec_time = tx['timeStamp']
            if from_addr not in exec_list:
                exec_list.append(from_addr)
            if exec_time not in exec_times:
                exec_times.append(exec_time)
    return txs,exec_list,exec_times

accs = loadaccounts('check.txt')
for x in range(len(accs)):
    safe = accs[x]
    creator = getcreator(safe)
    txs,exec_by,exec_time = gettxsandexeced(safe)
    print(safe,creator,txs,exec_by,exec_time)


