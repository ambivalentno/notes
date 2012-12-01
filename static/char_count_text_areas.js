
if (!django) {var django = {
    "jQuery": jQuery};
};

django.jQuery(document).ready(function(){

    function calculate(obj){
        var count = django.jQuery(obj).val().length;
        django.jQuery(obj).parent().find('span').html(count);
    };

    django.jQuery('.countable').each(function(index){
        calculate(this);
        django.jQuery(this).keyup(function(){calculate(this)});
        django.jQuery(this).change(function(){calculate(this)});
        })  
    }); 