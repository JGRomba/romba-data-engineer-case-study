########################################################################################
# Author: Romba 
# Date: 04/05/2024
# Comment: Script for generating the sellable objects entities.
########################################################################################

print("########################################################################################")

import os
import json
from datetime import datetime

# Raw and Curated folder path
raw_folder = 'schema/raw'
curated_folder = 'schema/curated'

print("Starting transformation process for sellable objects")
try:
    # Get list of raw files
    raw_files = [file for file in os.listdir(raw_folder) if file.startswith("unit_listing")]

    # Verify the presence of raw data
    if not raw_files:
        print("No files found in the raw folder")
        exit()

    # Find the most recent file based on the timestamp in the filename
    latest_timestamp = max([int(file.split("_")[-1].split(".")[0]) for file in raw_files])
    latest_file = [file for file in raw_files if str(latest_timestamp) in file][0]
    latest_file_path = os.path.join(raw_folder, latest_file)

    print(f"Using JSON data from {latest_file_path}")

    # Load JSON data from the latest file
    with open(latest_file_path) as f:
        data = json.load(f)

except FileNotFoundError:
    print("No files found in the raw folder")
    exit()

except Exception as e:
    print(f"Error using JSON data: {str(e)}")
    exit()

# Define entities and align fields
units = []
property = []
prices = []
concessions = []
fees = []

# Initialize a set to keep track of propertyIds
seen_property_ids = set()

for item in data:
    # Extract data for Unit entity
    unitId = item.get('id')
    propertyId = item.get('propertyId')
    fullAddress = item.get('address', {}).get('fullAddress')
    roomNumber = item.get('address', {}).get('roomNumber')
    occupancyType = item.get('occupancyType')
    description = item.get('description')
    listingSqft = item.get('listingSqft')
    unitSqft = item.get('unitSqft')
    currencyCode = item.get('currencyCode')
    minimum_price = item.get('pricing', {}).get('minimumPrice')
    maximum_price = item.get('pricing', {}).get('maximumPrice')
    minimum_stay = item.get('pricing', {}).get('minimumStay')
    units.append({
        "unitId": unitId,
        "propertyId": propertyId,
        "fullAddress": fullAddress,
        "roomNumber": roomNumber,
        "occupancyType": occupancyType,
        "description": description,
        "unitSqft": unitSqft,
        "listingSqft": listingSqft,
        "currencyCode": currencyCode,
        "minimum_price": minimum_price,
        "maximum_price": maximum_price,
        "minimum_stay": minimum_stay
    })

    # Extract data for Property entity
    propertyId = item.get('propertyId')

    # Check if propertyId is already seen, if so, skip this item
    if propertyId in seen_property_ids:
        continue

    propertyName = item.get('propertyName')
    marketingName = item.get('marketingName')
    streetAddress = item.get('address', {}).get('streetAddress')
    city = item.get('address', {}).get('city')
    stateCode = item.get('address', {}).get('stateCode')
    postalCode = item.get('address', {}).get('postalCode')
    countryCode = item.get('address', {}).get('countryCode')
    latitude = item.get('address', {}).get('latitude')
    longitude = item.get('address', {}).get('longitude')
    belongedCity = item.get('address', {}).get('belongedCity')
    neighborhood = item.get('neighborhood')
    neighborhoodDescription = item.get('neighborhoodDescription')
    bedrooms = item.get('bedrooms')

    # Add propertyId to seen set
    seen_property_ids.add(propertyId)

    property.append({
        "propertyId": propertyId,
        "propertyName": propertyName,
        "marketingName": marketingName,
        "streetAddress": streetAddress,
        "city": city,
        "stateCode": stateCode,
        "postalCode": postalCode,
        "countryCode": countryCode,
        "latitude": latitude,
        "longitude": longitude,
        "belongedCity": belongedCity,
        "neighborhood": neighborhood,
        "neighborhoodDescription": neighborhoodDescription,
        "bedrooms": bedrooms
    })

    # Extract data for Fee entity
    for fee in item.get('fees', []):
        fees.append({
            "feeId": len(fees) + 1,
            "unitId": unitId,
            "name": fee.get('name'),
            "description": fee.get('description'),
            "amount": fee.get('amount'),
            "isMandatory": fee.get('isMandatory'),
            "isRefundable": fee.get('isRefundable')
        })

    # Prepare data for Price and Concession entities
    pricing_data = item.get('pricing')
    monthly_pricing = pricing_data.get('monthlyPricing', [])

    # Initialize price_id
    price_id = len(prices) + 1

    # Extract data for Price entity
    for price in monthly_pricing:
        prices.append({
            "priceId": price_id,
            "unitId": unitId,
            "name": price.get('name'),
            "months": price.get('months'),
            "amount": price.get('amount')
        })

        # Extract data for Concession entity
        concession_descriptions = price.get('concessionsApplied', [])
        for concession_description in concession_descriptions:
            concessions.append({
                "concessionId": len(concessions) + 1,
                "priceId": price_id,
                "concessionDescription": concession_description
            })

        # Increment price_id for each price
        price_id += 1

# Create folder curated if it doesn't exist and delete existing files if the folder exists
if not os.path.exists(curated_folder):
    os.makedirs(curated_folder)
else:
    print("Deleting existing files in the curated folder...")
    files = os.listdir(curated_folder)
    for file in files:
        os.remove(os.path.join(curated_folder, file))
    print("Existing files deleted successfully")

print("Saving new entities as JSON files...")
try:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    with open(os.path.join(curated_folder, f'unit_{timestamp}.json'), 'w') as f:
        json.dump(units, f, indent=4)
    print("Unit file saved successfully")

    with open(os.path.join(curated_folder, f'property_{timestamp}.json'), 'w') as f:
        json.dump(property, f, indent=4)
    print("Property file saved successfully")

    with open(os.path.join(curated_folder, f'price_{timestamp}.json'), 'w') as f:
        json.dump(prices, f, indent=4)
    print("Price file saved successfully")

    with open(os.path.join(curated_folder, f'concession_{timestamp}.json'), 'w') as f:
        json.dump(concessions, f, indent=4)
    print("Concession file saved successfully")

    with open(os.path.join(curated_folder, f'fee_{timestamp}.json'), 'w') as f:
        json.dump(fees, f, indent=4)
    print("Fee file saved successfully")

    print("All entities saved successfully")
except Exception as e:
    print(f"Error saving entities: {str(e)}")
