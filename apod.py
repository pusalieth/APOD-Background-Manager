import datetime
import requests
import re
import os
import database_manager
import base64
import sys


class API:
    def __init__(self):
        self.archive_url = "https://apod.nasa.gov/apod/archivepix.html"
        self.apod_daily = "https://apod.nasa.gov/apod/ap"
        self.apod_url = "https://apod.nasa.gov/apod/"
        self.year_start = 1995
        self.month_start = 6
        self.date_start = 25
        self.time_now = datetime.datetime.now()
        self.months = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        self.days = ['0', '31', '28', '31', '30', '31', '30',
                     '31', '31', '30', '31', '30', '31']
        self.filetypes = ['.jpg', '.gif']

        # db manager
        self.db = database_manager.MANAGER(client='apod')

    def downloadPrim(self):
        for year in range(self.year_start, self.year_start + 1):
            for month in range(self.month_start, 12 + 1):
                for day in range(self.date_start, int(self.days[month]) + 1):
                    this_year = str(year)[2:]
                    this_month = str(month).rjust(2, '0')
                    this_day = str(day).rjust(2, '0')
                    self.downloadAPOD(
                        year=this_year, month=this_month, date=this_day)

    # 11, 1, 96 url change
    def downloadAll(self):
        for year in range(1997, self.time_now.year + 1):
            for month in range(1, 12 + 1):
                for day in range(1, int(self.days[month]) + 1):
                    this_year = str(year)
                    this_month = str(month).rjust(2, '0')
                    this_day = str(day).rjust(2, '0')

                    if(self.db.checkDay(year=this_year, month=this_month, date=this_day)):
                        self.downloadAPOD(
                            year=this_year, month=this_month, date=this_day)
                    else:
                        print(".", end='', flush=True)

    def downloadAPOD(self, year, month, date):
        appendix = str(year) + str(month) + str(date) + ".html"
        apod = str(requests.get(self.apod_daily +
                                appendix).content).splitlines()

        dict = self.parse(year, month, date)
        path = dict['path']
        filename = dict['filename']
        print('\nDownloading... %s: %s, %s, %s' %
              (filename, month, date, year))

        # download image
        image = requests.get(self.apod_url + path).content
        image_data = base64.b64encode(image)

        # add record
        self.db.addDay(path, year=year,
                       month=month, date=date, filename=filename, data=image_data)

    def downloadArchive(self):
        archive_html = requests.get(self.archive_url).content
        self.archive = str(archive_html).replace('\n\n', '\n').splitlines()
        for substring in list(self.archive):
            found = False
            for month in self.months:
                if(month in substring):
                    found = True
                    break
            if(not found):
                self.archive.remove(substring)

        self.apods = []
        for substring in self.archive:
            temp = substring.split(':')
            timestamp = dict()
            timestamp['year'] = re.search(r"(\d{4})", temp[0]).group(1)
            timestamp['date'] = re.search(r"(\d{2})", temp[0]).group(1)
            for month in self.months:
                if(month in temp[0]):
                    timestamp['month'] = month
                    break
            url_start = temp[1].find('=') + 2
            url_end = temp[1].find('\"', url_start)
            timestamp['url'] = temp[1][url_start:url_end]
            filename_start = temp[1].find('>', url_end) + 1
            filename_end = temp[1].find('<', filename_start)
            timestamp['filename'] = temp[1][filename_start:filename_end]
            self.apods.append(timestamp)

    def parse(self, year, month, date):
        appendix = str(year)[2:] + str(month) + str(date) + ".html"
        apod = str(requests.get(self.apod_daily +
                                appendix).content.decode('ascii')).splitlines()

        found = False
        for line in list(apod):
            for filetype in self.filetypes:
                if('href=\"image' in line):
                    image_regex = "href=\"image/.*\""
                    path = re.search(image_regex, str(line)).group(0)[6:-1]
                    found = True
                    if(filetype in line):
                        filename = str(
                            re.search('[^/]*.[0-9a-zA-Z]*%s' % filetype, path).group(0))
            if(found):
                break
        dict = {
            "path": path,
            "filename": filename
        }

        return dict


if __name__ == "__main__":
    main = API()
    # main.downloadAPOD('2011', '12', '25')
    main.downloadAll()
