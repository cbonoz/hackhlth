$(function () {
  'use strict'

  $('[data-toggle="offcanvas"]').on('click', function () {
    $('.row-offcanvas').toggleClass('active')
  })
})

 $(document).ready(function(){
        $('.dropdown-toggle').dropdown()
    });



// stickynav
$(window).bind('scroll', function () {

    if ($(window).scrollTop() > 100)
        $('.mainmenu').addClass('nav-down');
    else
        $('.mainmenu').removeClass('nav-down');
});


// Hide Header on on scroll down
var lastScrollTop = 0;
var delta = 5;
var navbarHeight = $('.mainmenu').outerHeight();

$(window).scroll(function(event){

    var st = $(this).scrollTop();

    // Make sure they scroll more than delta
    if(Math.abs(lastScrollTop - st) <= delta)
        return;

    // If they scrolled down and are past the navbar, add class .nav-up.
    // This is necessary so you never see what is "behind" the navbar.
    if (st > lastScrollTop && st > navbarHeight){
        // Scroll Down
        $('.mainmenu').removeClass('nav-down').addClass('nav-up');
    } else {
        // Scroll Up
        if(st + $(window).height() < $(document).height()) {
            $('.mainmenu').removeClass('nav-up');
        }
    }

    lastScrollTop = st;
});