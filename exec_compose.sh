# Usage: megasimplesync [local folder] [remote folder]

docker exec datarchiver_sortdata_1 sh -c 'python3 sort_data.py'
#docker exec datarchiver_sync2018_1 sh -c 'megasimplesync $LOCAL_FOLDER $REMOTE_FOLDER'
docker exec datarchiver_sync2020_1 sh -c 'megasimplesync $LOCAL_FOLDER $REMOTE_FOLDER'
