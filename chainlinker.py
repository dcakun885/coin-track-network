"""
ChainLinker: нахождение связанных адресов в Bitcoin через входы/выходы транзакций.
"""

import requests
import argparse
from collections import defaultdict

def get_transaction_ids(address):
    url = f"https://api.blockchair.com/bitcoin/dashboards/address/{address}?transaction_details=true"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Не удалось получить транзакции.")
    return r.json()["data"][address]["transactions"][:10]

def get_transaction_io(txid):
    url = f"https://api.blockchair.com/bitcoin/raw/transaction/{txid}"
    r = requests.get(url)
    if r.status_code != 200:
        return [], []
    tx = r.json()["data"][txid]["decoded_raw_transaction"]
    inputs = []
    for vin in tx.get("vin", []):
        addr = vin.get("addresses", [])
        if addr:
            inputs.extend(addr)
    outputs = []
    for vout in tx.get("vout", []):
        addr = vout.get("script_pub_key", {}).get("addresses", [])
        if addr:
            outputs.extend(addr)
    return inputs, outputs

def analyze_links(address):
    txids = get_transaction_ids(address)
    linked_in = defaultdict(int)
    linked_out = defaultdict(int)

    for txid in txids:
        inputs, outputs = get_transaction_io(txid)
        if address in outputs:
            for addr in inputs:
                if addr != address:
                    linked_in[addr] += 1
        if address in inputs:
            for addr in outputs:
                if addr != address:
                    linked_out[addr] += 1

    print(f"🔍 Анализ цепочек адреса: {address}")
    print("\n⬅️ Получено от:")
    for addr, count in linked_in.items():
        print(f"  {addr} — {count} раз(а)")
    print("\n➡️ Отправлено на:")
    for addr, count in linked_out.items():
        print(f"  {addr} — {count} раз(а)")
    if not linked_in and not linked_out:
        print("❌ Нет обнаруженных связанных адресов (ограничение по 10 транзакциям).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ChainLinker — поиск связанных BTC-адресов.")
    parser.add_argument("address", help="Bitcoin-адрес")
    args = parser.parse_args()
    analyze_links(args.address)
