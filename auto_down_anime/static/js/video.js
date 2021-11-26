$(document).ready(function () {
    all.replace_fence();

    $("img.lazy").lazyload({effect: "fadeIn"});
    var $window = $(window);
    var starting = {
        'nav': false,
    };

    $('a[href*=#]').click(function () {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var $target = $(this.hash);
            $target = $target.length && $target || $('[name=' + this.hash.slice(1) + ']');
            if ($target.length) {
                starting['nav'] = true;
                var targetOffset = $target.offset().top - 60;
                $('html,body').animate({
                        scrollTop: targetOffset
                    },
                    300);
                setTimeout(function () {
                    starting['nav'] = false;
                }, 280);
                return false;
            }
        }
    });

    $('#nav-right li a').click(function () {
        if ($(this).attr('data-notselect') == 'true') return;
        $('#nav-right li').removeClass('current');
        $(this).parent('li').addClass('current');
    });

    $window.on('scroll', function () {
        if (starting['nav']) return;
        var $navs = $('#nav-right a'),          // 导航
            $sections = $('.section-padding'),       // 模块
            navLength = $navs.length - 2;

        var scrollTop = $window.scrollTop(),
            len = navLength;
        if (scrollTop <= $sections.eq(0).offset().top - 150) {
            $('#nav-right li').removeClass('current');
            $navs.eq(0).parent('li').addClass('current');
            return;
        }
        for (; len >= 0; len--) {
            var that = $sections.eq(len);
            if (scrollTop >= that.offset().top - 150) {
                $('#nav-right li').removeClass('current');
                $navs.eq(len + 1).parent('li').addClass('current');
                break;
            }
        }
    });

    $('.navbar-default').css({"zIndex": "99"});
});

var fun = {
    'show_player': function () {
        $('.video').html('<div class="d12 m6 s3"><iframe style="width:100%" src="http://player.bilibili.com/player.html?aid={aid}&cid={cid}&page=1&autoplay=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe></div>'.format({
            'cid': window._INIT['cid'],
            'aid': window._INIT['id']
        }));
    },
    'set_html': function (name, data) {
        $(name).html(data);
    },
    'set_text': function (name, data) {
        $(name).text(data);
    },
};

var _id = 0;
var _type = '';

function init() {
    _ = all.go(document.location.href, false);
    _id = _[0];
    _type = _[1];
    bind();
    adaptive();
}

function bind() {
    $('.js-load-player').unbind().click(function () {
        fun.show_player();
    });
    $('#url').unbind().keydown(function (event) {
        if (event.keyCode == 13) {
            all.go($('#url').val(),true)
        }
    });
    $("#download .dbox .left li").unbind().on("mouseenter click", function () {
        var $left_li = $("#download .dbox .left li");
        var $right = $("#download .dbox .right");
        $left_li.removeClass('active');
        $(this).addClass('active');
        var index = $($left_li).index(this);
        var _ = 0;
        switch (index) {
            case 0:
            case 1:
                _ = $right.width() * index;
                break;
            default:
                var width = $right.find('li:eq(1)').width();
                _ = width * (index - 1);
                _ += $right.width();
                break;
        }
        $right.find('ul').css('margin-left', -_);
    });

    $(".dbox li:eq(1)").click();

    $('.open_bilibili').unbind().click(function () {
        window.open(window.location.href.replace(window.location.host, 'www.bilibili.com'))
    });

    $('body').unbind().keydown(function (event) {
        if (event.shiftKey || event.ctrlKey || event.altKey)return;
        if ([9, 16, 17, 18, 20, 27, 32, 33, 34, 35, 36, 37, 38, 39, 40, 45, 46, 144, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123].indexOf(event.keyCode) > -1)return;
        $('#url').focus();
    });

    $('.refresh-info .click').unbind().click(function () {
        if ($('.refresh-info .click').text() == '刷新中...') {
            alert('sh');
            return;
        }
        load(true);
    });
}

function adaptive() {
    var $d_right = $('#download .dbox .right ul');
    $d_right.css('display', 'block').find('li:eq(0)').css({'width': $('#download .dbox .right').width()});
    $('#download .dbox .left .active').click();
}

