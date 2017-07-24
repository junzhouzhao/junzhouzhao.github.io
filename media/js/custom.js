
$(document).ready(function() {
    $(window).scroll(function(){
      $("#rightmenu").stop().animate({"marginTop": ($(window).scrollTop()) + "px", "marginLeft":($(window).scrollLeft()) + "px"}, "fast" );
    });
});