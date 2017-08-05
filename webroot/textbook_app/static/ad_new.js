function searchSuccess(data, textStatus, jqXHR) {
  $('#search_results').html(data);
}

function infoRetrievalSuccess(data, textStatus, jqXHR) {

}

var vm = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!',
    isTextbookFormShown: false,
    textbookIsbn: '',
    textbookTitle: '',
    textbookAuthor: '',
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
    getTextbookInfo: function() {
      $.ajax({
        type: 'GET',
        dataType: 'json',
        url: '/textbook/get_textbook_info_by_isbn',
        success: function(data){
          var parsedData = JSON.parse(data);
          if (parsedData.author){
            this.textbookAuthor = parsedData.author;
          }
          if (parsedData.title){
            this.textbookTitle = parsedData.title;
          }
        }
      })
    }
  },
  // Lets us use vue templates with different brackets. Ex: [data] instead of the default {{data}}
  // This is because the default brackets conflicts with django's templating system
  delimiters: ["[", "]"],
});
