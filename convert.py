#Place your image in the folder with the image-hodler folder, then run the script.

from PIL import Image
import os
import numpy as np


def closest(color):
    color = np.array(color)
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    return np.where(distances == np.amin(distances))[0][0]

def makeInclude():
    try: os.remove(out_folder + 'include.asm') 
    except: pass
    include = ''
    count = 0
    for i in os.listdir(out_folder):
        include += '%include \'' + out_basefolder + os.listdir(out_folder)[count] + '\'\n'
        count += 1
    
    with open(out_folder + 'include.asm', "w") as includefile:
        includefile.write(include)
    return

def getArray(img_path):
    final_val = []
    img = Image.open(img_path, 'r')
    img.putalpha(255)
    img_val = list(img.getdata())
    
    inc = 0
    for i in img_val:
        ndx = closest(i)
        final_val.append(ndx)
        inc += 1
    return final_val


img_folder = '../../art/'
out_basefolder = 'src/art/'
out_folder = '../../' + out_basefolder
ref = Image.open('ref.png', 'r')
ref_val = list(ref.getdata())
colors = np.array(ref_val)

counter = 0
for files in os.listdir(img_folder):
    img_file = os.listdir(img_folder)[counter]
    print(img_file)
    img_path = os.path.join(os.path.dirname(img_folder), os.path.basename(img_file))
    final = os.path.splitext(img_file)[0] + ": db \\\n" + (', '.join(str(x) for x in getArray(img_path)))
    with open(out_folder + os.path.splitext(img_file)[0] + ".asm", "w") as outfile:
        outfile.write(final)
    counter += 1

makeInclude()
