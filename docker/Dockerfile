FROM python:3

RUN apt-get upgrade && apt-get update -y

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# setup cronjob
#COPY ./crontab_sort /etc/cron.d/crontab_sort
#RUN chmod 0644 /etc/cron.d/crontab_sort
#RUN crontab /etc/cron.d/crontab_sort
#RUN touch ./cron.log

# install exiftool
RUN gzip -dc Image-ExifTool-11.93.tar.gz | tar -xf -
WORKDIR /usr/src/app/Image-ExifTool-11.93
RUN perl Makefile.PL
RUN make test
RUN make install

WORKDIR /usr/src/app/


#CMD [ "python", "./sort_pics.py" ]
