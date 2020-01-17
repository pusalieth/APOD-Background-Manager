import pymongo


class MANAGER:
    def __init__(self, client=None):
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        if(client != None):
            self.db = self.client[client]

    def setClient(self, client):
        self.db = self.client[client]

    def getRandomDay(self):
        print()

    def addDay(self, url, year, month, date, filename, data):
        sub_dict = {"url": url,
                    "year": year,
                    "month": month,
                    "day": date,
                    "filename": filename,
                    "data": data}
        dict = {"images": sub_dict}

        try:
            if(self.checkDay(year=year, month=month, date=date)):
                self.db["database"].insert(dict)
            else:
                print('Document already exists')
        except Exception as e:
            print('Insert failed due to %s' % e)

    def checkDay(self, year, month, date):
        result = self.db["database"].find(
            {
                "images.year": year,
                "images.month": month,
                "images.day": date
            },
            {
                "images.url": 0,
                "images.filename": 0,
                "images.data": 0
            }
        ).count()

        if(result == 0):
            return True
        else:
            return False

    def addTooLargeDay(self, year, month, date):
        result = self.db["database"].find(
            {
                "too_large.year": year,
                "too_large.month": month,
                "too_large.day": date
            }
        ).count()

        try:
            sub_dict = {"year": year,
                        "month": month,
                        "day": date}
            dict = {"too_large": sub_dict}
            if(result == 0):
                self.db["database"].insert(dict)
        except Exception as e:
            print('Insert failed due to %s' % e)

    def getTooLargeDays(self):
        result = self.db["database"].find(
            {
                "too_large": {'$exists': 1}
            }
        )

        too_large = []

        for record in result:
            this_record = record['too_large']
            too_large.append(this_record['year'] + this_record['month'] + this_record['day'])

        return too_large

    def addBadDay(self, year, month, date):
        result = self.db["database"].find(
            {
                "bad_days.year": year,
                "bad_days.month": month,
                "bad_days.day": date
            }
        ).count()

        try:
            sub_dict = {"year": year,
                        "month": month,
                        "day": date}
            dict = {"bad_days": sub_dict}
            if(result == 0):
                self.db["database"].insert(dict)
        except Exception as e:
            print('Insert failed due to %s' % e)

    def getBadDays(self):
        result = self.db["database"].find(
            {
                "bad_days": {'$exists': 1}
            }
        )

        bad_days = []

        for record in result:
            this_record = record['bad_days']
            bad_days.append(this_record['year'] + this_record['month'] + this_record['day'])

        return bad_days

    def removeBadDay(self, year, month, date):
        result = self.db["database"].find(
            {
                "bad_days.year": year,
                "bad_days.month": month,
                "bad_days.day": date
            }
        )

        try:
            if(result.count() > 0):
                self.db["database"].delete_one(dict)
        except Exception as e:
            print('Insert failed due to %s' % e)

    def removeDuplicate(self, year, month, date):
        print()

    def deleteCollection(self, collection=None):
        collection.drop()
        result = self.checkCollectionExists(collection)
        if(result is None):
            return ("Collection %s successfully deleted" % collection)
        else:
            return ("Error occured, Collection was not removed")

    def checkDBExists(self, db_name=None):
        dblist = self.client.list_database_names()
        if db_name in dblist:
            return ("The database %s exists." % db_name)

    def checkCollectionExists(self, collection=None):
        collist = self.db.list_collection_names()
        if collection in collist:
            return ("The collection %s exists." % collection)
