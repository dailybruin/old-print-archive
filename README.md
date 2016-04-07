# print-archive
Redo of Sam's print-archive site : http://samhoff.github.io/archive/

Basically, the Daily Bruin's print archives are available in two formats:
1915-2002: Scans stored at archive.org in 200 "reels" uploaded by the UCLA Library; accessible by downloading large (700mb) PDFs or by using archive.org's lazy loading viewer that allows text searching within the scanned documents
2003-2016: PDFs stored in a Google Drive folder under editor@media.ucla.edu; updated every night by the Copy department


The goal of the site is to have one place where a reader can easily access the day's paper from any day in our history. The tricky thing is, some of the archive.org reels cover multiple years, while others cover only a few months; and there's no way to know the start or end dates without going through them manually. Additionally, searching for a date in the middle of the reel, which contains different newspapers of different page lengths, is a challenge. The Google Drive folder also grows nightly.


Major things to rebuild:

-A way of indexing the reels that makes sense. In Sam's repo, he named a bunch of points within each reel including a "start" point; if a user enters a date after the one named in script.js then their browser will take them to the corresponding reel. 

-A way to search that is at least as good as the current search capabilities. Currently you can pick a date, then search in the archive.org viewer and it will search within the reel you're currently looking at. 

-Make the site prettier

-There should be an emphasis on getting folks to pay for this old copyrighted content. Maybe we could disable download unless folks pay (doesn't need to mean we implement a payment system; just link to our download site) or have a popup after 5 minutes saying that to continue you should donate to DB. 
