# This will split the pdf by page and output to a pdf 
# named document-pagenumber.pdf. 
# TO DO (BASIC): 
# 1. Ouput pdf to google drive folder instead of local directory
# 2. Put PDF into folder named "month-day-year" based on date on top of PDF
# 	 (ie somehow need analyze pdf and get date of the paper and put this
#     into a google drive folder)



from PyPDF2 import PdfFileWriter, PdfFileReader

inputpdf = PdfFileReader(open("ucladailybruin191losax.pdf", "rb"))

for i in xrange(inputpdf.numPages):
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    with open("document-page%s.pdf" % i, "wb") as outputStream:
        output.write(outputStream)
