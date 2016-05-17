import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#Pdf Miner Dependencies
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

from multiprocessing import Process, Queue
#from threading import Thread, local
import urllib
import re

#db init
user = raw_input("Username: ")
pw = raw_input("Password: ")
year = raw_input("Year: ")

if not os.path.exists('dl'):
    os.makedirs('dl')

client = MongoClient('mongodb://' + user + ':' + pw + '@45.55.184.137:27017/db-archive', connect=False)


db = client.get_default_database()
archive_collection = db.test_archive_collection

q = Queue()
#dq = Queue() #download queue
#threadLocal = local()


def yearlookup(x):
    return {
        '2003': '0B9y1-prT44zAMjRjNXNEYlFPelk',
        '2004': '0B9y1-prT44zAQUV5eVRJZHhpcWM',
        '2005': '0B9y1-prT44zANGMxU3VHTnBpek0', 
        '2006': '0B9y1-prT44zAZW5YYkVWR1lBRVU',
        '2007': '0B9y1-prT44zAT2JvalFwQlZid1E', 
        '2008': '0B9y1-prT44zAdE1BNUQ3RlY1b28',
        '2009': '0B9y1-prT44zAeExhdGVfYm1FVE0', 
        '2010': '0B9y1-prT44zAdU16d0lNOGFNYzA',
        '2011': '0B9y1-prT44zAUjhkc2dlY05fLVU', 
        '2012': '0B9y1-prT44zAVzlCTE9qMzRFZjA',
        '2013': '0B9y1-prT44zASG9vQUdVYXBybFk', 
        '2014': '0B9y1-prT44zAQXhPRGFRTUVJVkE',
        '2015': '0B9y1-prT44zAcVlwYlRFdGR3MWs', 
        '2016': '0B9y1-prT44zAeUVUNDg4UFdvU3M'
    }[x]


def pdfWorker():
    while True:
        d = q.get()
        if d is None:
            break;
        d.test_format_and_upload()

class Doc:
    def __init__(self, directLink, downloadLink, thumbnail, date, page, docsFileId):
        self.directLink = directLink
        self.downloadLink = downloadLink
        self.thumbnail = thumbnail
        self.month = date.month
        self.day = date.day
        self.year = date.year
        self.page = page
        self.date = date
        self.docsFileId = docsFileId

    def downloadFile(self, drive):
        if archive_collection.find_one({"docsFileId": self.docsFileId}):
            print "File already indexed! Done!"
            return False
        else:
            print "Downloading " + self.downloadLink + " ..."
            self.filedir = "dl/" + self.docsFileId
            try:
                f = drive.drive.CreateFile({'id': self.docsFileId})
                f.GetContentFile(self.filedir)
            except:
                print "!!!! Error downloading file:" + self.filedir
                print "!!!! Error found for: " + self.docsFileId
                print "!!!! DirectLink: " + self.directLink
                print "!!!! Skipping...\n"
                return False
            return True


    def test_format_and_upload(self):
        #urllib.urlretrieve(self.downloadLink, filedir)
        try:
            raw_text = convert_pdf_to_txt(self.filedir)
        except:
            print "!!!! Error parsing file:" + self.filedir
            print "!!!! Error found for: " + self.docsFileId
            print "!!!! DirectLink: " + self.directLink
            print "!!!! Skipping...\n"
            return
            #raise
        post = {
            "directLink": self.directLink,
            "downloadLink": self.downloadLink,
            "thumbnail": self.thumbnail,
            "day": self.day,
            "month": self.month,
            "year": self.year,
            "page": self.page,
            "date": datetime.datetime(self.year, self.month, self.day),
            "docsFileId": self.docsFileId,
            "text": raw_text
        }
        print "Done! Now inserting to DB..."
        archive_collection.insert_one(post)
        #this seems to impede perf for some reason
        #try:
        #    archive_collection.insert_one(post)
        #except:
        #    print "!!!! File already indexed:" + self.filedir
        #    print "!!!! Error found for: " + self.docsFileId
        #    print "!!!! DirectLink: " + self.directLink
        #    print "!!!! Skipping...\n"
        os.remove(self.filedir)

