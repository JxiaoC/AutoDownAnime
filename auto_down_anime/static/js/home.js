var home = {
    
};

$('#url').unbind().keydown(function(event){
        if (event.keyCode == 13){
            all.go($('#url').val(),true)
        }
    });

$('body').unbind().keydown(function(event){
    $('#url').focus();
    });

$('#url').focus();
// end_sub