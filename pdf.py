from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import dateutil.parser as dparser
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pymongo import MongoClient
from multiprocessing import Pool
import datetime
import os
from bson.json_util import dumps

#db init
client = MongoClient()
db = client.db_archive
archive_collection = db.test_archive_collection

class Doc:
    def __init__(self, url, month, day, year, page):
        self.url = url
        self.month = month
        self.day = day
        self.year = year
        self.page = page
        self.date = datetime.datetime(year,month,day)
    def test_format_and_upload(self):
        print "Converting " + self.url + " ..."
        raw_text = convert_pdf_to_txt(self.url)
        post = {
            "url": self.url,
            "month": self.month,
            "day": self.day,
            "year": self.year,
            "page": self.page,
            "date": self.date,
            "text": raw_text
        }
        print "Done! Now inserting to DB..."
        archive_collection.insert_one(post)

class GDrive:
    def __init__(self):
        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'ascii'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str


def pop_test():
    ls = os.listdir("testfiles")
    docs = []
    for i, f in enumerate(ls):
        path = "testfiles/" + f
        d = Doc(path, 1, 6, 2003, i+1)
        docs.append(d)
    map(lambda d: d.test_format_and_upload(), docs)

def main():
    #gdrive = GDrive()
    #pop_test()
    res = archive_collection.find(
        { '$text': { '$search': "auld lang syne" } },
        { 'url': 1,'score' : { '$meta': 'textScore' }}
    )
    l = list(res)
    print dumps(l)


if __name__ == "__main__":
    main()

#for file_list in drive.ListFile():
#  print 'Received %s files from Files.list()' % len(file_list) # <= 10
#  for file1 in file_list:
#    print 'title: %s, id: %s' % (file1['title'], file1['id'])
