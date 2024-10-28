import requests
import json
import time

"""r = requests.get('http://127.0.0.1:5000/home/toilet/window')
print(r.json())

r = requests.post('http://127.0.0.1:5000/home/toilet/window', json={'status': 'open'})
print(r.json())

r = requests.get('http://127.0.0.1:5000/home/toilet/window')
print(r.json())"""

r = requests.post('http://192.168.178.125:5000/home/toilet/window', json={'status': 'open'})
print(r.json())
