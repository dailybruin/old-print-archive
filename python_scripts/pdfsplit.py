# This will split the pdf by page and output to a pdf 
# named document-pagenumber.pdf. 
# TO DO (BASIC): 
# 1. Ouput pdf to google drive folder instead of local directory
# 2. Put PDF into folder named "month-day-year" based on date on top of PDF
# 	 (ie somehow need analyze pdf and get date of the paper and put this
#     into a google drive folder)

from PyPDF2 import PdfFileWriter, PdfFileReader
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import unicodedata
import codecs

def analyzepdf( pdftext ):
   normaltext = unicodedata.normalize('NFKD', pdftext).encode('ascii','ignore')
   return normaltext

# Split PDFs

#inputpdf = PdfFileReader(open("ucladailybruin01losa.pdf", "rb"))

#for i in xrange(inputpdf.numPages):
#   output = PdfFileWriter()
#   output.addPage(inputpdf.getPage(i))
#   with open("document-page%s.pdf" % i, "wb") as outputStream:
#       output.write(outputStream)

#End Split PDFs


#This block takes in a pdf document and will convert it to text and put it in a file test.txt


Pdf_File = PdfFileReader(open("document-page3.pdf", "rb"))
for pg_idx in range(0, Pdf_File.getNumPages()):
    page_Content = Pdf_File.getPage(pg_idx).extractText()


f = codecs.open('test.txt', encoding='utf-8', mode='w+')
f.write(page_Content)
f.close()
#End convert to text

#This block is just playing around with Google Drive API. 
'''
# Google Authorizations
gauth = GoogleAuth()
# gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication

#Upload to Google drive
#date = "02-04-1996"

drive = GoogleDrive(gauth) # Create GoogleDrive instance with authenticated GoogleAuth instance

#create folder for each date
file1 = drive.CreateFile(
	{
  'title' : date,
  'mimeType' : 'application/vnd.google-apps.folder'
	}
)

file1.Upload() # Upload it 
print 'title: %s, id: %s' % (file1['title'], file1['id']) # title: Hello.txt, id: {{FILE_ID}}
folderid = file1['id']

file2 = drive.CreateFile(
	{
  		'title' : 'document-page6.pdf',
  		'parents': [{"id": folderid}]
	}
)
file2.SetContentFile('document-page6.pdf') 
file2.Upload()
'''
