animeMusic.onProgress = function (per, now, all) {
    document.querySelector('.player .progress .now').style.width = per + '%';
    document.querySelector('.player .time').innerText = now + '/' + all;
};

animeMusic.onLoaded = function (res) {
    console.log(res);

    history.pushState(null, document.title, '?id=' + res.id);
    document.querySelector('.player .name').innerText = res.title + ' - ' + res.anime_info.title;

    var bg = document.createElement("img");
    bg.src = res.anime_info.bg;
    bg.onload = function () {
        if (document.querySelectorAll('.bg img').length > 1) {
            document.querySelectorAll('.bg img')[0].className = "";
            setTimeout(function () {
                document.querySelectorAll('.bg img')[0].remove();
            }, 1100);
        }
        this.className = "show";
    };
    document.querySelector('.bg').append(bg);

    var logo = document.createElement("img");
    logo.src = res.anime_info.logo;
    logo.onload = function () {
        if (document.querySelectorAll('.player .logo img').length > 1) {
            document.querySelectorAll('.player .logo img')[0].className = "";
            setTimeout(function () {
                document.querySelectorAll('.player .logo img')[0].remove();
            }, 1100);
        }
        this.className = "show";
    };
    document.querySelector('.player .logo').append(logo);
};

animeMusic.onPlay = function () {
    document.querySelector('.player .control').className = 'control iconfont icon-pause';
    document.querySelector('.player .control').onclick = function () {
        animeMusic.Pause();
    };
};

animeMusic.onLoad = animeMusic.onPlay;

animeMusic.onPause = function () {
    document.querySelector('.player .control').className = 'control iconfont icon-play';
    document.querySelector('.player .control').onclick = function () {
        animeMusic.Play();
    };
};

document.querySelector('.player .next').onclick = function () {
    animeMusic.Next();
};

animeMusic.bindPlayTo('.player .progress'); //绑定鼠标点击进度条时的处理事件

document.querySelector('.player .control').onclick = function () {
    animeMusic.Next();
};