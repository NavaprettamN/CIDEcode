from django.http import HttpResponse
from django.shortcuts import render
import joblib
from supabase_py import create_client
import requests
import pprint
import re
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
        # print(txid_data)
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
        return render(request, "transaction.html", {'txid': txid,'vin': vin, 'vout': vout, 'bin': bin, 'bout': bout, 'sender_addresses': sender_adresses, 'receiver_addresses': receiver_addresses})

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
        
        # print(bin, bout)

        # print(vin, vout)

        model = joblib.load('illicit_model_v001.sav')

        model_result = int(model.predict([[vin, vout, bin, bout]])[0])
        
        # data, count = supabase.table('illicit').insert({"tx_id": txid, "vin": vin, "vout": vout, "bin": bin, "bout": bout, "illicit": model_result}).execute()
        # supabase txid, vin, vout, bin, bout, 
        data, count = supabase.table('illicit').insert({"tx_id": txid, "vin": vin, "vout": vout, "bin": bin, "bout": bout, "illicit": model_result}).execute()
        # print(data[0], count)
        return render(request, "illicit.html", {'vin': vin, 'vout': vout, 'bin': bin, 'bout': bout, 'illicit': model_result})

    return render(request, "illicit.html")


# view for mixer

def mixer_page(request):
    if request.GET != {}:
        txid = request.GET['txid']
        txid_data = get_transaction_data(txid)

        return render(request, "mixer,html")


    return render(request, "mixer.html")

# overall model {txid/block_hash/wallet_hash -> }

def overall_analaysis_page(request):
    if request.GET != {}:
        hash = request.GET['hash']
        bitcoin_address_pattern = re.compile(r'^[13][a-km-zA-HJ-NP-Z1-9]*$')
        block_hash_pattern = re.compile(r'^0000000[0-9a-fA-F]*$')
        transaction_hash_pattern = re.compile(r'^[0-9a-f]*$')

        # wallet addresss
        if bitcoin_address_pattern.match(hash):
            print("it is a wallet address", hash)
            data = get_balance_data(hash)
            balance = data['final_balance']
            n_tx = data['n_tx']
            total_received = data['total_received']
            return render(request, 'overall.html', {'balance': balance, 'n_tx': n_tx, 'total_received': total_received})
        
        elif block_hash_pattern.match(hash):
            print("it is a block hash", hash)
            # data = 
        else:
            print("it is a txhash", hash)
        return render(request, 'overall.html')
    return render(request, 'overall.html')


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
        response.raise_for_status()  # Check for HTTP errors

        # If the request was successful, you can access the data using response.json()
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
    api_url = 'https://blockchain.info/balance?active={wallet_address}'
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

def crypto_get_balance_data(wallet_address):
    

def index(request):
    response0 = supabase.table('illicit').select("*").eq('illicit', '0').execute()
    response1 = supabase.table('illicit').select("*").eq('illicit', '1').execute()
    return render(request, "index.html", {"licit": len(response0['data']), "illicit": len(response1['data'])})
