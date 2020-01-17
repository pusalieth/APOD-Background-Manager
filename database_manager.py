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

    def addRecord(self, type, year, month, date):
        result = self.db["database"].find(
            {
                type + ".year": year,
                type + ".month": month,
                type + ".day": date
            }
        ).count()

        try:
            print(result)
            sub_dict = {"year": year,
                        "month": month,
                        "day": date}
            dict = {type: sub_dict}
            if(result == 0):
                self.db["database"].insert(dict)
        except Exception as e:
            print('Insert failed due to %s' % e)

    def getRecords(self, type):
        result = self.db["database"].find(
            {
                type: {'$exists': 1}
            }
        )

        temp = []

        for record in result:
            this_record = record[type]
            temp.append(this_record['year'] + this_record['month'] + this_record['day'])

        temp.sort()

        return temp

    def removeRecord(self, type, year, month, date):
        result = self.db["database"].find(
            {
                type + ".year": year,
                type + ".month": month,
                type + ".day": date
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
