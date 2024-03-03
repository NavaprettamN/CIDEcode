from django.http import HttpResponse
from django.shortcuts import render
import joblib
from supabase_py import create_client
import requests
import pprint
import re
import time
# import os


supabase_url = 'https://hotqztzexkqnxtrfeany.supabase.co'
supabase_api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhvdHF6dHpleGtxbnh0cmZlYW55Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDkzNTcyMzcsImV4cCI6MjAyNDkzMzIzN30.nWHwuaAN69VPLGOwaGUqQWVDed85anHx0xB-CE30y78'
supabase = create_client(supabase_url, supabase_api_key)

# view for transaction block {txid -> txid, vin, vout, addresses, bin, bout, (check illicit)->/illicit/txid}

def transaction_page(request):
    # print(request.GET == {})
    if request.GET != {}:
        # here do the checking of txid (api call -> store data -> data to model -> value of risk)
        txid = request.GET['txid']
        txid_data = get_transaction_data(txid)
        time.sleep(5)
        # print(txid_data)
        if(txid_data):
            vin, vout = txid_data['vin_sz'], txid_data['vout_sz']
            # print(vin, vout)
            sender_adresses = []
            receiver_addresses = []
            for i in txid_data['inputs']:
                sender_adresses.append(i['prev_out']['addr'])
            for i in txid_data['out']:
                receiver_addresses.append(i['addr'])
            bin,bout=0,0
            for i in txid_data['inputs']:
                bin += i['prev_out']['value']
                bin /= 100000
            for i in txid_data['out']:
                bout += i['value']
                bout /= 100000
            
        n = 0
        # for i in sender_adresses:
        #     m=get_single_address_data(i)
        #     n+=m['n_tx']
        # total_sent = 0
        # for i in sender_adresses:
        #     ts=get_single_address_data(i)
        #     total_sent+=m['total_sent']
        n = vin + vout
        data_api = get_sender_data(txid)
        print(type(data_api))
        data_api*=61990
        print(n, data_api)
        exchange_model = joblib.load('exchange_v001.sav')
        x = exchange_model.predict([[vin, vout, bin, bout, n, data_api]])[0]
        # print(x)
        return render(request, "transaction.html", {'txid': txid,'vin': vin, 'vout': vout, 'bin': bin, 'bout': bout, 'sender_addresses': sender_adresses, 'receiver_addresses': receiver_addresses, 'exchange': x})
    return render(request, "transaction.html")

# illicit page view

def illicit_page(request):
    if request.GET != {}:
        # here do the checking of txid (api call -> store data -> data to model -> value of risk)
        txid = request.GET['txid']
        txid_data = get_transaction_data(txid)
        vin, vout = txid_data['vin_sz'], txid_data['vout_sz']
        # print(type(txid_data['inputs']))
        bin,bout=0,0
        for i in txid_data['inputs']:
            bin += i['prev_out']['value']
            bin /= 100000
        for i in txid_data['out']:
            bout += i['value']
            bout /= 100000

        model = joblib.load('illicit_model_v001.sav')

        model_result = int(model.predict([[vin, vout, bin, bout]])[0])
        print(model_result, vin, vout)
        # supabase txid, vin, vout, bin, bout, 
        data, count = supabase.table('illicit').insert({"tx_id": txid, "vin": vin, "vout": vout, "bin": bin, "bout": bout, "illicit": model_result}).execute()
        # print(data[0], count)
        return render(request, "illicit.html", {'txid': txid, 'vin': vin, 'vout': vout, 'bin': bin, 'bout': bout, 'illicit': model_result})

    return render(request, "illicit.html")


# view for mixer

def mixer_page(request):
    if request.GET != {}:
        txid = request.GET['txid']
        txid_data = get_transaction_data(txid)
        vin, vout = txid_data['vin_sz'], txid_data['vout_sz']
        bin,bout=0,0
        for i in txid_data['inputs']:
            bin += i['prev_out']['value']
            bin /= 100000
        for i in txid_data['out']:
            bout += i['value']
            bout /= 100000
        model = joblib.load('mixer_model_v002.sav')
        anomalous = model.predict([[vin, vout, bin, bout]])
        print(anomalous)
        return render(request, "mixer.html", {'anomalous':anomalous, 'vin': vin, 'vout': vout})
    return render(request, "mixer.html")

# overall model {txid/block_hash/wallet_hash -> }

