#!/usr/bin/python3
# Organise images by date taken
#
# 02 Feb 21
# Tim Stephenson

import argparse
import os
import shutil
import sys
from PIL import Image

# Set list of valid file extensions
valid_extensions = [".JPG", ".jpg", ".jpeg", ".png"]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default=".", help="base input directory")
    parser.add_argument("-o", "--output", default="output", help="base output directry")
    parser.add_argument("-m", "--move", action="store_true", help="move the file (default is to copy)")
    parser.add_argument("-r", "--recurse", action="store_true", help="process child directories as well")
    parser.add_argument("-v", "--verbose", action="store_true", help="increase the progess messages")
    return parser.parse_args()

def process_dir(dir_path):
    print('processing dir: ' + dir_path)

    # list files in dir
    file_names = os.listdir(dir_path)

    # for each file
    for file_name in file_names:
        if (args.verbose):
            print('  processing: ' + file_name)

        # get file extension
        file_ext = os.path.splitext(file_name)[1]

        # process image / dir / other
        if (file_ext in valid_extensions):
            process_image(os.path.join(dir_path, file_name))
        elif (os.path.isdir(os.path.join(dir_path, file_name))):
            process_dir(os.path.join(dir_path, file_name))
        else:
            if (args.verbose):
                print('    skipping unsupported extension: ' + file_ext)
            continue

def process_image(file_name):
    print('    process image: ' + file_name)
    # Create the old file path
    old_file_path = os.path.join(dir_path, file_name)

    # open the image
    if (args.verbose):
        print('    opening: ' + old_file_path)
    try:
        image = Image.open(old_file_path)
    except:
        if (args.verbose):
            print('    cannot open ' + file_name)
        return

    # get EXIF metadata
    if (image._getexif() == None):
        if (args.verbose):
            print('    skipping ' + file_name + ' because no EXIF data available')
        return

    # get date taken from metadata
    try:
        print(image._getexif()[36867])
        date_taken = image._getexif()[36867]
    except:
        if (args.verbose):
            print('    skipping ' + file_name + ' because no EXIF data available')
        return

    # close the image
    image.close()

    # extract parts of date and format
    year = date_taken[0:4]
    month = date_taken[5:7]
    day = date_taken[8:10]
    date_time = date_taken \
        .replace(":", "-") \
        .replace(" ", "-")

    # get the base file without parent dir or extension
    file_base = os.path.basename(os.path.splitext(file_name)[0])

    # get file extension
    file_ext = os.path.splitext(file_name)[1]

    # combine the new file name and file extension
    new_file_name = year + '-' + month + '-' + day + '-' + file_base + file_ext.lower()

    # make target dir
    if not (os.path.exists(args.output)):
        os.mkdir(args.output)
    trgt_path = os.path.join(args.output, year)
    if not (os.path.exists(trgt_path)):
        os.mkdir(trgt_path)
    trgt_path = os.path.join(trgt_path, month)
    if not (os.path.exists(trgt_path)):
        os.mkdir(trgt_path)

    # create the new dir path
    new_file_path = os.path.join(trgt_path, new_file_name)

    # copy / move the file
    if (args.move):
        if (args.verbose):
            print('    moving from ' + old_file_path + ' to ' + new_file_path)
        shutil.move(old_file_path, new_file_path)
    else:
        if (args.verbose):
            print('    copying from ' + old_file_path + ' to ' + new_file_path)
        shutil.copy2(old_file_path, new_file_path)

# main
args = parse_args()

dir_path = args.input
if (dir_path == '.'):
    dir_path = os.getcwd()

process_dir(dir_path)
