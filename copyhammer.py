#------------------------------------------------------------------------------#
#copyhammer.py
#
#NPS Night Skies Program
#
#This script copies and resizes the selected reference Hammer images from the 
#graphics folder to prepare for the NPMaps update. The graphic folder is copied 
#directly from the processing computer.
#
#Input: 
#   (1) Graphics libruary (copied from the processing computer N:\Graphics)
#   (2) Excel database exported from the access database
#
#Output:
#   (1) Reference full resolution and artificial-only images
#   (2) Full resolution images resized to a quarter and 1/10th
#   (3) Artificial-only images resized to a quarter
#
#History:
#	Li-Wei Hung -- Created 
#
#------------------------------------------------------------------------------#
import pandas as pd
import shutil

from PIL import Image

#------------------------------------------------------------------------------#
#Data nights where the images need to be copied
dnight_update = ["BALM240508_2","CEBR230715_1","CEBR230716_1","GRCA151014",
"GRCA250206","GRCA250219","GRCA250225","GRCA250227","GUIS221020","GUIS221022A",
"GUIS221022B","GUIS221022C","GUIS230316","GUIS231211","GUIS240502","HTSP250124",
"PICE170330","PNMM170923","PNMM170923A","SHNF170822","SUCR050313","USFW221021",
"USFW231211","UTMO240430","UTMO240908","ZION170919"]

#Graphics libruary copied from the processing computer
graphics = "D:/Graphics/"

#Excel database location
database = "../2025_update/NPMaps.xlsx"

#Output folder
outfolder = "../2025_update/GraphicsWeb/"

#------------------------------------------------------------------------------#
#Read in the database
nsData = pd.read_excel(database)
df = nsData.set_index("DNIGHT")

#Copy and resize images
for i in dnight_update:
    
    try:
        #Copy the reference full-resolution and artificial-only images
        shutil.copy2(graphics+df["FULLPATH"][i],outfolder+i+"_hmrFull.jpg")
        shutil.copy2(graphics+df["ARTPATH"][i],outfolder+i+"_hmrArt.jpg")
        
        full = Image.open(outfolder+i+"_hmrFull.jpg")
        art = Image.open(outfolder+i+"_hmrArt.jpg")
        
        #Resize images to 1/10th the size for popup
        size_p = (720,260)
        full_p = full.resize(size_p)
        full_p.save(outfolder+i+"_hmrFULLp.jpg", optimize=True, quality=95)
        
        #Resize images to a quarter size for display in the detailed report
        size_s = (1800,605)
        full_s = full.resize(size_s)
        full_s.save(outfolder+i+"_hmrFulls.jpg", optimize=True, quality=95)
        art_s = art.resize(size_s)
        art_s.save(outfolder+i+"_hmrArts.jpg", optimize=True, quality=95)
                
        print("Copied and resized reference images for", i)
        
        
    except FileNotFoundError:
        print("File Not Found Error", i)