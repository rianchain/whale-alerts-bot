import requests
import json

chain_id = 11155420
client_id = "9e33a4cef6d76467bc53fdd1f491213a"
wallet_address = "0x6482f9C2E181F21Ebafc6f7070462BFdBf34C50B"
limit = 1
sort_by = "block_number"
sort_order = "desc"

transactions_url = f"https://{chain_id}.insight.thirdweb.com/v1/transactions?limit={limit}&clientId={client_id}&sort_by={sort_by}&sort_order={sort_order}"

# https://1.insight.thirdweb.com/v1/transactions?limit=5&clientId=9e33a4cef6d76467bc53fdd1f491213a

def fetch_data(url):
    response = requests.get(url)
    return response.json()


transactions = fetch_data(transactions_url)
if transactions:
    print(json.dumps(transactions, indent=4))