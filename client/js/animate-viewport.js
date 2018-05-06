$( document ).ready(function() {
// * VIEWPORT ANIMATION
// Start animations when element appears in viewpoint
// JS: components/jquery.viewportchecker.js
$(".viewpoint-fadeIn").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeIn'
});
$(".viewpoint-fadeInLeft").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeInLeft'
});
$(".viewpoint-fadeInRight").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeInRight'
});
$(".viewpoint-fadeInUp").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeInUp'
});
$(".viewpoint-fadeInDown").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeInDown'
});

// ** Delays
// - Up
$(".viewpoint-fadeInUp-delay1").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeInUp delay1'
});
$(".viewpoint-fadeInUp-delay2").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeInUp delay2'
});
$(".viewpoint-fadeInUp-delay3").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeInUp delay3'
});
$(".viewpoint-fadeInUp-delay4").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeInUp delay4'
});
$(".viewpoint-fadeInUp-delay5").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeInUp delay5'
});

// - Left
$(".viewpoint-fadeInLeft-delay1").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeInLeft delay1'
});

// - In
$(".viewpoint-fadeIn-delay1").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeInDown delay1'
});
$(".viewpoint-fadeIn-delay2").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeInDown delay2'
});
$(".viewpoint-fadeIn-delay3").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeInDown delay3'
});
$(".viewpoint-fadeIn-delay4").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeInDown delay4'
});
$(".viewpoint-fadeIn-delay5").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeInDown delay5'
});

// Inset
$(".viewpoint-fadeInSet-delay1").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeIn delay1'
});
    $(".viewpoint-fadeInSet-delay2").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeIn delay2'
});
    $(".viewpoint-fadeInSet-delay3").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeIn delay3'
});
$(".viewpoint-fadeInSet-delay4").viewportChecker({
  classToRemove: 'invisible',
  classToAdd: 'animated fadeIn delay4'
});

// -Zoom
$(".viewpoint-zoomIn").viewportChecker({
  classToAdd: 'animated zoomIn'
});
// * END VIEWPORT ANIMATIONS
});