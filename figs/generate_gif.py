import imageio
import glob
import os

def clean_jpg_files():
    jpg_files = glob.glob("figs/*.jpg")
    
    for jpg_file in jpg_files:
        os.remove(jpg_file)
    

def main():

    jpg_files = glob.glob("figs/*.jpg")
    count = len(jpg_files)

    filenames = [ f"{i}.jpg" for i in range(count)]
    images = []
    for filename in filenames:
        image = imageio.imread(f"figs/{filename}")
        images.append(image)

    output_filename = 'first_animation.gif'
    imageio.mimsave(output_filename, images, duration=0.75)