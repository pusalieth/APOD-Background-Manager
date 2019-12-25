import datetime
import requests


class WEB_HANDLER:
    def __init__(self):
        self.archive_url = "https://apod.nasa.gov/apod/archivepix.html"
        self.image_dl_url = "https://apod.nasa.gov/apod/image/1912/"
        self.start_year = '1995'
        self.time_now = datetime.datetime.now()
        self.months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                       'August', 'September', 'October', 'November', 'December']

    def checkDB(self):
        print()

    def downloadImage(self, date):
        filename = ""
        response = requests.get(self.image_dl_url + filename)
        file = open(filename, 'wb')
        file.write(response.content)
        file.close()

    def downloadArchive(self):
        response = requests.get(self.archive_url)
        self.archive = str(response.content).replace('\n\n', '\n').splitlines()
        for substring in list(self.archive):
            found = False
            for month in self.months:
                if(month in substring):
                    found = True
                    break
            if(not found):
                self.archive.remove(substring)

    def setDateFilenames(self):
        self.dates = []
        for substring in self.archive:
            temp = substring.split(':')
            timestamp = dict()
            timestamp['year'] = temp[0][-4:]
            timestamp['date'] = temp[0][-7:-5]
            timestamp['month'] = temp[0][:-8]
            url_start = temp[1].find('=') + 2
            url_end = temp[1].find('\"', url_start)
            timestamp['url'] = temp[1][url_start:url_end]

            print(temp[url_end:])


if __name__ == "__main__":
    main = WEB_HANDLER()
    main.downloadArchive()
    main.setDateFilenames()
