var routes = {
  '/': '#main',
  '/new-event': '#new-event',
  '/summary': '#summary'
};

var remote = 'localhost';

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
    changeSection(href);
  });

  $('#new-event .add-row').on('click', function(ev) {
    ev.preventDefault();
    var $newRow = $('#new-event .from').last().clone();
    $('#new-event .from').last().after($newRow);
  });

  $('#new-event [type=submit]').on('click', function(ev) {
    ev.preventDefault();

    var rows = [];

    $fromRows = $('#new-event .from');
    $toInput = $('#new-event .to input[name=to]');

    $fromRows.each(function() {
      rows.push({
        from: $('input[name=from]', this).val(),
        amount: $('input[name=amount]', this).val(),
        to: $toInput.val()
      });
    });

    $.post(remote + '/event', JSON.stringify(rows));
  });

});

window.onpopstate = function() {
  console.log('popstate');
  var href = document.location.hash;
  changeSection(href);
};

function changeSection(href) {
    history.pushState({}, "", '#' + href);
    var selector = routes[href];
    $currentSection.hide();
    $currentSection = $(selector).show();
}
