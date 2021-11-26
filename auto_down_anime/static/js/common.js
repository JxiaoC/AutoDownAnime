var common = {
    get_html: function (url) {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                data[url] = xhr.responseText;
            }
        };
        xhr.open('get', url, false);
        xhr.send();
        return data[url];
    }

    , openUrl: function (url) {
        if (window.localStorage.open_current) {
            document.location.href = url;
        } else {
            window.open(url);
        }
    }

    , get_query_string: function (name) {
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return unescape(r[2]);
        return null;
    }

    , goto_top: function (acceleration, stime) {
        acceleration = acceleration || 0.1;
        stime = stime || 10;
        var x1 = 0;
        var y1 = 0;
        var x2 = 0;
        var y2 = 0;
        var x3 = 0;
        var y3 = 0;
        if (document.documentElement) {
            x1 = document.documentElement.scrollLeft || 0;
            y1 = document.documentElement.scrollTop || 0;
        }
        if (document.body) {
            x2 = document.body.scrollLeft || 0;
            y2 = document.body.scrollTop || 0;
        }
        var x3 = window.scrollX || 0;
        var y3 = window.scrollY || 0;
        var x = Math.max(x1, Math.max(x2, x3));
        var y = Math.max(y1, Math.max(y2, y3));
        var speeding = 1 + acceleration;
        window.scrollTo(Math.floor(x / speeding), Math.floor(y / speeding));
        if (x > 0 || y > 0) {
            var run = "gotoTop(" + acceleration + ", " + stime + ")";
            window.setTimeout(run, stime);
        }
    }

    , show_hitokoto: function (sleep, class_name, type) {
        sleep = sleep < 3000 ? 3000 : sleep;
        var fun = type == 'modern' ? common._show_hitkoto_modern : common._show_hitkoto;
        fun(sleep, class_name);
        clearInterval(window.home_hitokoto);
        window.home_hitokoto = setInterval(function () {
            fun(sleep, class_name);
        }, sleep);
    }
    , _show_hitkoto: function (sleep, class_name) {
        $.get('//hitokoto.jijidown.com/v1/api/hitokoto?maxlength=80', function (_) {
            _ = JSON.parse(_);
            $('.' + class_name).css('opacity', '0');
            setTimeout(function () {
                $('.' + class_name).html('{data}&nbsp;&nbsp;&nbsp;&nbsp;——{from}'.format({
                    'data': _['hitokoto'],
                    'from': _['source']
                }));
                $('.' + class_name).css('opacity', '1');
            }, 1000);
        });
    }
    , _show_hitkoto_modern: function (sleep, class_name) {
        $.get('//hitokoto.jijidown.com/v1/api/hitokoto?maxlength=80', function (_) {
            _ = JSON.parse(_);
            var t = $('.' + class_name);
            t.removeClass('hitokoto').css('transform', 'perspective(400px) rotateX(0deg) rotateY(0deg);');
            t.find('.start').html(t.find('.end').html());
            t.addClass('hitokoto');
            $('.' + class_name + ' .end').html('{data}&nbsp;&nbsp;&nbsp;&nbsp;——{from}'.format({
                'data': _['hitokoto'],
                'from': _['source']
            }));
            $('.' + class_name).css('transform', 'perspective(400px) rotatex(90deg);');
        });
    }
    , formatTime: function (time) {
        if (time == 0) return 'N/A';
        var unixTimestamp = new Date(time * 1000);
        var Y = unixTimestamp.getFullYear();
        var M = ((unixTimestamp.getMonth() + 1) >= 10 ? (unixTimestamp.getMonth() + 1) : '0' + (unixTimestamp.getMonth() + 1));
        var D = (unixTimestamp.getDate() >= 10 ? unixTimestamp.getDate() : '0' + unixTimestamp.getDate());
        var H = (unixTimestamp.getHours() >= 10 ? unixTimestamp.getHours() : '0' + unixTimestamp.getHours());
        var m = (unixTimestamp.getMinutes() >= 10 ? unixTimestamp.getMinutes() : '0' + unixTimestamp.getMinutes());
        return Y + '-' + M + '-' + D + ' ' + H + ':' + m;
    }
    , timeago: function (dateTimeStamp) {   //dateTimeStamp是一个时间毫秒，注意时间戳是秒的形式，在这个毫秒的基础上除以1000，就是十位数的时间戳。13位数的都是时间毫秒。
        dateTimeStamp = dateTimeStamp * 1000;
        var minute = 1000 * 60;      //把分，时，天，周，半个月，一个月用毫秒表示
        var hour = minute * 60;
        var day = hour * 24;
        var week = day * 7;
        var halfamonth = day * 15;
        var month = day * 30;
        var now = new Date().getTime();   //获取当前时间毫秒
        var diffValue = now - dateTimeStamp; //时间差

        if (diffValue < 0) {
            return '刚刚';
        }
        var minC = diffValue / minute;  //计算时间差的分，时，天，周，月
        var hourC = diffValue / hour;
        var dayC = diffValue / day;
        var weekC = diffValue / week;
        var monthC = diffValue / month;
        var result = "";
        if (monthC >= 1 && monthC <= 3) {
            result = " " + parseInt(monthC) + "月前"
        } else if (weekC >= 1 && weekC <= 3) {
            result = " " + parseInt(weekC) + "周前"
        } else if (dayC >= 1 && dayC <= 6) {
            result = " " + parseInt(dayC) + "天前"
        } else if (hourC >= 1 && hourC <= 23) {
            result = " " + parseInt(hourC) + "小时前"
        } else if (minC >= 1 && minC <= 59) {
            result = " " + parseInt(minC) + "分钟前"
        } else if (minC < 1) {
            result = '刚刚';
        } else {
            var datetime = new Date();
            datetime.setTime(dateTimeStamp);
            var Nyear = datetime.getFullYear();
            var Nmonth = datetime.getMonth() + 1 < 10 ? "0" + (datetime.getMonth() + 1) : datetime.getMonth() + 1;
            var Ndate = datetime.getDate() < 10 ? "0" + datetime.getDate() : datetime.getDate();
            var Nhour = datetime.getHours() < 10 ? "0" + datetime.getHours() : datetime.getHours();
            var Nminute = datetime.getMinutes() < 10 ? "0" + datetime.getMinutes() : datetime.getMinutes();
            var Nsecond = datetime.getSeconds() < 10 ? "0" + datetime.getSeconds() : datetime.getSeconds();
            result = Nyear + "-" + Nmonth + "-" + Ndate
        }
        return result;
    }
    , show_alert: function (data) {
        var html = '<div class="alert" style="position:fixed;top:0;left:0;width:100%;height:100%;background-color:rgba(0,0,0,0.5);text-align:center;">\n' +
            '            <div style="max-height: 300px;width: 700px;position: relative;top: 50%;left: 50%;margin: -150px 0 0 -370px;background-color: rgba(255,255,255,0.9);user-select: text;padding: 50px 20px 50px 20px;overflow-y: auto;">\n' +
            '                <div style="position: absolute;right: 0;top:0;width:50px;height:50px;background-color:red;cursor:pointer;color: white;line-height: 50px;" onclick="$(\'.alert\').remove();">X</div>\n' +
            '            {data}</div>\n'.format({data: data}) +
            '        </div>';
        $('body').append(html);
    }
    , load_dongcidaci: function () {
        $('.modern[data-dongcidaci]').each(function (i, self) {
            var code = $(self).attr('data-dongcidaci');
            $(self).find('.sub').addClass('full').append('<img src="{img}" style="width:100%;height:100%;"/>'.format({img: dongcidaci[code][0]}));
            $(self).find('.sub img').unbind().click(function () {
                window.open(dongcidaci[code][1]);
            });
        })
    }
};