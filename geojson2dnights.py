import json
import pandas as pd

# Function to extract DNIGHT entries from GeoJSON
def extract_dnights(geojson_file, output_excel_file):
    # Read the GeoJSON file
    with open(geojson_file, 'r') as f:
        data = json.load(f)

    # List to hold DNIGHT entries
    dnights = []

    # Iterate over features and extract DNIGHT
    for feature in data['features']:
        dnight = feature['properties'].get('DNIGHT')
        if dnight:
            dnights.append({
                'DNIGHT': dnight,
                'SITE_NAME': feature['properties'].get('SITE_NAME'),
                'NPS_UNIT': feature['properties'].get('NPS_UNIT'),
                'ELEVATION': feature['properties'].get('ELEVATION'),
                'MID_DATE_LMT': feature['properties'].get('MID_DATE_LMT'),
                'MID_TIME_LMT': feature['properties'].get('MID_TIME_LMT'),
            })

    # Create a DataFrame from the list
    df = pd.DataFrame(dnights)

    # Output to Excel
    df.to_excel(output_excel_file, index=False)

# Example usage
geojson_file = 'C:/Users/lhung/Research/NPMaps/nsdmap.geojson'  # Replace with your GeoJSON file path
output_excel_file = 'C:/Users/lhung/Research/output_dnights.xlsx'   # Output Excel file name
extract_dnights(geojson_file, output_excel_file)

print(f"DNIGHT entries have been extracted to {output_excel_file}.")