import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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

def format_and_upload():
    text = convert_pdf_to_txt("page1.pdf")
    print text
    d = dparser.parse(text[4:50],fuzzy=True).date()
    print d

def main():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)


    file_list = drive.ListFile({'q': "'0B9y1-prT44zATkItckZyajJwLXM' in parents and trashed=false"}).GetList()
    for file1 in file_list:
      if( not (file1['title'] < "2003")):
      #if (file1['title'] == "2003"):
        #print 'title: %s, id: %s' % (file1['title'], file1['id'])
        query = ('\'%s\' in parents and trashed=false' % file1['id'])
        file_list2 = drive.ListFile({'q': query}).GetList()
        for file2 in file_list2:
            #print 'title2: %s, id2: %s' % (file2['title'], file2['id'])
            query2 = ('\'%s\' in parents and trashed=false' % file2['id'])
            file_list3 = drive.ListFile({'q': query2}).GetList()
            for file3 in file_list3:
                #print 'title3: %s, id3: %s' % (file3['title'], file3['id'])
                query3 = ('\'%s\' in parents and trashed=false' % file3['id'])
                file_list4 = drive.ListFile({'q': query3}).GetList()
                for file4 in file_list4:
                    if ( not (file4['title'] == ".DS_Store" or file4['title'] == "Icon\r" or file4['title'] == "Icon")):
                        date = file4['title']
                        date = date[0:6]
                        fileid = file4['id']

                        for key in file4.keys() :
                           if (key == 'thumbnailLink'):
                              thumbnail = file4[key]

                        directlink = file4['alternateLink']

                        for key in file4.keys() : #need this or else will end prematurely for some years
                           if (key == 'webContentLink'):
                              downloadlink = file4[key]

                        print 'date: %s' % date
                        print 'file id: %s' % fileid
                        print 'thumbnail: %s' % thumbnail
                        print 'directlink: %s' % directlink
                        print 'downloadlink: %s' % downloadlink
                        print 'page num: %s' % (file4['title']) #note they do not always in order
                        print "\n"



                        #print 'title: %s, id: %s' % (file4['title'], file4['id'])





def main():
    #gdrive = GDrive()
    #pop_test()
    res = archive_collection.find(
        { '$text': { '$search': "office depot" } },
        { 'url': 1,'score' : { '$meta': 'textScore' }}
    ).sort([('score', {'$meta': 'textScore'})])
    l = list(res)
    print dumps(l)


if __name__ == "__main__":
    main()

#for file_list in drive.ListFile():
#  print 'Received %s files from Files.list()' % len(file_list) # <= 10
#  for file1 in file_list:
#    print 'title: %s, id: %s' % (file1['title'], file1['id'])
