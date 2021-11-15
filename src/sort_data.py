
####################################################################
# script to import data from different sources into defined structure
# Author: Michael Mink
####################################################################

# import packages
import os
import exiftool
import glob
import yaml
import logging


# configuration for logger
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s]  %(message)s",
    handlers=[
        logging.StreamHandler()
    ])

# ++++++++++++++++++++++++++++++
# create_date class
# ++++++++++++++++++++++++++++++
class create_date:
    def __init__(self):
        self.year = None
        self.month = None
        self.day = None

    def insert_date(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def get_date_string(self):
        if self.year is None and self.month is None and self.day is None:
            return None
        else:
            return '%s-%s-%s' % (self.year, self.month, self.day)


class SortData:
    def __init__(self):

        logging.info('Start SortData Tool.')

        # read config file
        try:
            path_to_yaml = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml')
            with open(path_to_yaml, 'r') as config_file:
                self.config = yaml.load(config_file, Loader=yaml.FullLoader)
        except IOError:
            raise Exception('config file reading error.')

        # read parameters
        self.dir_data_unsorted = self.config['path_settings']['dir_data_unsorted']
        self.dir_data_sorted = self.config['path_settings']['dir_data_sorted']
        self.pic_file_type = self.config['pic_file_type']
        self.vid_file_type = self.config['vid_file_type']
        self.daily_folder_suffix = self.config['daily_folder_suffix']
        self.exif_key_create_date = self.config['exif_key_create_date']

        # define path to unknown date files
        self.path_unknown_date = os.path.join(self.dir_data_sorted, 'unknown_date')

        # create unknown date folder (if not exist)
        os.system('mkdir -p %s' % self.path_unknown_date)

        # start
        self.start_sort_data()

        # end
        logging.info('End of SortData Tool.')

    def start_sort_data(self):
        """
        search directories recursively
        """
        for (path,_,files) in os.walk(self.dir_data_unsorted):
            logging.info('Looking into %s ...' % path)

            # get files in directory
            for file in files:
                # check file if its a pic or a vid
                if file.endswith(tuple(self.pic_file_type)) or file.endswith(tuple(self.vid_file_type)):

                    file_path = os.path.join(path, file)
                    file_type = file.split('.')[-1]
                    create_date_obj = create_date()

                    # update Comment Tag with Name
                    for originator in self.config['originator_names']:
                        if originator in path:
                            _ = os.system("""exiftool -Comment="%s" -overwrite_original_in_place %s""" % (originator, file_path))

                    # read exif header
                    with exiftool.ExifTool() as et:
                        exif_data = et.get_metadata(file_path)

                    # get create_date entry from exif header (if available)
                    create_date_tag = None
                    for tag in exif_data:
                        if self.exif_key_create_date in tag:
                            create_date_tag = tag
                            continue

                    # if file has exif header and the create_date entry
                    if create_date_tag in exif_data:
                        create_datetime_raw = exif_data[create_date_tag]
                        create_date_raw = create_datetime_raw.split(' ')[0]
                        year = create_date_raw.split(':')[0]
                        month = create_date_raw.split(':')[1]
                        day = create_date_raw.split(':')[2]
                        create_date_obj.insert_date(year, month, day)

                    # if file has no exif header, but its a whatsapp
                    elif ('IMG-' and '-WA' in file) or ('VID-' and '-WA' in file):
                        year = file.split('-')[1][0:4]
                        month = file.split('-')[1][4:6]
                        day = file.split('-')[1][6:8]
                        create_date_obj.insert_date(year, month, day)

                    else:
                        # if create_date is not found then cp file to unknown_date folder
                        os.system('cp -n %s %s' % (str(file_path), self.path_unknown_date))
                        logging.error('No Date Info Found -> %s' % file_path)
                        continue

                    # create yearly folder (if not exist)
                    folder_year = os.path.join(self.dir_data_sorted, create_date_obj.year)
                    os.system('mkdir -p %s' % (folder_year))

                    # create daily folder (if not exist)
                    folder_day_wo_suffix = os.path.join(folder_year, create_date_obj.get_date_string())
                    nr_folders_wo_suffix = len(glob.glob(os.path.join(folder_day_wo_suffix + '*')))

                    # if folder not exists then create default folder (w suffix)
                    if nr_folders_wo_suffix == 0:
                        folder_day = os.path.join(folder_day_wo_suffix + self.daily_folder_suffix)
                        os.system('mkdir -p %s' % (folder_day))
                    elif nr_folders_wo_suffix == 1:
                        folder_day = glob.glob(os.path.join(folder_day_wo_suffix + '*'))[0]
                    elif nr_folders_wo_suffix > 1:
                        logging.error('more than one daily folders found!!!!!!')
                        exit(1)

                    # move to daily folder
                    # if its a pic
                    if file_type in self.pic_file_type:
                        os.system('cp -n %s %s' % (file_path, folder_day))
                    # if its a vid (create vid dir if not exist)
                    elif file_type in self.vid_file_type:
                        folder_day = os.path.join(folder_day, 'vid')
                        os.system('mkdir -p %s' % (folder_day))
                        os.system('cp -n %s %s' % (file_path, folder_day))

                    logging.info('copied %s --> %s, create date: %s' % (file_path, folder_day, create_date_obj.get_date_string()))

                else:
                    logging.error('File Not Supported -> %s' % file)

if __name__ == "__main__":
    run = SortData()
