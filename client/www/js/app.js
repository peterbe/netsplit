var routes = {
  '/': main,
  '/new-event': new_event,
  '/summary': summary
};

var STATE;
//var remote = 'http://localhost:5000';
var remote = 'http://www.peterbe.com:5000';

var $currentSection = null;


/* Views */
function main() {
  $currentSection.hide();
  $currentSection = $('#main').show();
}

function summary() {
  $currentSection.hide();
  $currentSection = $('#summary').show();
  summaryUpdate();
}

function summaryUpdate() {
  $ul = $currentSection.find('ul').html('');

  $.each(STATE, function() {
    $ul.append('<li>{from} owes {to} ${amount}.</li>'.format(this));
  });
}

function new_event() {
  $currentSection.hide();
  $currentSection = $('#new-event').show();
  $('#new-event .froms').html('');
  newEventAddFromRow();
}

newEventFromRowTemplate =
'<div class="row from">' +
'  <input type="text" name="from" value="{from}" placeholder="Name"/>' +
'  <input type="text" name="amount" value="{amount}" placeholder="$"/>' +
'</div>';

function newEventAddFromRow() {
  var $lastRow = $('#new-event input.from').last();
  var data = {from: '', amount: ''};
  if ($lastRow.length) {
    data['from'] = $lastRow.find('input[name=from]').val();
    data['amount'] = $lastRow.find('input[name=amount]').val();
  }
  var $newRow = $(newEventFromRowTemplate.format(data));
  $('#new-event .froms').append($newRow);
}

define(function(require) {
  var $ = require('zepto');
  require('./install-button');
  require('./utils');

  // Write your app here.

  $currentSection = $('#main').show();

  $('a.nav').on('click', function(ev) {
    ev.preventDefault();
    var $this = $(this);
    var href= $this.attr('href');
    changeSection(href);
  });

  $('#new-event .add-row').on('click', function(ev) {
    ev.preventDefault();
    newEventAddFromRow();
  });

  $('#new-event a.create').on('click', function(ev) {
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
    $.post(remote + '/event', {data: JSON.stringify(rows)}, function(response) {
      console.log('got response');
      STATE = JSON.parse(response);
      $('#new-event').append('Done');
    });
  });

  $.getJSON(remote + '/state', function(data) {
    console.log('loading state');
    console.log(data);
    STATE = data;
    summaryUpdate();
    console.log(STATE);
  });
});

window.onpopstate = function() {
  console.log('popstate');
  var href = document.location.hash;
  changeSection(href);
};

function changeSection(href) {
  history.pushState({}, "", '#' + href);
  routes[href]();
}
