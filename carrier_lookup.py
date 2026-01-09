#!/usr/bin/env python3
"""
Carrier Lookup using Ytel API
Reads phone numbers from phone_numbers.csv and appends carrier lookup data
"""

import csv
import requests
import time
import os
from urllib.parse import quote
from dotenv import load_dotenv
from pathlib import Path

# Load API key from .env.ytel
API_KEY = None
try:
    with open('.env.ytel', 'r') as f:
        API_KEY = f.readline().strip()
except FileNotFoundError:
    print("ERROR: .env.ytel file not found")
    exit(1)

if not API_KEY:
    print("ERROR: API key is empty in .env.ytel")
    exit(1)

# API Configuration
API_BASE_URL = "https://api.ytel.com/api/v4/carrier/lookup"
RATE_LIMIT = 10  # Transactions per second
DELAY = 1.0 / RATE_LIMIT  # Delay between requests

def lookup_carrier(phone_number):
    """
    Query Ytel API for carrier information
    
    Args:
        phone_number: E.164 format phone number (e.g., +12125551234)
    
    Returns:
        dict: API response data or error information
    """
    try:
        # URL encode the phone number (keeps the + as %2B)
        phone_encoded = quote(phone_number, safe='')
        
        # Build URL with phone number in path
        url = f"{API_BASE_URL}/{phone_encoded}"
        
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            response_data = response.json()
            return {'success': True, 'data': response_data, 'raw_response': response_data}
        else:
            return {
                'success': False, 
                'error': f"HTTP {response.status_code}",
                'message': response.text
            }
    
    except requests.exceptions.Timeout:
        return {'success': False, 'error': 'Timeout'}
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': str(e)}

def main():
    """Main execution function"""
    
    print("=" * 60)
    print("Ytel Carrier Lookup")
    print("=" * 60)
    print(f"Rate Limit: {RATE_LIMIT} requests/second")
    print(f"Delay between requests: {DELAY:.3f} seconds")
    print()
    
    # Read input CSV
    input_file = 'phone_numbers.csv'
    output_file = 'phone_numbers_with_carrier.csv'
    
    if not Path(input_file).exists():
        print(f"ERROR: {input_file} not found!")
        return
    
    phone_numbers = []
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        phone_numbers = [row['phone_number'] for row in reader]
    
    print(f"Loaded {len(phone_numbers)} phone numbers from {input_file}")
    print()
    
    # Process each phone number
    results = []
    
    for idx, phone in enumerate(phone_numbers, 1):
        print(f"[{idx}/{len(phone_numbers)}] Processing {phone}...", end=' ')
        
        result = lookup_carrier(phone)
        
        if result['success']:
            data = result['data']
            print("✓ Success")
            
            # Extract carrier info from response
            carrier_data = {}
            if isinstance(data, dict):
                # Check if API returned success with payload
                if data.get('status') is True and 'payload' in data:
                    payload = data.get('payload', [])
                    if payload and len(payload) > 0:
                        carrier_data = payload[0]
                # Or if there's an error
                elif data.get('status') is False:
                    carrier_data = {'error': data.get('error', [])}
            
            results.append({
                'phone_number': phone,
                'success': 'True' if carrier_data.get('status', False) else 'False',
                'carrier': carrier_data.get('network', carrier_data.get('company', '')),
                'line_type': 'wireless' if carrier_data.get('wireless') else 'landline',
                'city': carrier_data.get('city', ''),
                'state': carrier_data.get('state', ''),
                'zip_code': carrier_data.get('zipCode', ''),
                'country': carrier_data.get('country', ''),
                'raw_response': str(data),
                'error': str(carrier_data.get('error', '')) if 'error' in carrier_data else ''
            })
        else:
            print(f"✗ Failed: {result.get('error', 'Unknown error')}")
            results.append({
                'phone_number': phone,
                'success': 'False',
                'carrier': '',
                'line_type': '',
                'city': '',
                'state': '',
                'zip_code': '',
                'country': '',
                'raw_response': result.get('message', ''),
                'error': result.get('error', 'Unknown error')
            })
        
        # Rate limiting
        if idx < len(phone_numbers):
            time.sleep(DELAY)
    
    # Write results to output CSV
    print()
    print(f"Writing results to {output_file}...")
    
    fieldnames = [
        'phone_number', 'success', 'carrier', 'line_type', 'city', 'state', 
        'zip_code', 'country', 'raw_response', 'error'
    ]
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    # Summary
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    successful = sum(1 for r in results if r['success'] == 'True')
    failed = len(results) - successful
    print(f"Total processed: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Output file: {output_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()
