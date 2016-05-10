from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import dateutil.parser as dparser
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

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

    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
      print 'title: %s, id: %s' % (file1['title'], file1['id'])



main()

#gauth = GoogleAuth()
#gauth.LocalWebserverAuth()
#drive = GoogleDrive(gauth)

#for file_list in drive.ListFile():
#  print 'Received %s files from Files.list()' % len(file_list) # <= 10
#  for file1 in file_list:
#    print 'title: %s, id: %s' % (file1['title'], file1['id'])
