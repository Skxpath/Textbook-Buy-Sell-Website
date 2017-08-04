function searchSuccess(data, textStatus, jqXHR) {
  $('#search_results').html(data);
}

var vm = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!',
    isTextbookFormShown: false,
  },
  methods: {
    toggleTextbookForm: function() {
      this.isTextbookFormShown = !this.isTextbookFormShown;
    },
    searchTextbooks: function() {
      $.ajax({
        type: 'POST',
        url: '/textbook/textbook_search',
        data: {
          'search_text': $('#search').val(),
          'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: searchSuccess,
        dataType: 'html',
      });
    },
  },
  // Lets us use vue templates with different brackets. Ex: [data] instead of the default {{data}}
  // This is because the default brackets conflicts with django's templating system
  delimiters: ["[", "]"],
});
