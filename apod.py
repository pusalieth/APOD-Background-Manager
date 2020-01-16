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
        self.mix_types_days = ['20010418', '20010628', '20020429', '20020522', '20020704', '20021106', '20030825', '20050117', '20060529', '20061204', '20070120', '20070303', '20070312', '20070318', '20070514', '20070522', '20070702', '20070829', '20071106', '20071204', '20080228', '20080429', '20080519', '20080525', '20080722', '20081125', '20081231', '20090405', '20090413', '20090629', '20090810', '20100120', '20100124', '20100510', '20100526', '20100608', '20100725', '20100825', '20101124', '20101215', '20110123', '20110201', '20110222', '20110307', '20110315', '20110328', '20110418', '20110504', '20110516', '20110526', '20110601', '20110613', '20110704', '20110711', '20110809', '20110827', '20110905', '20110920', '20110927', '20111003', '20111005', '20111018', '20111101', '20111106', '20111108', '20111121', '20111206', '20120116', '20120209', '20120305', '20120312', '20120320', '20120411', '20120424', '20120501', '20120508', '20120514', '20120523', '20120611', '20120702', '20120710', '20120717', '20120723', '20120731', '20120806', '20120813', '20120821', '20121022', '20121107', '20121114', '20121210', '20130115', '20130121', '20130129', '20130130', '20130204', '20130217', '20130218', '20130226', '20130331', '20130424', '20130514', '20130606', '20130609', '20130612', '20130618', '20130701', '20130702', '20130724', '20130731', '20130805', '20130819', '20130827', '20130916', '20130930', '20131130', '20131225', '20131229', '20140112', '20140210', '20140224', '20140312', '20140319', '20140409', '20140428', '20140512', '20140514', '20140521', '20140526', '20140616', '20140617', '20140811', '20140826', '20140907', '20140922', '20141005', '20141013', '20141022', '20141124', '20141208', '20150112', '20150125', '20150224', '20150324', '20150414', '20150421', '20150527', '20150601', '20150610', '20150622', '20150629', '20150718', '20150722', '20150927', '20151006', '20151020', '20151028', '20151102', '20151109', '20151202', '20151205', '20151222', '20151225', '20151228', '20160209', '20160212', '20160222', '20160306', '20160315', '20160405', '20160509', '20160511', '20160530', '20160601', '20160615', '20160628', '20160731', '20160802', '20160921', '20160926', '20161003', '20161010', '20161017', '20161105', '20161221', '20170116', '20170201', '20170221', '20170319', '20170401', '20170417', '20170515', '20170523', '20170531', '20170607', '20170618', '20170619', '20170704', '20170717', '20170731', '20170812', '20170814', '20170820', '20170826', '20170910', '20170911', '20170912', '20171016', '20171113', '20171126', '20171127', '20171203', '20171204', '20171211', '20171214', '20171220', '20180101', '20180104', '20180122', '20180128', '20180219', '20180226', '20180305', '20180312', '20180318', '20180409', '20180416', '20180424', '20180429', '20180521', '20180527', '20180530', '20180612', '20180618', '20180710', '20180729', '20180806', '20180808', '20180902', '20180910', '20180912', '20180918', '20181007', '20181010', '20181101', '20181113', '20181120', '20181126', '20181203', '20181208', '20181223', '20190108', '20190120', '20190205', '20190219', '20190224', '20190226', '20190312', '20190320', '20190324', '20190410', '20190414', '20190422', '20190428', '20190506', '20190520', '20190526', '20190602', '20190630', '20190703', '20190710', '20190716', '20190717', '20190820', '20190825', '20190903', '20190908', '20191001', '20191021', '20191118', '20191202', '20191209', '20191222', '20191223']

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
        self.download_years(start_year=self.year_start, end_year=self.time_now.year)

    def downloadAll_1995_thru_1997(self):
        for year in range(self.year_start, 1997):
            for month in range(1, 12 + 1):
                for day in range(1, int(self.days[month]) + 1):
                    this_year = str(year)
                    this_month = str(month).rjust(2, '0')
                    this_day = str(day).rjust(2, '0')

                    if(str(this_year + this_month + this_day) in self.mix_types_days):
                        print(".", end='', flush=True)
                        self.mix_types_days.pop(0)
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

                    if(str(this_year + this_month + this_day) in self.mix_types_days):
                        print(".", end='', flush=True)
                        self.mix_types_days.pop(0)
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
            image_size = int(requests.head(self.apod_url + path).headers['content-length'])
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
            print('\nDownload failed due to %s\t%s %s %s' % (e, year, month, date))

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
                self.mix_types_days.append('%s%s%s' % (year, month, date))
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
    main.download_years(start_year=2016, end_year=2020)
