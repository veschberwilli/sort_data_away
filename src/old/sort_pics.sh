
#!/bin/bash

#export dir_data_unsorted=/media/egon/egon/data
export dir_data_unsorted=/media/pi/egon/data_all_unsorted
export dir_data_sorted=/media/pi/egon/data_sorted
export daily_folder_suffix="_dummy"


# loop over data recursively
IFS=$'\n'
for file_raw in `find $dir_data_unsorted -type f \
	-name "*.png" -or \
	-name "*.jpg" -or \
	-name "*.jpeg" -or \
	-name "*.JPG" -or \
	-name "*.mp4"`
do
 file=$( echo "$file_raw" | sed 's/ /\\ /g' )

 # read exif header
 CREATE_DATE=$(eval exiftool -d "%Y-%m-%d" -CreateDate -S -s "$file")

 # check if create_date is available
 if [ -z "$CREATE_DATE" ]
 then
  # if no create_date is found, then file is storred to separate folder
  CREATE_DATE='missing_creation_date'
  folder_day=$dir_data_sorted/$CREATE_DATE

  if [[ $file =~ "IMG-" ]]
  then
   # no create_date found but file name is according to whatsapp naming convention
   # date in file name refers to receive/sent date!
  
   # parse date out of file name
   CREATE_DATE_RAW=$(echo $file | awk -F'/' '{print $NF}' | cut -c 5-12)
   YEAR=$(echo $CREATE_DATE_RAW | cut -c 1-4)
   MONTH=$(echo $CREATE_DATE_RAW | cut -c 5-6)
   DAY=$(echo $CREATE_DATE_RAW | cut -c 7-8)
   export CREATE_DATE=$YEAR-$MONTH-$DAY

   # year folder
   folder_year=$dir_data_sorted/$YEAR

   # day folder
   folder_day=$dir_data_sorted/$YEAR/$CREATE_DATE$daily_folder_suffix

   # create year-dir if not exist
   mkdir -p $folder_year
  fi

 else
  # create_date available

  # parse date
  YEAR=$(echo $CREATE_DATE | cut -c 1-4)

  # year folder
  folder_year=$dir_data_sorted/$YEAR

  # day folder
  folder_day=$dir_data_sorted/$YEAR/$CREATE_DATE$daily_folder_suffix

  # create year-dir if not exist
  mkdir -p $folder_year
 fi

 # create day-dir if not exist
 mkdir -p $folder_day

 # distinguish vid and pic
 if [[ $file =~ ".mp4" ]]
 then
  # create vids folder in day-dir if not exist
  mkdir -p $folder_day/vids
  
  # cp to dir_data_sorted
  eval "cp $file $folder_day/vids"
 else
  # cp to dir_data_sorted
  eval "cp $file $folder_day"
 fi

 # log
 #echo "File moved: " $file "-->" $folder_day
 printf "%40s \t --> \t%s\n" $file $folder_day
done

# identify WA format. how to handle this? obviously send/receive date is provided and exif got stripped


