function searchSuccess(data, textStatus, jqXHR) {
  $('#search_results').html(data);
}

var vm = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!',
    isTextbookFormShown: false,
    textbookIsbn: '',
    textbookTitle: '',
    textbookAuthor: '',
    showTextbookInfoNotFound: false,
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
      this.textbookAuthor = '';
      this.textbookTitle = '';
      this.showTextbookInfoNotFound = false;

      $.get('/textbook/get_textbook_info_by_isbn/'+this.textbookIsbn, function(data){
        let bookInfo = data[Object.keys(data)[0]];
        if(bookInfo){
          if (bookInfo.authors && bookInfo.authors.length > 0){
            this.textbookAuthor = bookInfo.authors[0].name;
          }
          else{
            this.showTextbookInfoNotFound = true;
          }
          if (bookInfo.title){
            this.textbookTitle = bookInfo.title;

            if (bookInfo.subtitle){
              this.textbookTitle += ' '+bookInfo.subtitle;
            }
          }
          else{
            this.showTextbookInfoNotFound = true;
          }
        }
        else{
          this.showTextbookInfoNotFound = true;
        }
      }.bind(this));
    }
  },
  // Lets us use vue templates with different brackets. Ex: [data] instead of the default {{data}}
  // This is because the default brackets conflicts with django's templating system
  delimiters: ["[", "]"],
});
