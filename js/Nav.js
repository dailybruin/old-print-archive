function setUpNavBar() {
  var $searchEndDate = $("#search-end-date");
  var $searchField = $("#search-field");
  var $searchText = $("#search-text");
  var $searchDate = $("#search-start-date");

  var $searchBtn = $("#searchBtn");
  var searchMenuContent = $("#searchMenu").html();

  $searchBtn.popover({
    html: true,
    content: searchMenuContent
  });


  var d = new Date(Date.now());
  $searchEndDate.attr("placeholder", d.getMonth() + "/" + d.getDay() + "/" + d.getFullYear());

  $searchField.submit(function(e){
    e.preventDefault();
    //navigate to search page,
    //if on search page, change/update the results
  });
}

$(function(){
  setUpNavBar();
});
