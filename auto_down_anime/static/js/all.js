DEBUG = window.location.port == '1234';
var data = {};
String.prototype.format = function (args) {
    if (arguments.length > 0) {
        var result = this;
        if (arguments.length == 1 && typeof (args) == "object") {
            for (var key in args) {
                var reg = new RegExp("({" + key + "})", "g");
                result = result.replace(reg, args[key]);
            }
        } else {
            for (var i = 0; i < arguments.length; i++) {
                if (arguments[i] == undefined) {
                    return "";
                } else {
                    var reg = new RegExp("({[" + i + "]})", "g");
                    result = result.replace(reg, arguments[i]);
                }
            }
        }
        return result;
    } else {
        return this;
    }
};
var config = {
    'cdn_host': ['/'],
};

if (DEBUG) {
    config = {'cdn_host': ['/']};
}

var all = {
    'replace_class': function (name, rename) {
        $('.' + name).each(function () {
            $(this).removeClass(name).addClass(rename);
        });
    },
    'set_html': function (name, data) {
        $(name).html(data);
    },
    'set_text': function (name, data) {
        $(name).text(data);
    },
    'replace_fence': function () {
        all.replace_class('d2', 'col-md-2');
        all.replace_class('d3', 'col-md-3');
        all.replace_class('d6', 'col-md-6');
        all.replace_class('d9', 'col-md-9');
        all.replace_class('d10', 'col-md-10');
        all.replace_class('d12', 'col-md-12');

        all.replace_class('m3', 'col-sm-3');
        all.replace_class('m6', 'col-sm-6');
        all.replace_class('m9', 'col-sm-9');
        all.replace_class('m12', 'col-sm-12');

        all.replace_class('s3', 'col-xs-3');
        all.replace_class('s6', 'col-xs-6');
        all.replace_class('s9', 'col-xs-9');
        all.replace_class('s12', 'col-xs-12');
    },
    'load_resources': function (name, filePath, ver, type, genTag) {
        if (DEBUG) ver = Math.random();
        // genTag = !genTag;
        if (genTag) {
            var url = config.cdn_host[0] + filePath + '?v=' + ver;
            if (type == 'css') {
                document.write('<link type="text/css" rel="stylesheet" href="{0}"/>'.format(url));
            }
            else {
                document.write('<script src="{0}"><\/script>'.format(url));
            }
            return;
        }
        var key = name + '_' + type;
        var localVer = window.localStorage.getItem(key + '_ver');
        if (localVer != ver) {
            var urls = [];
            for (var i in config.cdn_host) urls.push(config.cdn_host[i] + filePath + '?v=' + ver);
            var resources = all.get_resources(urls);
            if (resources) {
                window.localStorage.setItem(key + '_ver', ver);
                window.localStorage.setItem(key, resources);
            }
        }
        var data = window.localStorage.getItem(key);
        document.writeln(type === 'css' ? '<style>' + data + '<\/style>' : '<script>' + data + '<\/script>');
    },
    'get_resources': function (urls, index) {
        index = index ? index : 0;
        var url = urls[index];
        try {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    data[url] = xhr.responseText;
                }
            };
            xhr.open('get', url, false);
            xhr.send();
            if ((!data[url] || data[url].indexOf('end_sub') === -1) && index < urls.length - 1) {
                console.log('load url failure>> ' + url);
                return all.get_resources(urls, index + 1);
            } else {
                setTimeout(function () {
                    delete data[url];
                }, 100);
                return data[url];
            }
        }
        catch (e) {
            console.log('load url error>> ' + url);
            if ((!data[url] || data[url].indexOf('end_sub') === -1) && index < urls.length - 1) {
                return all.get_resources(urls, index + 1);
            } else {
                setTimeout(function () {
                    delete data[url];
                }, 100);
                return data[url];
            }
        }
    },
    'go': function (url, href) {
        url = url.toLowerCase();
        var reg = null;
        var ret = [0, ''];
        if (parseInt(url)) {
            ret = [parseInt(url), 'video'];
            if (DEBUG) console.log('all.go 1');
            url = '/video/av' + url;
        } else if (url.toLowerCase().indexOf('video/av') > -1) {
            reg = new RegExp(/video\/av(\d*)/);
            reg.test(url);
            ret = [parseInt(RegExp.$1), 'video'];
            if (DEBUG) console.log('all.go 2');
            url = '/video/av' + RegExp.$1;
        } else if (url.toLowerCase().indexOf('/md') > -1) {
            reg = new RegExp(/md(\d*)/);
            reg.test(url);
            ret = [parseInt(RegExp.$1), 'anime'];
            if (DEBUG) console.log('all.go 3');
            url = '/bangumi/media/md' + RegExp.$1;
        } else if (url.toLowerCase().indexOf('/anime') > -1) {
            reg = new RegExp(/\/anime\/(\d*)/);
            reg.test(url);
            ret = [parseInt(RegExp.$1), 'anime'];
            if (DEBUG) console.log('all.go 3.1');
            url = '/bangumi/media/md' + RegExp.$1;
        } else if (url.toLowerCase().indexOf('av') > -1) {
            reg = new RegExp(/av(\d*)/);
            reg.test(url);
            ret = [parseInt(RegExp.$1), 'video'];
            url = '/video/av' + RegExp.$1;
            if (DEBUG) console.log('all.go 4');
        } else {
            url = "/search/" + encodeURIComponent(url).replace(/%/g, "|");
            ret = [url, 'search'];
        }
        if (href) window.open(url);
        return ret;
    },
};

if (!window.localStorage.JJ_Token) {
    var d = new Date();
    var nowtime = d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate();

    if (window.location.href.indexOf('mobile') == -1 && !window.localStorage.RightAndBotton_Time || window.localStorage.RightAndBotton_Time != nowtime) {
        //???
        document.write('<div style="position: fixed;right: 0;bottom: -1px;z-index:5;"><div style="cursor: pointer;" onclick="$(this).parent().remove();">??????<\/div><a href="http://t.cn/RQ2GA29" target="_black"><img src="http://zcdn.jijidown.com/static/img/right_bottom.gif"><\/a><\/div>');
        setTimeout(function () {
            window.localStorage.RightAndBotton_Time = nowtime;
        }, 5000);
    }
}

function yimada(){
        if ($('#go').val()) {
            $('.down_msg').html('?????????! ??????<span style="font-weight: 700;color:#ffb000;">??????</span>!');
        } else {
            $('.down_msg').html('??????B??????????????????????????????????????????');
        }
}