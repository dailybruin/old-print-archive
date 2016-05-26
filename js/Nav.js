function bindSearchFormHandlers() {
  $("#search-field").submit(function(e){
    e.preventDefault();
    console.log("dsfdssdf");
    //navigate to search page,
    //if on search page, change/update the results
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
