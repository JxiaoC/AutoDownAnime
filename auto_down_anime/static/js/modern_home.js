function adaptive() {
    $(".roll-list ul li").css("height", $(".recommend").height());
}

$('#go').unbind('keydown').keydown(function (event) {
    if (event.keyCode == 13) {
        all.go($('#go').val(), true);
    }
});

$('body').unbind().keydown(function (event) {
    $('#go').focus();
});

$('#go').focus();
common.show_hitokoto(10000, 'hitokoto');

$('.roll-list ul').Roll(5000);

adaptive();
common.load_dongcidaci();

window.onresize = function () {
    adaptive();
};

window.onload = function () {
    adaptive();
    $('.links').css('left', $(window).width() - $('.links').width() - 50).mouseenter(function(){
        $('.links').css('left', $(window).width() - $('.links').width() - 50);
    }).mouseleave(function(){
        $('.links').css('left', '99.5%');
    });
    setTimeout(function(){$('.links').css('left', '99.5%');}, 3000);
};