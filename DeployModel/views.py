from django.http import HttpResponse
from django.shortcuts import render
import joblib
from supabase_py import create_client
import requests
import pprint
# import os


supabase_url = 'https://jbxwmefylhjinddezouk.supabase.co'
supabase_api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpieHdtZWZ5bGhqaW5kZGV6b3VrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDg1NzE5NjcsImV4cCI6MjAyNDE0Nzk2N30.-F5-r5UZDXUvSB-UawcQQxkHoo7E3qqnxrtRTxLM41Y'

supabase = create_client(supabase_url, supabase_api_key)

# view for transaction block

def transaction_page(request):
    print(request.GET == {})
    if request.GET != {}:
        # here do the checking of txid (api call -> store data -> data to model -> value of risk)
        print(request, "2nd one")
        txid = request.GET['txid']
        txid_data = get_transaction_data(txid)
        print(txid_data)
        vin, vout = txid_data['vin_sz'], txid_data['vout_sz']

        print(vin, vout)
        return render(request, "transaction.html", {'vin': vin, 'vout': vout})

    return render(request, "transaction.html")

def illicit_page(request):
    if request.GET != {}:
        # here do the checking of txid (api call -> store data -> data to model -> value of risk)
        print(request, "2nd one")
        txid = request.GET['txid']
        txid_data = get_transaction_data(txid)

        # vin, vout = txid_data['vin_sz'], txid_data['vout_sz']
        # print(type(txid_data['inputs']))
        bin,bout=0,0
        for i in txid_data['inputs']:
            bin += i['prev_out']['value']
            bin /= 100000
        for i in txid_data['out']:
            bout += i['value']
            bout /= 100000
        
        print(bin, bout)

        # print(vin, vout)

        model = joblib.load('illicit_model_v001.sav')

        model_result = model.predict([[4, 3, 4.939574, 5.788070]])[0]
        # print(model_result)

        # supabase txid, vin, vout, bin, bout, 
        return render(request, "illicit.html", {'vin': vin, 'vout': vout, 'illicit': model_result})

    return render(request, "illicit.html")





def result(request):
    cls = joblib.load('illicit_model_v001.sav')

    value_in_String = request.GET['txid']
    value_in_int = int(value_in_String)
    value_in_array = [float(value) for value in value_in_String.split(',')]
    print(value_in_int)
    response = supabase.table('mainTable').select("risk").eq('txid', value_in_String).execute()
    data = response['data']

    block_chain = blockApi(value_in_int)
    # Process the data as needed
    print(data)

    return render(request, "result.html", {'ans': data})


def blockApi(block_hash):
    api_url = f'https://blockchain.info/rawblock/{block_hash}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        block_data = response.json()
        return block_data

    except:
        print("errors : ")
        return None
    

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

def index(request):
    return render(request, "index.html")

def mixer_page(request):
    return render(request, "mixer.html")

