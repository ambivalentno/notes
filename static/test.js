
function somef(inputa,outputa){
    $("#"+inputa).keyup(function(){
        var i = $("#"+inputa).val().length;
        $("#"+outputa).val(i);
    });
}
