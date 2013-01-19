var routes = {
  '/new-event': '#new-event',
  '/summary': '#summary'
};

var $currentSection = null;

define(function(require) {
  var $ = require('zepto');
  require('./install-button');

  // Write your app here.

  $currentSection = $('#main').show();

  $('#main .nav').on('click', function(ev) {
    ev.preventDefault();
    var $this = $(this);
    var href= $this.attr('href');
    history.pushState({}, "", href);
    var selector = routes[href];
    $currentSection.hide();
    $currentSection = $(selector).show();
  });

});