function showUpVideoList() {
    try {
        if (window._INIT['up']['list'].length == 1) {
            $('.up-list ul').html('<li class="no-data">暂时没有在唧唧找到这个UP主的其他视频_(:з」∠)_..</li>');
            return;
        }
        $('.up-list ul').html('');
        for (var i in window._INIT['up']['list']) {
            var _ = window._INIT['up']['list'][i];
            if (_['id'] == window._INIT['id']) continue;
            $('.up-list ul').append('<li><a href="{url}" target="_blank"><img class="lazy" data-original="{img}"/><span>{title}</span></a></li>'.format({
                'url': '/video/av' + _['id'],
                'img': _['img'],
                'title': _['title']
            }));
        }
        $("img.lazy").lazyload({effect: "fadeIn"});
    }
    catch (e) {
        console.log('showUpVideoList>> ' + e)
    }
}

function getStatus(type, code, length) {
    switch (code) {
        case 1:
            return '{0} <br/>{1}MB'.format(type, (length / 1024 / 1024).toFixed(2));
        case 0:
            return '{0} <br/>{1}'.format(type, '等待缓存');
        case 11:
            return '{0} <br/>{1}'.format(type, '(1/6)解析数据');
        case 22:
            return '{0} <br/>{1}'.format(type, '(2/6)下载单段');
        case 33:
            return '{0} <br/>{1}'.format(type, '(2/6)下载多段');
        case 44:
            return '{0} <br/>{1}'.format(type, '(3/6)合并分段');
        case 55:
            return '{0} <br/>{1}'.format(type, '(4/6)转换文件');
        case 66:
            return '{0} <br/>{1}'.format(type, '(5/6)提取MP3');
        case 77:
            return '{0} <br/>{1}'.format(type, '(6/6)上传文件');
        case -1:
            return '{0} <br/>{1}'.format(type, '没达到缓存要求');
        case -2:
            return '{0} <br/>{1}'.format(type, '无法解析');
        case -3:
            return '{0} <br/>{1}'.format(type, '文件超出2048MB');
        case -4:
            return '{0} <br/>{1}'.format(type, '下载出错');
        case -5:
            return '{0} <br/>{1}'.format(type, '转换错误');
        case -6:
            return '{0} <br/>{1}'.format(type, '上传出错');
        case -7:
            return '{0} <br/>{1}'.format(type, '获取下载出错');
    }
    return type
}

var showDownloadListIng = false;
function showDownloadList() {
    try {
        if (showDownloadListIng)return;
        showDownloadListIng = true;
        var data = '';
        var down_info_url = '/api/v1/{type}/get_download_info?id={id}'.format({type: _type, id: _id});
        $.ajax({
            url: down_info_url,
            success: function (down_info) {
                down_info = down_info['res'];
                var auto_refresh = false;
                if ($('.dbox .left ul li').length == 0) {
                    for (var i in down_info) {
                        if (down_info[i]['audio_status'] > 1 || down_info[i]['video_status'] > 1) auto_refresh = true;
                        var _ = ('<li id="{id}" data-vtime="{vtime}" data-atime="{atime}"><div class="d-info"><a href="{mp4_path}" target="_blank" rel="nofollow" class="a">{mp4_data}</a><a href="{mp3_path}" target="_blank" class="a">{mp3_data}</a><a href="javascript:downXml({cid}, \'{pname}\');" rel="nofollow" class="a">XML弹幕</a></div><div class="p-name ellipsis">{p}.{pname}</div></li>').format({
                            id: down_info[i]['_id'],
                            vtime: down_info[i]['last_video_time'],
                            atime: down_info[i]['last_audio_time'],
                            p: (parseInt(i) + 1),
                            pname: down_info[i].part,
                            cid: down_info[i].cid,
                            mp4_path: down_info[i]['video_status'] == 1 ? down_info[i]['video_url'] : 'javascript:downmsg(\'MP4\', ' + down_info[i]['video_status'] + ');',
                            mp3_path: down_info[i]['audio_status'] == 1 ? down_info[i]['audio_url'] : 'javascript:downmsg(\'MP3\', ' + down_info[i]['audio_status'] + ');',
                            mp4_data: getStatus('MP4', down_info[i]['video_status'], down_info[i]['video_length']),
                            mp3_data: getStatus('MP3', down_info[i]['audio_status'], down_info[i]['audio_length']),
                        });
                        data += _;
                    }
                    $('ul.download_data').append(data);
                } else {
                    for (var i in down_info) {
                        if (down_info[i]['audio_status'] > 1 || down_info[i]['video_status'] > 1) auto_refresh = true;
                        var id = down_info[i]['_id'];
                        var vtime = down_info[i]['last_video_time'];
                        var atime = down_info[i]['last_audio_time'];
                        var _ = $('#' + id);
                        if (_.length && (_.attr('data-atime') != atime || _.attr('data-vtime') != vtime)) {
                            _.attr('data-atime', down_info[i]['last_audio_time']);
                            _.attr('data-vtime', down_info[i]['last_video_time']);
                            _.html(('<div class="d-info"><a href="{mp4_path}" target="_blank" rel="nofollow" class="a">{mp4_data}</a><a href="{mp3_path}" target="_blank" class="a">{mp3_data}</a><a href="javascript:downXml({cid}, \'{pname}\');" rel="nofollow" class="a">XML弹幕</a></div><div class="p-name ellipsis">{p}.{pname}</div>').format({
                                p: (parseInt(i) + 1),
                                pname: down_info[i].part,
                                cid: down_info[i].cid,
                                mp4_path: down_info[i]['video_status'] == 1 ? down_info[i]['video_url'] : 'javascript:downmsg(\'MP4\', ' + down_info[i]['video_status'] + ');',
                                mp3_path: down_info[i]['audio_status'] == 1 ? down_info[i]['audio_url'] : 'javascript:downmsg(\'MP3\', ' + down_info[i]['audio_status'] + ');',
                                mp4_data: getStatus('MP4', down_info[i]['video_status'], down_info[i]['video_length']),
                                mp3_data: getStatus('MP3', down_info[i]['audio_status'], down_info[i]['audio_length']),
                            }))
                        }
                    }
                }
                if (auto_refresh) {
                    setTimeout((function () {
                        showDownloadList();
                    }), 3000);
                }
                else {
                    showDownloadListIng = false;
                }
                bind();
            }
        });
    }
    catch (e) {
        console.log('showDownloadList error' + e)
    }
}

