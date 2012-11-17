
  
    $(function() {
        $("#contactform").bind("submit", function(e) {
            var form = jQuery("#contactform");
            e.preventDefault(); 
            $("#sendbutton").attr('disabled', true)
            $("#sending").toggle()
            $("#ajaxwrapper").load(
                form.attr('action'),
                form.serializeArray(),
                function(responseText, responseStatus) {
                    $("#sendbutton").attr('disabled', false)
                    $("#sending").toggle()
                });
        });
    });