class GDrive:
    def __init__(self):
        self.gauth = GoogleAuth()
        self.gauth.LoadCredentialsFile("cred.txt")
        if self.gauth.credentials is None:
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            self.gauth.Refresh()
        else:
            self.gauth.Authorize()
        self.gauth.SaveCredentialsFile("cred.txt")

        self.drive = GoogleDrive(self.gauth)

    def iteratePdfs(self):
        yearid = yearlookup(year);
        query = ('\'%s\' in parents and trashed=false' % yearid)
        print year,  yearid
        file_list = self.drive.ListFile({'q': query}).GetList()

        for file1 in file_list: #months
            print 'title2: %s, id2: %s' % (file1['title'], file1['id'])
            query2 = ('\'%s\' in parents and trashed=false' % file1['id'])
            file_list3 = self.drive.ListFile({'q': query2}).GetList()
            for file3 in file_list3:
                print 'title3: %s, id3: %s' % (file3['title'], file3['id'])
                query3 = ('\'%s\' in parents and trashed=false' % file3['id'])
                file_list4 = self.drive.ListFile({'q': query3}).GetList()
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

                        #d = Doc(url=downloadlink, )
                        
                        try:
                            dt = dparser.parse(date,fuzzy=True).date()
                        except:
                            print "\n!!!! DATE NOT FOUND Error found for: " + fileid
                            print "!!!! DirectLink: " + directlink
                            print "!!!! Skipping...\n"
                            continue

                        try:
                            #pn = int(file4['title'][11:13])
                            pn = int(re.search('(?<=page)\d+', file4['title']).group(0))
                        except:
                            try:
                                pn = int(re.search('(?<=pageA)\d+', file4['title']).group(0))
                            except:
                                try:
                                    pn = int(re.search('(?<=pageB)\d+', file4['title']).group(0))
                                except:
                                    print "\n!!!! PAGE NOT FOUND Error found for: " + fileid
                                    print "!!!! DirectLink: " + directlink
                                    print "!!!! DEFAULTING TO PAGE 0...\n"
                                    pn = 0

                        d = Doc(directLink=directlink, downloadLink=downloadlink, thumbnail=thumbnail,date=dt,page=pn, docsFileId=fileid)

                        if d.downloadFile(self):
                            q.put(d)
                            print 'Queued ' + date + ' page: %s' % pn
                            #print 'Total items: %s \n' % q.qsize()
                        else:
                            continue
                            
                        #print 'date: %s' % date
                        #print 'file id: %s' % fileid
                        #print 'thumbnail: %s' % thumbnail
                        #print 'directlink: %s' % directlink
                        #print 'downloadlink: %s' % downloadlink
                        #print 'page num: %s' % (file4['title']) #note they do not always in order
                        #print "\n"
                        #print 'title: %s, id: %s' % (file4['title'], file4['id'])


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

def pop_test():
     ls = os.listdir("testfiles")
     docs = []
     for i, f in enumerate(ls):
         path = "testfiles/" + f
         d = Doc(path, 1, 6, 2003, i+1)
         docs.append(d)
     map(lambda d: d.test_format_and_upload(), docs)

def search(query):
    #gdrive = GDrive()
    #pop_test()
    res = archive_collection.find(
        { '$text': { '$search': "query" } },
        { 'url': 1,'score' : { '$meta': 'textScore' }}
    ).sort([('score', {'$meta': 'textScore'})]).limit(20)[0:20]
    l = list(res)
    print dumps(l)

def main():
    threads = []
    num_worker_threads = 4
    drive = GDrive()

    for i in range(num_worker_threads):
        t = Process(target=pdfWorker)
        t.start()
        threads.append(t)

    drive.iteratePdfs()

    q.join()
    for i in range(num_worker_threads):
        q.put(None)
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()

#for file_list in drive.ListFile():
#  print 'Received %s files from Files.list()' % len(file_list) # <= 10
#  for file1 in file_list:
#    print 'title: %s, id: %s' % (file1['title'], file1['id'])
