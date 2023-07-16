from ants_main import main as am
from figs_producer import main as fm
from second_figs_producer import main as sfm
from figs.generate_gif import main as fgfm
from figs.generate_gif import clean_jpg_files as cleanf
from second_figs.generate_gif import main as sfgfm
from second_figs.generate_gif import clean_jpg_files as cleansf

print("cleaning figs directories")
cleanf()
cleansf()

print("Starting ant colony simulator")
am()

print("Starting production of figs for the first GIF simulation")
fm()

print("Starting production of figs for the second GIF simulation")
sfm()

print("Producing first GIF simulation")
fgfm()

print("Producing second GIF simulation")
sfgfm()