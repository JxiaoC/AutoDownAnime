$(document).ready(function () {
    all.replace_fence();
    $("img.lazy").lazyload({ effect: "fadeIn" });
    var $window = $(window);
    var starting = {};
    $window.load(function () {
        $('.preloader').fadeOut();
        $('.preloader-area').delay(350).fadeOut('slow');
    });
});

var PageTransitions = (function () {

    var $main = $('#pt-main'),
        $pages = $main.children('div.pt-page'),
        $iterate = $('#iterateEffects'),
        animcursor = 1,
        pagesCount = $pages.length,
        current = 0,
        isAnimating = false,
        endCurrPage = false,
        endNextPage = false,
        animEndEventNames = {
            'WebkitAnimation': 'webkitAnimationEnd',
            'OAnimation': 'oAnimationEnd',
            'msAnimation': 'MSAnimationEnd',
            'animation': 'animationend'
        },
        // animation end event name
        animEndEventName = animEndEventNames[Modernizr.prefixed('animation')],
        // support css animations
        support = Modernizr.cssanimations;

    function init() {

        $pages.each(function () {
            var $page = $(this);
            $page.data('originalClassList', $page.attr('class'));
        });
        // $pages.eq(current).addClass('pt-page-current');
    }

    function ok(animation) {
        return !isAnimating;
    }

    function nextPage(animation) {

        if (isAnimating) {
            return false;
        }

        isAnimating = true;

        var $currPage = $pages.eq(current);

        if (current < pagesCount - 1) {
            ++current;
        }
        else {
            current = 0;
        }

        var $nextPage = $pages.eq(current).addClass('pt-page-current'),
            outClass = '', inClass = '';

        switch (animation) {
            case 1:
                outClass = 'pt-page-rotateCarouselLeftOut pt-page-ontop';
                inClass = 'pt-page-rotateCarouselLeftIn';
                break;
            case 0:
                outClass = 'pt-page-rotateCarouselRightOut pt-page-ontop';
                inClass = 'pt-page-rotateCarouselRightIn';
                break;

        }

        $currPage.addClass(outClass).on(animEndEventName, function () {
            $currPage.off(animEndEventName);
            endCurrPage = true;
            if (endNextPage) {
                onEndAnimation($currPage, $nextPage);
            }
        });

        $nextPage.addClass(inClass).on(animEndEventName, function () {
            $nextPage.off(animEndEventName);
            endNextPage = true;
            if (endCurrPage) {
                onEndAnimation($currPage, $nextPage);
            }
        });

        if (!support) {
            onEndAnimation($currPage, $nextPage);
        }

    }

    function onEndAnimation($outpage, $inpage) {
        endCurrPage = false;
        endNextPage = false;
        resetPage($outpage, $inpage);
        isAnimating = false;
    }

    function resetPage($outpage, $inpage) {
        $outpage.attr('class', $outpage.data('originalClassList'));
        $inpage.attr('class', $inpage.data('originalClassList') + ' pt-page-current');
    }

    init();

    return {init: init, nextPage: nextPage, ok: ok};

})();
var loading =false;

function get_data(page) {
    if(loading) return;
    loading =true;
    history.pushState({}, document.title, '/up/id/{upid}/{page}'.format({upid: upid, page: page}));
    var next = page > now_page;
    now_page = page;
    $.get('/api/v1/up/video/{id}/{page}'.format({id: upid, page: page}), function (data) {
        var html = '';
        for (var i in data.res.list) {
            var _ = data.res.list[i];
            html += '<div class="info"><a target="_blank" href="/video/av{av}"><img src="{img}" onerror="javascript: this.src = \'/static/img/itai.jpg\';"/><span class="title" title="{title}">{title}</span></a></div>'.format({
                av: _['id'],
                img: _['img'],
                title: _['title'],
            })
        }
        html += gen_page(data['count']);
        next && PageTransitions.nextPage(1) || PageTransitions.nextPage(0);
        $('.pt-page .ro').html('');
        $('.pt-page.pt-page-current .ro').html(html);

        if (page == 1){
            $('.up-name').text(data.res.upinfo.author);
            $('.up-sign').text(data.res.upinfo.sign);
            $('.up-avatar img').attr('src', data.res.upinfo.avatar);
            document.title = data.res.upinfo.author + '-唧唧-bilibili视频|弹幕在线下载';
        }

        bind_page();
        loading = false;
    }).error(function(){loading=false;});
}

function gen_page(count) {
    var html = '<div class="pages">';
    var max_page = count / 12 + (count % 12 === 0 ? 0 : 1);
    if (now_page > 1) {
        html += '<span data-page="' + (now_page - 1) + '"><</span>';
    }

    var start = now_page <= 3 ? 1 : now_page - 2;
    var end = now_page <= 3 ? 5 : now_page + 2;

    for (var i = start; i <= end && i<=max_page; i++) {
        html += '<span class="' + (i === now_page ? 'active': '') + '" data-page="' + i + '">' + i + '</span>';
    }

    if (now_page < max_page - 1) {
        html += '<span class="' + (i === now_page ? 'active': '') + '" data-page="' + (now_page + 1) + '">></span>';
    }
    html += '</div>';
    return html;
}

function bind_page(){
    $('.pages span').unbind().click(function(){
        get_data(parseInt($(this).attr('data-page')));
    });
}

get_data(now_page);