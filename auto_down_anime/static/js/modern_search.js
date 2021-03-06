function gen_page(count) {
    var html = '';
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
    return html;
}


function bind_page(){
    $('.pages span').unbind().click(function(){
        get_data(parseInt($(this).attr('data-page')));
    });
}

var loading =false;

function get_data(page) {
    if(loading) return;
    loading =true;
    history.pushState({}, document.title, '/search/{key}'.format({key: search_key}));
    var next = page > now_page;
    now_page = page;
    $.get('/api/v1/search/video?key={key}&page={page}'.format({key: search_key, page: page}), function (data) {
        var html = '';
        for (var i in data.res) {
            var _ = data.res[i];
            html += '<div class="modern w2 h1" data-name="{title}" data-href="/video/av{av}"><div class="sub full"><img src="{img}"/></div></div>'.format({
                av: _['id'],
                img: _['img'],
                title: _['title'],
            })
        }
        $('result').html(html);
        $('.pages').html(gen_page(data['count']));
        load_modern_href();
        load_modern_name();
        bind_page();
        loading = false;
    }).error(function(){loading=false;});
}

var now_page = 1;
get_data(now_page);

$('#search').unbind().keydown(function(event){
        if (event.keyCode == 13){
            if(!$('#search').val().trim()) return;
            search_key = $('#search').val();
            $('.title').text(search_key + '的搜索结果');
            get_data(1);
        }
    });