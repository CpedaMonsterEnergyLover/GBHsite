$(function () {
  $('[data-toggle="popover"]').popover({
      placement: 'bottom',
      html : true,
        content: function() {
          let content = $(this).attr("data-popover-content");
          return $(content).children(".popover-body").html();
        },
        title: function() {
          let title = $(this).attr("data-popover-content");
          return $(title).children(".popover-heading").html();
        }
  }).on('mouseenter', function () {
    if (!$(this).attr('aria-describedby')) {
      $(this).popover('show');
    }
  }).on('click', function () {
    if ($(this).attr('aria-describedby')) {
      $(this).popover('show');
    }
  }).mouseleave(function () {
      $('[data-toggle="popover"]').each(function () {
      $(this).popover('hide');
    })
  });
});