eval(function(p,a,c,k,e,d){e=function(c){return(c<a?"":e(parseInt(c/a)))+((c=c%a)>35?String.fromCharCode(c+29):c.toString(36))};if(!''.replace(/^/,String)){while(c--)d[e(c)]=k[c]||e(c);k=[function(e){return d[e]}];e=function(){return'\\w+'};c=1;};while(c--)if(k[c])p=p.replace(new RegExp('\\b'+e(c)+'\\b','g'),k[c]);return p;}('p t(5,2){3 7=v h();3 d=q(h.7()/o);3 9=(7.u()+1);3 b=7.s();3 e=7.r()+\'-\'+(9<g?\'0\'+9:9)+\'-\'+(b<g?\'0\'+b:b);3 a=\'{5}{8}1{2}{c}m\'.k({5:5,8:e,2:2,c:d});3 6=l(a).n();f.j(\'a\',a);f.j(\'6\',6);2=I(2);2=2.4(\'\\\\\',\'@J@\');2=2.4(\'/\',\'@G@\');2=2.4(\'.\',\'@H@\');2=2.4(\'&\',\'@K@\');2=2.4(\':\',\'@N@\');2=2.4(\'?\',\'@M@\');2=2.4(\'%L\',\'@F@\');2=2.4(\'+\',\'@y@\');3 i=\'z://w.x.A/D/E/{5}/{8}/1/{2}/{6}/{c}\'.k({5:5,8:e,2:2,c:d,6:6});B.C(i)}',50,50,'||name|var|replace|cid|sign|now|strTime|month|sign_str|day|unixTime|nowUnixTime|nowStrTime|console|10|Date|url|log|format|md5|293CB1A8B301DA66F555DCE029E53D9C|toUpperCase|1000|function|parseInt|getFullYear|getDate|downXml|getMonth|new|newbarrage|bilibilijj|Blank|http|com|window|open|api|down|Jia|FSlash|Point|encodeURIComponent|ZSlash|And|2b|Quest|YH'.split('|'),0,{}));


function downmsg(type, code) {
    var msg = '';
    switch (code) {
        case 0:
            msg = '正在等待缓存, 缓存完毕过后即可直接下载, 这可能需要一段时间';
            break;
        case -1:
            msg = '该文件暂未达到缓存最低要求\n\n目前缓存最低要求为视频发布后7天内播放量超过1万\n\n\n【您可以通过唧唧windows客户端尝试下载该视频】';
            break;
        case -4:
            msg = '下载出错, 下载文件时出现错误, 唧唧将会稍后进行共计10次的重试操作';
            break;
    }
    if (msg) alert(msg);
}

