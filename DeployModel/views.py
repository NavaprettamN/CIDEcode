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

def home(request):
    return render(request, "home.html")

def result(request):
    cls = joblib.load('finalise_model.sav')

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
    api_url = f'https://blockchain.info/rawblock/${block_hash}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        block_data = response.json()
        return block_data

    except:
        print("errors : ")
        return None
    

def get_block_data(block_hash):
    api_url = f'https://blockchain.info/rawblock/{block_hash}'
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Check for HTTP errors

        # If the request was successful, you can access the data using response.json()
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

def index(request):
    return render(request, "index.html")

# Replace 'your_block_hash' with the actual block hash you want to retrieve
# block_hash_to_get = '0000000000000bae09a7a393a8acded75aa67e46cb81f7acaa5ad94f9eacd103'
# block_data = get_block_data(block_hash_to_get)

# # Do something with the block_data
# pprint.pprint(block_data)

