########################################################################################
# Author: Romba 
# Date: 04/05/2024
# Comment: Main orchestration script.
########################################################################################

import subprocess

def main():
    try:
        # Execute Extraction script
        subprocess.run(["python3", "scripts/habyt_01_raw_unit_listing.py"])
    except subprocess.CalledProcessError as e:
        print(f"Error running the script habyt_01_raw_unit_listing.py: {e}")
    
    try:
        # Execute Transformation script
        subprocess.run(["python3", "scripts/habyt_02_curated_sellable_object.py"])
    except subprocess.CalledProcessError as e:
        print(f"Error running the script habyt_02_curated_sellable_object.py: {e}")

if __name__ == "__main__":
    main()
