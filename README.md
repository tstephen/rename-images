# Rename Images with Date Photo Taken

Purpose: Renames image files in a folder based on date photo taken from EXIF metadata

Original author: Matthew Renze
Modified by: Tim Stephenson to offer choice of move and copy and to recurse directories

Usage: ./organise-py --help

Example: ./organise.py -r -i ~/Photos -o ~/Album
  will create a new structure, copy and rename the photos into Album

Behaviour:
 - Given a photo named "Photo of Dad.jpg"
 - with EXIF date taken of "4/1/2018 5:54:17 PM"  
 - when you run this script on its parent folder
 - then it will be moved / copied to 2018/04/2018-04-01-Photo of Dad.jpg"

Notes:
  - For safety, please make a backup before running this script
  - Currently only designed to work with .jpg, .jpeg, and .png files
  - EXIF metadate must exist or an error will occur
