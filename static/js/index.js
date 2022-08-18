var existContentIdList = [];
var renderFlg = true;
var renderedContentValue = 0;
var loadedEmbededYTValue = 0;
isLogin = document.getElementById('login-flg').value == 'True';

async function ajax(url = '', method = '', data = {}) {

    const response = await fetch(url, {
        method: method,
        mode: 'same-origin',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'charset':'utf-8',
            'X-Xsrftoken':getCookie("_xsrf")
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
    })
    return response.json();
}


function changeDeleteTarget(id) {
    document.getElementById('delete-target').value = id;

}

function changeEditTarget(id, url, title, artist, time) {
    document.getElementById('edit-target').value = id;
    document.getElementById('edit-url').value = url;
    document.getElementById('edit-artist').value = artist;
    document.getElementById('edit-title').value = title;
    var hour = Math.floor(time / 3600);
    time -= hour * 3600;
    var minute = Math.floor(time / 60);
    time -= minute * 60;
    var sec = time;
    document.getElementById('edit-time').value = `${hour}:${minute}:${sec}`;
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function postNewContent() {
    var newContentform = document.getElementById('new-content-form');

    const data = {
        'title': newContentform.title.value,
        'url': newContentform.url.value,
        'time': newContentform.time.value,
        '_xsrf': getCookie("_xsrf")
    };
    ajax('api/content', 'POST', data).then(data => {
        UIkit.modal(document.getElementById("new-content-modal")).hide();
        for (item of data) {
            existContentIdList.push(item['_id']);
        }
        renderContent(data);

    });
}


function postDeleteContent() {
    var deleteContentform = document.getElementById('delete-content-form');
    const data = {
            'target': deleteContentform.target.value,
            '_xsrf': getCookie("_xsrf")
    };
    ajax('api/content', 'DELETE', data).then(data => {
            document.getElementById(deleteContentform.target.value).remove();
            renderedContentValue -= 1;
            loadedEmbededYTValue -= 1;
            UIkit.modal(document.getElementById("delete-confirm-modal")).hide();
    });

}

function postEditContent() {
    var editform = document.getElementById('edit-form');
    const data = {
                'target': editform.target.value,
                'title': editform.title.value,
                'artist': editform.artist.value,
                'url': editform.url.value,
                'time': editform.time.value,
                '_xsrf': getCookie("_xsrf")
    };
    ajax('api/content', 'PUT', data).then(data => {
            var target_card = document.getElementById(editform.target.value);
            var template = document.getElementById('content-template');
            setTemplateValue(target_card, data);
            UIkit.modal(document.getElementById("edit-modal")).hide();
    });
}




function sendFavorite(id) {
    const data = {
                'target': id,
                '_xsrf': getCookie("_xsrf"),
    };
    ajax('api/favorite', 'POST', data).then(data => {
            document.getElementById(id).querySelector('#favorite-btn').hidden = true;
            document.getElementById(id).querySelector('#unfavorite-btn').hidden = false;
    });
    return false;
}

function sendUnFavorite(id) {
    const data = {
                'target': id,
                '_xsrf': getCookie("_xsrf"),
    };
    ajax('api/favorite', 'DELETE', data).then(data => {
            document.getElementById(id).querySelector('#favorite-btn').hidden = false;
            document.getElementById(id).querySelector('#unfavorite-btn').hidden = true;
    });
    return false;
}

function getParam(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function setTemplateValue(template, data) {
    const dom = template;
    dom.querySelector('#title').textContent = data['title'];
    dom.querySelector('#artist').textContent = data['artist'] == "" ? "不明なアーティスト" : data['artist'];
    dom.querySelector('#artist-btn').setAttribute('href', `/?artist=${encodeURIComponent(data['artist'] == ""?"unknown":data['artist'])}`);

    dom.querySelector('#youtube').setAttribute("videoid", data['video_id']);
    dom.querySelector('#youtube').setAttribute("params", `controls=0&start=${data['time']}&modestbranding=2&rel=0&enablejsapi=1`);
    dom.querySelector('#youtubeapp-btn').setAttribute("href", `https://www.youtube.com/watch?v=${data['video_id']}&t=${data['time']}`)
    dom.querySelector('#search-btn').setAttribute("href", `/?search=${encodeURIComponent(data['title'])}&perfect=true`);
    if (isLogin) {
        dom.querySelector('#favorite-btn').hidden = data['isFavorite']
        dom.querySelector('#unfavorite-btn').hidden = !data['isFavorite']
        dom.querySelector('#favorite-btn').setAttribute('onclick', `sendFavorite('${data['_id']}')`);
        dom.querySelector('#unfavorite-btn').setAttribute('onclick', `sendUnFavorite('${data['_id']}')`);
    } else {
        dom.querySelector('#local-favorite-btn').setAttribute('onclick', `localFavorite('${data['_id']}')`);
        dom.querySelector('#local-unfavorite-btn').setAttribute('onclick', `localUnFavorite('${data['_id']}')`);
        if (localStorage.getItem(`favorites-${data['_id']}`)) {
            dom.querySelector('#local-favorite-btn').hidden = true;
            dom.querySelector('#local-unfavorite-btn').hidden = false;
        } else {
            dom.querySelector('#local-favorite-btn').hidden = false;
            dom.querySelector('#local-unfavorite-btn').hidden = true;
        }
    }

    dom.querySelector('#share').setAttribute('href', encodeURI(`http://twitter.com/share?url=https://youtu.be/${data['video_id']}?t=${data['time']}&text=レオナちゃんの「${data['title']}」おすすめだよ！&hashtags=獅子神レオナ`));
    dom.querySelector('#delete-btn').setAttribute('onclick', `changeDeleteTarget('${data['_id']}')`);
    dom.querySelector('#edit-btn').setAttribute('onclick',
        `changeEditTarget(
                    "${data['_id']}",
                    "https://www.youtube.com/watch?v=${data['video_id']}",
                    "${data['title']}",
                    "${data['artist']}",
                    "${data['time']}"
                    )`);
    return dom;
}

function renderContent(data) {
    if (data.length == 0) {
        //        document.getElementById('loading-text').innerHTML = "何も見つからないよ"
    }
    for (i of data) {
        if (i != undefined && (i['title'] != undefined)) {
            renderedContentValue += 1;
            var template = document.getElementById('content-template');
            var clone = template.content.cloneNode(true);
            var div = clone.querySelector('#content-root');
            div.id = `${i['_id']}`;
            clone = setTemplateValue(clone, i);
            document.getElementById('content-area').appendChild(clone);
        }
    }
}

async function getNextContent() {
    if (renderFlg) {
        renderFlg = false;
        const data = {
            '_xsrf': getCookie("_xsrf"),
            'exist': existContentIdList.join(','),
            'search': getParam('search', location.href),
            'perfect': getParam('perfect', location.href),
            'favorite': getParam('favorite', location.href),
            'artist': getParam('artist', location.href),
            'local-favorite': JSON.stringify(getAllLocalStrageFavorites())
        };
        ajax('api/content', 'QUERY', data).then(data => {
            for (const item of data) {
                existContentIdList.push(item['_id']);
            }
            renderContent(data);
            renderFlg = true;
        });
    }
}

function getAllLocalStrageFavorites() {
    var localStrageFavorites = [];
    for (var i = 0; i < localStorage.length; ++i) {
        var key = localStorage.key(i);
        var value = localStorage[key];
        if (key.indexOf('favorite') != -1) {
            localStrageFavorites.push(value);
        }
    }
    return localStrageFavorites;

}

window.onscroll = function (ev) {

    var elScrollable;
    if (navigator.userAgent.indexOf('WebKit') < 0) {
        elScrollable = document.documentElement;
    } else {
        elScrollable = document.body;
    }

    var scrollTop = elScrollable.scrollTop;
    var windowHeight = window.innerHeight;
    var pageHeight = elScrollable.scrollHeight;
    var marginBottom = 10;
    if (windowHeight + scrollTop + marginBottom >= pageHeight) {
        getNextContent();
    }

};




function isReadyNextLoading() {
    return loadedEmbededYTValue == renderedContentValue;
}

function settingsliderParams() {
    var elems = document.querySelectorAll('.slider');
    var height_coefficient = 1;
    if ((screen.width > screen.height) || screen.width >= 1280) {
        //横長
        height_coefficient = 9;
    } else {
        //縦長
        height_coefficient = 5;
    }
    var options = {
        indicators: false,
        height: screen.width / height_coefficient,
        duration: 1000,
        interval: 5000
    }
    var instances = M.Slider.init(elems, options);
}

function expandSearch() {
    document.getElementById("search").style.display = "block";
    document.getElementById("search").focus();
}

function hideSearch() {
    document.getElementById("search").style.display = "none";
}
//スライダーの処理
document.addEventListener('DOMContentLoaded', settingsliderParams);
window.addEventListener('resize', settingsliderParams);

document.addEventListener('DOMContentLoaded', function () {
    var options = {

    }
    var elems = document.querySelectorAll('#fav-modal');
    var instances = M.Modal.init(elems, options);

});

function localFavorite(target) {
    localStorage.setItem('favorites-' + target, target);
    document.getElementById(target).querySelector('#local-favorite-btn').hidden = true;
    document.getElementById(target).querySelector('#local-unfavorite-btn').hidden = false;
}

function localUnFavorite(target) {
    localStorage.removeItem('favorites-' + target);
    document.getElementById(target).querySelector('#local-favorite-btn').hidden = false;
    document.getElementById(target).querySelector('#local-unfavorite-btn').hidden = true;
}



getNextContent();
