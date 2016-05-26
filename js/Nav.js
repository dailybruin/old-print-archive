function bindSearchFormHandlers() {
  var $searchEndDate = $("#search-end-date");
  var $searchStartDate = $("#search-start-date");
  var $searchText = $("#search-text");

  $searchStartDate.datepicker({
    startDate: "09/10/1915",
    endDate: Date(Date.now()),
    defaultViewDate: { year: 1915, month: 09, day: 10 }
  });

  $searchEndDate.datepicker({
    startDate: "09/10/1915",
    endDate: Date(Date.now())
  });

  $("#search-field").submit(function(e){
    e.preventDefault();
    if(NProgress)
      NProgress.done();
    doSearch($searchText.val(), $searchStartDate.datepicker('getDate'), $searchEndDate.datepicker('getDate'));
  });
};

function setUpNavBar() {
  var $searchBtn = $("#searchBtn");
  var $searchEndDate = $("#search-end-date");

  var d = new Date(Date.now());
  $searchEndDate.attr("placeholder", d.getMonth() + "/" + d.getDay() + "/" + d.getFullYear());

  var searchMenuContent = $("#searchMenu").html();
  $("#searchMenu").remove();
  $searchBtn.popover({
    html: true,
    content: searchMenuContent
  });

  $searchBtn.on('shown.bs.popover', bindSearchFormHandlers);
}

$(function(){
  setUpNavBar();
});
