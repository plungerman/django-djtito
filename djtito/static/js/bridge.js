$(function() {
  // Cycle through sidebar items
  function displayLoop() {
    // find the current item
    var current = $('.lw_widget_news li.active');
    var next = current.next().length ? current.next() : current.parent().children(':first');
    // display the next item
    current.fadeOut(500,function(){
      next.addClass('active').fadeIn(500);
      current.removeClass('active');
    });
    // repeat after 5 seconds
    setTimeout(displayLoop, 10000);
  }

  // Display the first sidebar item when the page loads, then call the display loop method
  $('.lw_widget_news li:first-child').addClass('active').fadeIn('slow').delay(10000, 'displayQueue').queue('displayQueue', function(){
    displayLoop();
  }).dequeue('displayQueue');
});
