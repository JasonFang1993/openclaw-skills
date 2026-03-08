#!/usr/bin/env python3
"""
Simple curl-cffi fetch wrapper.
"""
import sys
from curl_cffi import requests

def main():
    if len(sys.argv) < 2:
        print("Usage: fetch.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    r = requests.get(url)
    print(r.text)

if __name__ == "__main__":
    main()
