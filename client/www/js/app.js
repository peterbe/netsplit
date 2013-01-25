
/* Main */
define(function(require) {
  var $ = require('zepto');
  require('./install-button');
  require('./utils');

  var routes = {
    '/': { controller: main, section: '#main' },
    '/new-event': { controller: new_event, section: '#new-event' },
    '/summary': { controller: summary, section: '#summary' }
  };

  var STATE;
  //var remote = 'http://localhost:5000';
  var remote = 'http://www.peterbe.com:5000';

  var $currentSection = null;


  /* Views */
  function main() {
  }

  function summary() {
    $ul = $currentSection.find('ul').html('');

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
    summary();
    console.log(STATE);
  });

  window.onpopstate = function() {
    console.log('popstate');
    var href = document.location.hash;
    changeSection(href);
  };


  /* View switching */
  $currentSection = $('#main');

  var order = ['main', 'new-event', 'summary'];

  for (var i=0; i<order.length; i++) {
    var section = order[i];
    if (section != 'main') {
      $('#' + section).addClass(rel(section, 'main'));
    }
  }

  $('section').show();

  function rel(s1, s2) {
    var i1 = order.indexOf(s1);
    var i2 = order.indexOf(s2);

    return i1 > i2 ? 'right' : 'left';
  }

  function changeSection(href) {
    var route = routes[href];

    if (route.section) {
      var $oldSection = $currentSection;
      var $newSection = $(route.section);

      var oldId = $oldSection.attr('id');
      var newId = $newSection.attr('id');

      $oldSection.addClass(rel(oldId, newId));
      $newSection.removeClass(rel(newId, oldId));
      $currentSection = $newSection;
    }

    if (route.controller) {
      routes[href].controller();
    }

    history.pushState({}, "", '#' + href);
  }

});
