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
        self.filetypes = ['.jpg', '.gif', '.png', '.jpeg', '.JPG']

        # db manager
        self.db = database_manager.MANAGER(client='apod')
        self.wrong_filetype = self.db.getRecords(type='bad_days')
        self.too_large = self.db.getRecords(type='too_large')

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
        self.download_years(start_year=self.year_start,
                            end_year=self.time_now.year)

    def downloadAll_1995_thru_1997(self):
        for year in range(self.year_start, 1997):
            for month in range(1, 12 + 1):
                for day in range(1, int(self.days[month]) + 1):
                    this_year = str(year)
                    this_month = str(month).rjust(2, '0')
                    this_day = str(day).rjust(2, '0')

                    if(str(this_year + this_month + this_day) in self.wrong_filetype):
                        print(".", end='', flush=True)
                        self.wrong_filetype.pop(0)
                    elif(str(this_year + this_month + this_day) in self.too_large):
                        print(".", end='', flush=True)
                        self.too_large.pop(0)
                    elif(self.db.checkDay(year=this_year, month=this_month, date=this_day)):
                        self.downloadAPOD(
                            year=this_year, month=this_month, date=this_day)
                    else:
                        print(".", end='', flush=True)

    def download_years(self, start_year, end_year):
        end = False
        for year in range(start_year, end_year + 1):
            for month in range(1, 12 + 1):
                for day in range(1, int(self.days[month]) + 1):
                    this_year = str(year)
                    this_month = str(month).rjust(2, '0')
                    this_day = str(day).rjust(2, '0')

                    if(str(this_year + this_month + this_day) in self.wrong_filetype):
                        print(".", end='', flush=True)
                        self.wrong_filetype.pop(0)
                    elif(str(this_year + this_month + this_day) in self.too_large):
                        print(".", end='', flush=True)
                        self.too_large.pop(0)
                    elif(self.db.checkDay(year=this_year, month=this_month, date=this_day)):
                        self.downloadAPOD(
                            year=this_year, month=this_month, date=this_day)
                    else:
                        print(".", end='', flush=True)

                    if((year == end_year) and (month == self.time_now.month) and (day == self.time_now.day - 1)):
                        end = True
                        break
                if(end):
                    break
            if(end):
                break

    def downloadAPOD(self, year, month, date):
        try:
            dict = self.parse(year, month, date)
            path = dict['path']
            filename = dict['filename']
            image_size = int(requests.get(self.apod_url + path, stream=True).headers['Content-length'])
            if(image_size > 10133333):
                raise ValueError('image file being to large')

            # download image
            print('\nDownloading... %s: %s, %s, %s' %
                  (filename, month, date, year))
            image = requests.get(self.apod_url + path).content
            image_data = base64.b64encode(image)

            # add record
            self.db.addDay(path, year=year,
                           month=month, date=date, filename=filename, data=image_data)
        except Exception as e:
            if('large' in str(e)):
                self.db.addRecord(type='too_large', year=year, month=month, date=date)
            elif('incompatible' in str(e)):
                self.db.addRecord(type='bad_days', year=year, month=month, date=date)
            print('\nDownload failed due to %s\t%s %s %s' %
                  (e, year, month, date))

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
        apod = apod = requests.get(self.apod_daily +
                                   appendix).content
        try:
            apod = str(apod.decode('ascii', errors="ignore")).splitlines()

            found = False
            for line in list(apod):
                for filetype in self.filetypes:
                    if('href=\"image' in line):
                        image_regex = "href=\"image/.*\""
                        path = re.search(image_regex, str(line)).group(0)[6:-1]
                        if(filetype in line):
                            found = True
                            filename = str(
                                re.search('[^/]*.[0-9a-zA-Z]*%s' % filetype, path).group(0))
                if(found):
                    break
            if(not found):
                raise ValueError('an incompatible filetype')
            dict = {
                "path": path,
                "filename": filename
            }

            return dict
        except Exception as e:
            raise e


if __name__ == "__main__":
    main = API()
    # main.downloadAPOD('2011', '12', '25')
    main.download_years(start_year=2005, end_year=2020)
    # main.temp()
