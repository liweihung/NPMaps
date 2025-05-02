#------------------------------------------------------------------------------#
#csv2gjson.py
#
#NPS Night Skies Program
#
#This script converts the input file in CSV UTF-8 formate to a geojson file.
#
#Input: 
#   (1) NPMapsQuery.csv
#
#Output:
#   (1) nsmap.geojson
#   (2) nsmap_%Y%d%m.geojson (copy)
#
#History:
#	Sharolyn Anderson -- Created 
#   Li-Wei Hung -- Cleaned and modified
#
#------------------------------------------------------------------------------#

import geojson
import pandas as pd
import shutil
from datetime import datetime

#------------------------------------------------------------------------------#
#	            	      Read in files and clean data          		       #
#------------------------------------------------------------------------------#

#File names and location
folder = "../2025_update/"
file = "NPMaps.csv"

#Load data from Excel or CSV
nsData = pd.read_csv(folder+file)

#Data clean up, replace NAN 
nsData = nsData.fillna(value=" ")

#Replace "\r\n" with ";" and clean up extra semicolons
nsData["OBSERVERS"] = nsData["OBSERVERS"].str.replace("\r\n", ";")
nsData["OBSERVERS"] = nsData["OBSERVERS"].str.replace(";;", ";").str.rstrip(";")

#Round latitude and longitude to 5 decimal places
numerical_cols = ["LONGITUDE", "LATITUDE"]
nsData[numerical_cols] = nsData[numerical_cols].round({"LONGITUDE": 5, "LATITUDE": 5})

print("data shape is: ", nsData.shape)

#------------------------------------------------------------------------------#
#	            	      Convert to GeoJSON format		         		       #
#------------------------------------------------------------------------------#

features = []
for _, row in nsData.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row["LONGITUDE"], row["LATITUDE"]]
        },
        "properties": row.drop(["LONGITUDE", "LATITUDE"]).to_dict()
    }

    features.append(feature)

geojson_data = {"type": "FeatureCollection", "features": features}

# Write GeoJSON to file
filename = f"nsdmap.geojson"
with open(folder+filename, "w") as f:
    geojson.dump(geojson_data, f, indent=4)

# Save a copy with time stamp    
filename_copy = f"nsdmap_{datetime.now().strftime('%Y%d%m')}.geojson"    
shutil.copy2(folder+filename, folder+filename_copy)

