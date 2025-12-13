import requests
import json

try:
    res = requests.get("http://localhost:8000/api/v1/recalls")
    data = res.json()
    
    print(f"Status: {res.status_code}")
    print(f"Count: {len(data)}")
    
    if len(data) > 0:
        print("First Item Keys:", data[0].keys())
        print("First Item ID:", data[0].get("id"))
        
        # Check for anomalies
        missing_ids = [d for d in data if d.get("id") is None]
        if missing_ids:
            print(f"WARNING: Found {len(missing_ids)} items with missing IDs!")
        else:
            print("ALL items have valid IDs.")
    else:
        print("No data found.")
        
except Exception as e:
    print(f"Error: {e}")
