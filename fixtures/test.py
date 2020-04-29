import json

with open('living_prices/london.json') as f:    
    data = json.load(f)
print(type(data), data)