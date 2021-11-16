# sort_data_away
## Overview
This tool aims at archiving (or sorting) away files from a data pool into the following structure:
For example

- 2019
  - 2019-01-01_dummy
  - 2019-01-02_dummy
  - ...
  - 2019-12-31_dummy
- 2020
  - ...

Supported file types are mainly the one related to image files (e.g. png, jpg).
The date of the images are taken from the exif headers respectively via the tool ExifTool via
[github] (https://github.com/exiftool/exiftool) or download from [exiftool] (https://exiftool.org/)

## Instructions
To use the tool, be aware of properly configuring the config under \
`./config/config.yaml`
Make sure to set the path settings correct:\
- `data_dir_unsorted`: the directory where all the data that is to be archived is stored. 
Note that the tool searches recursively.
- `data_dir_sorted`: The path where the structure is build and the data is stored.
- `exif_key_create_date`: (static)
- `daily_folder_suffix`: suffix that is appended to the daily folders
- `originator_names`: if the data in the unsorted folder is in a folder that relates to the given names.
Then the name is attached to the ExifHeader Tag "Comment". 
This allows for searching later on from whom the data is coming from.

Then run the tool via:
```
python3 sort_data.py
```

Another script, namely the clean_folder_structure.py can be used to rename file and folder names 
in order to allow for recursive search (e.g. ä --> ae, empty spaces --> _)

Run the tool via:
```
python3 clean_folder_structure.py
```

## ExifTool
good examples: \
https://martin.hoppenheit.info/blog/2015/useful-exiftool-commands/

Write Comment Tag: \
`exiftool -Comment='TEST' 20201117_134332.jpg`

list files with Comment tag = TEST (recursively): \
`exiftool -if '$Comment =~ /(TEST)/' -Directory -FileName -T -R .`

## ExifMetaTool
under `./exif_meta_tool` is a script that allows to query the data based on ExifHeader Information.

## Issues, Room for Improvement
- Support further data types

## License
to be done