var setI_set_4x4_location;

function show_4x4_modern() {
    set_4x4_location();
}

function set_4x4_location() {
    if($(".js-4x4").length == 0)return;
    var _left = $(".js-4x4")[0].getBoundingClientRect().x - $(".modern_main")[0].getBoundingClientRect().x + 'px';
    var _top = $(".js-4x4")[0].getBoundingClientRect().y - $(".modern_main")[0].getBoundingClientRect().y + 'px';
    $(".modern.wh2").css({ 'left': _left, 'top': _top });
}

function load_modern_name() {
    $(".modern[data-name]").each(function (i, self) {
        var name = $(self).data('name');
        $(self).append('<div class="name">{name}</div>'.format({ name: name }));
    });
}

function load_modern_href() {
    $(".modern[data-href]").each(function (i, self) {
        var href = $(self).data('href');
        $(self).unbind().click(function () { common.openUrl(href); })
    });
}

function show_main() {
    if($(window).width() <=1400){
        $('.main').css({'top': '60%', 'opacity': 1});
    }
    else {
        $('.main').css({'top': '50%', 'opacity': 1});
    }
    // $('.main').css({'width': $('.modern_main').width() + $('.download_main').width() + 50});
}



(function ($) {
    $.fn.Roll = function (time) { //Win10 磁贴滚动效果
        if (!time) time = 3000;
        var This = this;
        var NowHeight = 0;
        var Time = time + Math.random() * 2000;
        setInterval(function () {
            Time = time + Math.random() * 2000;
            var Height = $(This).find("li:eq(0)").height();
            if (NowHeight + Height * 2 > Height * $(This).find("li").length) {
                NowHeight = 0;
                $(This).css("margin-top", "0px");
            }
            else {
                NowHeight += Height;
                $(This).css("margin-top", "-" + NowHeight + "px");
            }
        }, Time);
    }
})(jQuery);

$(document).on("mousewheel DOMMouseScroll", function (e) {

    var delta = (e.originalEvent.wheelDelta && (e.originalEvent.wheelDelta > 0 ? 1 : -1)) ||  // chrome & ie
                (e.originalEvent.detail && (e.originalEvent.detail > 0 ? -1 : 1));              // firefox


    if (delta > 0 && $(window).scrollLeft() > 0) {
        $(window).scrollLeft($(window).scrollLeft()-200);
    } else if (delta < 0) {
        $(window).scrollLeft($(window).scrollLeft()+200);
    }
});

function _init() {
    show_main();
    load_modern_name();
    load_modern_href();
    setTimeout(function () { show_4x4_modern(); }, 300);

    clearInterval(setI_set_4x4_location);
    setI_set_4x4_location = setInterval(function () { set_4x4_location(); }, 10);
    setTimeout(function(){clearInterval(setI_set_4x4_location);}, 2000);
}

$(window).resize(function(){
    show_main();

    clearInterval(setI_set_4x4_location);
    setI_set_4x4_location = setInterval(function () { set_4x4_location(); }, 10);
    setTimeout(function(){clearInterval(setI_set_4x4_location);}, 2000);
});


setTimeout(function () { _init(); }, 1);