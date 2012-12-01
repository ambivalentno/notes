if (!django) {var django = {
    "jQuery": jQuery};
};

  

(function($) {

    $.fn.charCount = function(options){    
        
        function calculate(obj){
            var count = $(obj).val().length;
            $(obj).next().html(count);
        };
                
        this.each(function() {              
            $(this).after('<p>' +'</>');
            calculate(this);
            $(this).keyup(function(){calculate(this)});
            $(this).change(function(){calculate(this)});
        });
      
    };

})(django.jQuery);

(function() {

$('form').ajaxForm({
    target: '#ajaxwrapper'
}); 
})(); 
