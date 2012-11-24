
  
(function() {

$('form').ajaxForm({
    success: function(xhr) {
        status.html(xhr.responseText);
    },
    target: '#ajaxwrapper'
}); 
})(); 