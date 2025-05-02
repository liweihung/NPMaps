#------------------------------------------------------------------------------#
#fisheyepopup.py
#
#NPS Night Skies Program
#
#This script processes fisheye images by opening each JPEG file, converting it 
#to an RGBA format to support transparency, and creating a circular mask to crop
#the image into a circular shape. It adds extra vertical space for text, draws 
#a filled white circle in the center of a grayscale mask, and pastes the 
#original image onto a new transparent background using this mask. The resulting 
#image is then resized to half its original dimensions, and a year extracted 
#from the filename is added as text on top of the image. Finally, the processed 
#image is saved as a PNG file in an output folder, preserving its transparency.
#
#Input: 
#   (1) fisheye images from the CCD processing output
#
#Output:
#   (1) small fisheye images with transparent background
#
#History:
#	Li-Wei Hung -- Created 
#
#------------------------------------------------------------------------------#
import glob
import os,sys
import re

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

#------------------------------------------------------------------------------#

#Input folder that contains fisheye images from the processing computer
FisheyeCCD = "../2025_update/FisheyeCCD/"

#Output folder
outfolder = "../2025_update/FisheyeWeb_year/"

#------------------------------------------------------------------------------#

for i in glob.glob(FisheyeCCD+"*.jpg"):
    
    # Convert the image to RGBA to support transparency
    image = Image.open(i).convert("RGBA")
    
    # Create a new image with the same size and a transparent background
    width, height = image.size
    extra_space = 300
    height += extra_space
    mask_image = Image.new("L", (width, height), 0)  # Create a grayscale mask
    
    # Create a draw object
    draw = ImageDraw.Draw(mask_image)
    
    # Define the center and radius for the circular mask
    center = (width // 2, height // 2 + extra_space // 2)
    radius = 730
    
    # Draw a filled circle (white) in the center of the mask
    draw.ellipse(
        [(center[0] - radius, center[1] - radius), 
         (center[0] + radius, center[1] + radius)],
         fill=255  # White circle (opaque)
    )
    
    # Create a new image for the result
    new_image = Image.new("RGBA", (width, height))
    result_image = Image.new("RGBA", (width, height))
    
    # Paste the original image onto the result image using the mask
    new_image.paste(image, (0,extra_space))
    result_image.paste(new_image, None, mask_image)
    
    # Resize image
    image = result_image.resize((width // 2, height // 2))
    
    # Add text to the image
    draw = ImageDraw.Draw(image)
    
    # Define the text and position
    text = '20' + re.search(r'\d{2}', Path(i).name).group()
    text_position = (240, 20)  # Change this to your desired position
    #text_position = (0, 0)  # Change this to your desired position
    #text_position = (600, 0)  # Change this to your desired position

    # Optionally, load a font
    # font = ImageFont.truetype("arial.ttf", size=40)  # Specify the font and size
    #font = ImageFont.load_default(size=60)  # Use default font
    font = ImageFont.load_default(size=130)  # Use default font
    
    # Add text to the image
    draw.text(text_position, text, fill="white", font=font)  # Change fill color as needed

    # Save the result as a PNG image to retain transparency
    file_name = os.path.splitext(os.path.basename(i))[0] + ".png"
    image.save(outfolder+file_name)
    
    

