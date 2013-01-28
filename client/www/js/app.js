
/* Main */
define(function(require) {
  var $ = require('zepto');
  require('./install-button');
  require('./utils');

  var STATE = [];
  //var remote = 'http://localhost:5000';
  var remote = 'http://ntsp.lt';

  var routes = {
    '/': { controller: main, selector: '#main' },
    '/new-event': { controller: new_event, selector: '#new-event' },
    '/summary': { controller: summary, selector: '#summary' }
  };

  var paneOrder = ['#main', '#new-event', '#summary'];
  var currentPane = null;

  /* Views */
  function main() {
  }

  function summary() {
    $ul = $(currentPane).find('ul').html('');

    $.each(STATE, function() {
      $ul.append('<li>{from} owes {to} ${amount}.</li>'.format(this));
    });
  }

  function new_event() {
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


  $('a.nav').on('click', function(ev) {
    ev.preventDefault();
    var $this = $(this);
    var href= $this.attr('href');
    changePane(href);
  });

  $('a.back').on('click', function(ev) {
    ev.preventDefault();
    window.history.back();
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
    summary();
    console.log(STATE);
  });

  /* View switching */
  window.onpopstate = function() {
    // Chop off leading '#'
    var href = document.location.hash.slice(1)
    if (href === '') {
      href = '/';
    }
    changePane(href, false);
  };

  function rel(s1, s2) {
    var i1 = paneOrder.indexOf(s1);
    var i2 = paneOrder.indexOf(s2);

    return i1 > i2 ? 'right' : 'left';
  }

  function changePane(href, push) {
    if (push === undefined) push = true;
    var route = routes[href];

    var $oldSection = $(currentPane);
    var $newSection = $(route.selector);

    var oldPane = '#' + $oldSection.attr('id');
    var newPane = '#' + $newSection.attr('id');

    $oldSection.addClass(rel(oldPane, newPane));
    $newSection.removeClass(rel(newPane, oldPane));

    routes[href].controller();

    if (push) {
      history.pushState({}, "", '#' + href);
    }
    currentPane = newPane;
  }

  $(function init() {
    console.log('calling init');
    if (document.location.hash.length) {
      var href = location.hash.slice(1);
      currentPane = routes[href].selector;
      window.onpopstate();
    } else {
      currentPane = '#main';
    }

    for (var i=0; i < paneOrder.length; i++) {
      var pane = paneOrder[i];
      if (pane != currentPane) {
        $(pane).addClass(rel(pane, currentPane));
      }
    }

    $('section').show();
  });

});
