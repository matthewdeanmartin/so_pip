"""
Module wide setup work
"""
import os

from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("key", None):
    print(
        "No key could be found, go register one with "
        "https://stackapps.com/apps/oauth/register Then "
        "put in in a .env file or `export key=(secret_key)`"
    )
    print("Application will attempt to run, but odds are good you will get throttled.")
    print()
