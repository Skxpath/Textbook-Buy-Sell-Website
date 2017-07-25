searchSuccess = function(data) {
  $('#search-results').html(data)

  // Wire up previous and next buttons to also make ajax requests
  var previousPageButton = $('#previous-page');
  previousPageButton.on('click', function() {
    search(searchSuccess, "?page=" + previousPageButton.attr('data-page-number'));
  });

  var nextPageButton = $('#next-page');
  nextPageButton.on('click', function() {
    search(searchSuccess, "?page=" + nextPageButton.attr('data-page-number'));
  });
}
search = function(callback, args) {
  $.ajax({
    type: 'GET',
    url: $('#search-form').attr('data-search-url') + (args ? args : ''),
    data: {
      'search_text': $('#ad-search-text').val(),
      'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
    },
    success: callback,
    dataType: 'html',
  });
}

$(document).ready(function() {
  $('#ad-search-button').on('click', function() {
    search(searchSuccess);
  });

  $('#search-form').on('submit', function(event) {
    // prevent the page from reloading when submitting the form
    // This happens if the user hits enter in the search field
    event.preventDefault();
    search(searchSuccess);
  });
});
