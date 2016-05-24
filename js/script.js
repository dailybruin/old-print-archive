function main() {
  //init
  loadHeader();
  var $searchBtn = $("#searchBtn");
  var searchMenuContent = $("#searchMenu").html();
  $searchBtn.popover({
    html: true,
    content: searchMenuContent
  });

}

function loadHeader() {
  $('#logo').fadeIn(1000, function(){
      //wait for .7 second before fading in "print archive"
      setTimeout(function(){
          $('#archive').animate({
              opacity:1
          },function(){
              //wait for .7 seconds before fading in
              setTimeout(function(){
                  $('#divider').animate({
                      opacity:1,
                      top:-5
                  },900,function(){
                      $('.intro a').fadeIn();
                      $('.intro h4').fadeIn();
                  });
              },500);
          });
      },500);
  });
}

$(function() {
  main();
});
