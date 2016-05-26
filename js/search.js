function doSearch(queryString, startDateDate, endDateDate, page) {
  if(window.location.pathname.includes("search")) {
    NProgress.start();
    var webArchiveUrlString = startDateDate && startDateDate.getTime ? WebArchive.getArchiveSrcFromDate(startDateDate) : null;

    console.log(webArchiveUrlString);
    if(webArchiveUrlString) {
      //old stuff



    } else {
      //new stuff

    }


  } else {
    //redirect
    var args = {
      "query": queryString ? queryString : "",
      "startDate": startDateDate && startDateDate.getTime ? startDateDate.getTime()/1000 : null,
      "endDate": endDateDate && endDateDate.getTime ? endDateDate.getTime()/1000 : null,
      "page": 1
    };

    window.location.href = "/search?" + $.param(args);
  }

}

function searchPageInit() {
  var q = $.QueryString;
  q.startDate = new Date(q.startDate*1000);
  q.endDate = new Date(q.endDate*1000);
  doSearch(q.query, q.startDate, q.endDate, q.page);
}

$(function() {
  if (window.location.pathname.includes("search"))
    searchPageInit();

});
