"""

SPRITE SHEET GENERATOR

Script by Vinterdragen
Based on @minzkraut script

IG: @Vinterdragen
Twitter: @Vinterdragen
ArtStation: www.artstation.com/simoncarmona

"""

"""Image manipulation library"""
from PIL import Image
import os, math

"""GUI library for the prompts"""
import tkinter
from tkinter import Tk, filedialog, simpledialog

root = Tk() # pointing root to Tk() to use it as Tk() in program.
root.withdraw() # Hides small tkinter window.
root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.


"""
Set up the maximum number of images per row
Keep it even if you care about mipmaps in your engine

"""
max_frames_row = 8.0 


frames = []
tile_width = 0
tile_height = 0


"""
Prompts the folder selection
"""
myDir = filedialog.askdirectory() # Returns opened path as str

print(myDir)

"""
Ask the user for the spritesheet's filename
"""
fileName = tkinter.simpledialog.askstring("Type the spritesheet name: ", root)


spritesheet_width = 0
spritesheet_height = 0

files = os.listdir(myDir)
files.sort()
print(files)

for current_file in files :
    try:
        with Image.open(myDir  + "/" + current_file) as im :
            frames.append(im.getdata())
    except:
        print(current_file + " is not a valid image")

tile_width = frames[0].size[0]
tile_height = frames[0].size[1]

if len(frames) > max_frames_row :
    spritesheet_width = tile_width * max_frames_row
    required_rows = math.ceil(len(frames)/max_frames_row)
    spritesheet_height = tile_height * required_rows
else:
    spritesheet_width = tile_width*len(frames)
    spritesheet_height = tile_height
    
print(spritesheet_height)
print(spritesheet_width)

spritesheet = Image.new("RGBA",(int(spritesheet_width), int(spritesheet_height)))

for current_frame in frames :
    top = tile_height * math.floor((frames.index(current_frame))/max_frames_row)
    left = tile_width * (frames.index(current_frame) % max_frames_row)
    bottom = top + tile_height
    right = left + tile_width
    
    box = (left,top,right,bottom)
    box = [int(i) for i in box]
    cut_frame = current_frame.crop((0,0,tile_width,tile_height))
    
    spritesheet.paste(cut_frame, box)
    
"""
it will save the Spritesheet into the python file folder.
"""    
spritesheet.save(fileName + ".png", "PNG")