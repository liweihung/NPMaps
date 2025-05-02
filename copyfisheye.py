import shutil
import xlrd

#Excel database location
database = "./NPMaps.xlsx"

workbook = xlrd.open_workbook(database)
sheet = workbook.sheet_by_index(0)

# Create a dictionary to hold the data
ref = {}

# Iterate through the rows, skipping the header
for row_idx in range(1, sheet.nrows):
    row = sheet.row_values(row_idx)
    dnight = row[0]  # 'DNIGHT' is the first column
    dset = int(row[1])  # 'DSET' is the second column
    ref[dnight] = dset
    

#Data nights where the images need to be copied
dnight_update = ["BALM240508_2","CEBR230715_1","CEBR230716_1","GRCA151014",
"GRCA250206","GRCA250219","GRCA250225","GRCA250227","GUIS221020","GUIS221022A",
"GUIS221022B","GUIS221022C","GUIS230316","GUIS231211","GUIS240502","HTSP250124",
"PICE170330","SHNF170822","SUCR050313","USFW221021","USFW231211","UTMO240430",
"UTMO240908","ZION170919"]

for i in ref.keys():
    fisheye = "N:/Griddata/"+ i + "/S_0"+ str(ref[i]) +"/artificial.jpg"
    try: 
        shutil.copy2(fisheye,"../copied_fisheye_reference_artificial/"+i+".jpg")
    except:
        print fisheye


