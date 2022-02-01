(function($) {
  // Cycle through sidebar items
  function displayLoop() {
    // find the current item
    var current = $('.lw_widget_events li.active');

    var next = current.next().length ? current.next() : current.parent().children(':first');
    // display the next item
    current.children('.lw_events_detail, .lw_item_thumb').fadeOut(500,function(){
      next.addClass('active').children('.lw_events_detail, .lw_item_thumb').fadeIn(1000);
      current.removeClass('active');
    });
    // repeat after 5 seconds
    setTimeout(displayLoop,6000);
  }

  // Display the first sidebar item when the page loads, then call the display loop method
  $('.lw_widget_events li:first-child').addClass('active').children('.lw_events_detail, .lw_item_thumb').fadeIn('slow').delay(6000, 'displayQueue').queue('displayQueue', function(){ 
    displayLoop();
  }).dequeue('displayQueue');
} (livewhale.jQuery));