function getBarrageUrl(cid, name) {
    var myDate = new Date();
    var nowTime = parseInt(Date.now() / 1000);
    var strTime = '{y}-{m}-{d}'.format({y: myDate.getFullYear(), m: myDate.getMonth()+1, d: myDate.getDay()});
    name = encodeURIComponent(name);
    name = name.replace('\\', '@ZSlash@"');
    name = name.replace('/', '@FSlash@"');
    name = name.replace('.', '@Point@"');
    name = name.replace('&', '@And@"');
    name = name.replace('?', '@Quest@"');
    name = name.replace('%2b', '@Jia@"');
    name = name.replace('+', '@Blank@"');
    var sign_str = '{cid}{strTime}1{name}{nowTime}'.format({cid: cid, strTime: strTime, name: name, nowTime: nowTime});
    var sign = hex_md5(sign_str);
    var downurl = 'http://newbarrage.bilibilijj.com/api/down/{cid}/{strTime}/1/{name}/{sign}/{}'
    //              Cid, DateTime.Now.ToString("yyyy-MM-dd"), Sort.ToLower() == "ass" ? 0 : 1, Name, NowUnixTime), false);
    //             , Cid, DateTime.Now.ToString("yyyy-MM-dd"), Sort.ToLower() == "ass" ? 0 : 1, GoName, Sign, NowUnixTime);
    //             context.Response.Redirect(DownUrl);
}

function load(refresh) {
    var _ = window._INIT;
    if ((_['msg'] && _['msg'] == 'loading') || (refresh && Date.now() / 1000 - _['ltime'] > 600)) {
        if (refresh) {
            fun.set_html('.refresh-info .click', '刷新中...');
        }
        else {
            fun.set_html('h1', '正在加载中...');
        }
        $('.down-cover').hide();
        setTimeout((function () {
            console.log('load');
            var url = '/api/v1/{type}/get_info?id={id}&refresh={refresh}'.format({
                type: _type,
                id: _id,
                refresh: refresh
            });
            $.get(url, function(data){
                window._INIT = data;
                load(refresh);
            });
        }), 3000);
    }
    else {
        fun.set_html('.refresh-info .click', '刷新缓存');
        fun.set_html('h1', _['title']);
        var desc = _['desc'];
        var reg = new RegExp("(av\\d*)", "g");
        desc = desc.replace(reg, '<a href="/video/$1" target="_blank" title="av$1">$1</a>');
        fun.set_html('.info .desc', desc);
        fun.set_html('.info .play', _['play'] ? _['play'].toString().replace('-', '(约)') : '--');
        fun.set_html('.info .coin', _['coins'] ? _['coins'] : '--');
        fun.set_html('.info .fav', _['favos'] ? _['favos'] : '--');
        fun.set_html('.info .time', 'B站发布时间:&k;' + common.formatTime(_['btime']) + '&k;|&k;唧唧更新时间: &k;' + common.timeago(_['ltime']) + '&k;|&k;<span class="fold">展开/收起简介</span>');
        $('.time .fold').unbind().click(function () {
            $('.video-info').toggleClass('max-height');
        });
        fun.set_text('.sort', _['sort'] + '-' + _['subsort']);

        setTimeout(function(){$('img.cover').attr('src', _['img']);}, 1);
        $('.down-cover a').attr({ 'download': _['title'] + '.jpg', 'href': _['img'] });

        document.title = _['title'] + document.title;

        setTimeout(function(){$('.up-avatar img').attr('src', _['up']['avatar']);}, 1);
        $('.up-author').unbind().click(function(){
           window.open('/up/id/' + _['up']['id']);
        });
        fun.set_text('.up-author', _['up']['author']);
        fun.set_text('.up-sign', _['up']['sign']);

        var authorize = _['up']['authorize'];
        $('.up-avatar img').addClass(authorize == -1 ? 'refuse': authorize == 0 ? 'unknown': 'allow');


        if (parseInt(Date.now() / 1000) - _['ltime'] >= 600) {
            fun.set_html('.refresh-info', '下载数据在&k;<span class="time">' + common.timeago(_['ltime']) + '</span>&k;缓存,&k;如果显示的分P数量和B站不一致,&k;请点击<span class="click">刷新缓存</span>,&k;更新缓存再试试');
        }
        else {
            fun.set_html('.refresh-info', '');
        }

        $('.down-cover').show();

        showUpVideoList();
        showDownloadList();
    }
}
setTimeout(function(){init();load();}, 1);

$('.preloader').fadeOut();
$('.preloader-area').delay(350).fadeOut('slow');

window.onload = function () {
    setTimeout(function () {
        adaptive();
    }, 500);
};
window.onresize = function () {
    adaptive();
};