def overall_analaysis_page(request):
    if request.GET != {}:
        hash = request.GET['hash']
        bitcoin_address_pattern = re.compile(r'^[a-km-zA-HJ-NP-Z1-9]*$')
        block_hash_pattern = re.compile(r'^0000000[0-9a-fA-F]*$')
        transaction_hash_pattern = re.compile(r'^[0-9a-f]*$')
        
        # wallet addresss
        if  bitcoin_address_pattern.match(hash):
            print("It is a wallet address", hash)
            data = get_balance_data(hash)
            if(data):
                n_tx = data['n_tx']
                total_sent = data['total_sent']
                total_received = data['total_received']
                balance = data['final_balance']
                return render(request, 'overall.html', {'val': 3, 'balance': balance, 'n_tx': n_tx, 'total_received': total_received, 'total_sent': total_sent})
            else: return render(request, 'overall.html')
        
        # block hash
        elif block_hash_pattern.match(hash):
            print("it is a block hash", hash)
            data = get_block_data(hash)
            if data:
                n_tx = data['n_tx']
                three_transactions = []
                for i in range(8):
                    three_transactions.append(data['tx'][i]['hash'])
                return render(request, 'overall.html', {'val':2,'n_tx': n_tx, 'three_transactions':three_transactions})
            else: return render(request, 'overall.html')
        
        # transaction hash
        elif transaction_hash_pattern.match(hash):
            data = get_transaction_data(hash)
            if data:
                vin, vout = data['vin_sz'], data['vout_sz']
                sender_adresses = []
                receiver_addresses = []
                for i in data['inputs']:
                    sender_adresses.append(i['prev_out']['addr'])
                for i in data['out']:
                    receiver_addresses.append(i['addr'])
                bin,bout=0,0
                for i in data['inputs']:
                    bin += i['prev_out']['value']
                    bin /= 100000
                for i in data['out']:
                    bout += i['value']
                    bout /= 100000
                print("it is a txhash", hash)
                return render(request, "overall.html", {'val':1, 'bin': bin, 'bout': bout, 'sender_addresses': sender_adresses, 'receiver_addresses': receiver_addresses})
            else: return render(request, "overall.html")
        
        else:
            return render(request, 'overall.html', {'val': 4})
    else:
        return render(request, 'overall.html', {})



# block hash api

def get_block_data(block_hash):
    api_url = f'https://blockchain.info/rawblock/{block_hash}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        block_data = response.json()
        return block_data
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

# transaction api

def get_transaction_data(transaction_hash):
    api_url = f'https://blockchain.info/rawtx/{transaction_hash}'
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  
        transaction_data = response.json()
        return transaction_data

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

# balance api

def get_balance_data(wallet_address):
    api_url = f'https://blockchain.info/rawaddr/{wallet_address}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        balance_data = response.json()
        return balance_data
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

# this is the other api calls from cryptoapis : 

# get balance data

def index(request):
    response0 = supabase.table('illicit').select("*").eq('illicit', '0').execute()
    response1 = supabase.table('illicit').select("*").eq('illicit', '1').execute()
    return render(request, "index.html", {"licit": len(response0['data']), "illicit": len(response1['data'])})

def get_single_address_data(addr):
    api_url = f'https://blockchain.info/rawaddr/{addr}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")
# this is the other api calls from cryptoapis : 

def get_sender_data(hash):
    url = "https://rest.cryptoapis.io/blockchain-data/bitcoin/testnet/transactions/4b66461bf88b61e1e4326356534c135129defb504c7acb2fd6c92697d79eb250"
    querystring = {"context": "yourExampleString"}
    headers = {
        'Content-Type': 'application/json',
        'X-API-Key': '4b72fd58075695ceeb3887be8073d346a17f1618'
    }
    add = 0
    response = requests.get(url, headers=headers, params=querystring)
    # response.raise_for_status()
    res = response.json()
    print(res)
    for i in res['data']['item']['recipients']:
        add += float(i['amount'])

    return add

# get balance data

def index(request):
    req_headers = request.META
    x_forwarded_for_value = req_headers.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for_value:
        ip_addr = x_forwarded_for_value.split(',')[-1].strip()
    else:
        ip_addr = req_headers.get('REMOTE_ADDR')
    print(ip_addr)
    response0 = supabase.table('illicit').select("*").eq('illicit', '0').execute()
    response1 = supabase.table('illicit').select("*").eq('illicit', '1').execute()
    return render(request, "index.html", {"licit": len(response0['data']), "illicit": len(response1['data']), "ip_addr": ip_addr})
    # return render(request, "index.html", {"licit": len(response0['data']), "illicit": len(response1['data'])})