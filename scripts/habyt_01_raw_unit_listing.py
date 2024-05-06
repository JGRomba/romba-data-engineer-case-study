########################################################################################
# Author: Romba 
# Date: 02/05/2024
# Comment: Script for extracting raw data from unit listings.
########################################################################################

print("########################################################################################")

import requests
import json
import os
from datetime import datetime

# API Endpoint
api_url = "https://www.common.com/cmn-api/listings/common"

# Raw Source Name
raw_source = "unit_listing"

# Generate current datetime
extraction_datetime = datetime.now().strftime("%Y%m%d%H%M%S")

# File destination folder (Raw folder)
raw_folder = 'schema/raw'

print(f"Starting extraction process for {raw_source}")
try:
    
    print("Sending API request...")

    # API request
    response = requests.get(api_url)

    # Check request status
    if response.status_code == 200:
        print("API request was successful")

        # Extract JSON data from response
        data = response.json()

        # Create folder if it doesn't exist
        if not os.path.exists(raw_folder):
            os.makedirs(raw_folder)

        # File path for JSON data
        file_path = f"{raw_folder}/{raw_source}_{extraction_datetime}.json"

        # Save JSON data to file
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

        print(f"Data sucessfully loaded in {file_path}")

    else:
        print("API request failed! Status code:", response.status_code)

except Exception as e:
    print("An error occurred:", str(e))
