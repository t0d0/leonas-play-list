const existContentIdList = [];
let renderFlg = true;
let renderedContentValue = 0;
let loadedEmbededYTValue = 0;
isLogin = document.getElementById('login-flg').value === 'True';
let ActiveLiteYoutube = undefined;
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
//お試し中---------------------------------------------------------
//       var tag = document.createElement('script');
//
//       tag.src = "https://www.youtube.com/iframe_api";
//       var firstScriptTag = document.getElementsByTagName('script')[0];
//       firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
//
//       // 3. This function creates an <iframe> (and YouTube player)
//       //    after the API code downloads.
//       var player;
//       function onYouTubeIframeAPIReady() {
//           console.log("funger");
//
//       }
//---------------------------------------------------------



function changeDeleteTarget(id) {
    document.getElementById('delete-target').value = id;

}

function changeEditTarget(id, url, title, artist, time) {
    document.getElementById('edit-target').value = id;
    document.getElementById('edit-url').value = url;
    document.getElementById('edit-artist').value = artist;
    document.getElementById('edit-title').value = title;
    const hour = Math.floor(time / 3600);
    time -= hour * 3600;
    const minute = Math.floor(time / 60);
    time -= minute * 60;
    const sec = time;
    document.getElementById('edit-time').value = `${hour}:${minute}:${sec}`;
}

function getCookie(name) {
    const r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function postNewContent() {
    const newContentform = document.getElementById('new-content-form');

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
    const deleteContentform = document.getElementById('delete-content-form');
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
    const editform = document.getElementById('edit-form');
    const data = {
                'target': editform.target.value,
                'title': editform.title.value,
                'artist': editform.artist.value,
                'url': editform.url.value,
                'time': editform.time.value,
                '_xsrf': getCookie("_xsrf")
    };
    ajax('api/content', 'PUT', data).then(data => {
        const target_card = document.getElementById(editform.target.value);
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
    const regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function setTemplateValue(template, data) {
    const dom = template;
    dom.querySelector('#title').textContent = data['title'];
    dom.querySelector('#artist').textContent = data['artist'] == "" ? "不明なアーティスト" : data['artist'];
    dom.querySelector('#published-at').textContent = data['published_at'] == "null" ? "未登録" : formatDate(new Date(data['published_at']));
    dom.querySelector('#artist-btn').setAttribute('href', `/?artist=${encodeURIComponent(data['artist'] == ""?"unknown":data['artist'])}`);

    dom.querySelector('.lite-youtube').setAttribute("videoid", data['video_id']);
    dom.querySelector('.lite-youtube').setAttribute("id", `lt-${data['_id']}`);

    // dom.querySelector('#youtube').setAttribute("onclick", "onClickVideo(this)");
    dom.querySelector('.lite-youtube').setAttribute("params", `controls=0&start=${data['time']}&modestbranding=2&rel=0&enablejsapi=1`);
    // dom.querySelector('.lite-youtube').setAttribute("controller", 'controller');
    dom.querySelector('#youtubeapp-btn').setAttribute("href", `https://www.youtube.com/watch?v=${data['video_id']}&t=${data['time']}&rel=0&playsinline=1&`)
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
document.addEventListener('click', function (e) {
    console.log("何かをクリック");
    console.log(e.target.tagName.toLowerCase());
    if((e.target.tagName.toLowerCase() === 'lite-youtube')
        ||(e.target.classList.contains('lty-playbtn'))) {
        if (ActiveLiteYoutube) {
            ActiveLiteYoutube.stop();
        }
        if (e.target.tagName.toLowerCase() === 'lite-youtube') {
            ActiveLiteYoutube = e.target.parentElement.querySelector('lite-youtube');
        } else if (e.target.classList.contains('lty-playbtn')) {
            ActiveLiteYoutube = e.target.parentElement;
        }
        document.getElementById('current-playing-title').innerText=ActiveLiteYoutube.parentElement.parentElement.querySelector('#title').innerText;
    }
});
function renderContent(data) {
    for (i of data) {
        if (i != undefined && (i['title'] != undefined)) {
            renderedContentValue += 1;
            const template = document.getElementById('content-template');
            let clone = template.content.cloneNode(true);
            const div = clone.querySelector('#content-root');
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
    const localStrageFavorites = [];
    for (let i = 0; i < localStorage.length; ++i) {
        const key = localStorage.key(i);
        const value = localStorage[key];
        if (key.indexOf('favorite') != -1) {
            localStrageFavorites.push(value);
        }
    }
    return localStrageFavorites;

}

window.onscroll = function (ev) {

    let elScrollable;
    if (navigator.userAgent.indexOf('WebKit') < 0) {
        elScrollable = document.documentElement;
    } else {
        elScrollable = document.body;
    }

    const scrollTop = elScrollable.scrollTop;
    const windowHeight = window.innerHeight;
    const pageHeight = elScrollable.scrollHeight;
    const marginBottom = 10;
    if (windowHeight + scrollTop + marginBottom >= pageHeight) {
        getNextContent();
    }

};


function settingSliderParams() {
    const elems = document.querySelectorAll('.slider');
    let height_coefficient = 1;
    if ((screen.width > screen.height) || screen.width >= 1280) {
        //横長
        height_coefficient = 9;
    } else {
        //縦長
        height_coefficient = 5;
    }
    const options = {
        indicators: false,
        height: screen.width / height_coefficient,
        duration: 1000,
        interval: 5000
    };
    const instances = M.Slider.init(elems, options);
}

function expandSearch() {
    document.getElementById("search").style.display = "block";
    document.getElementById("search").focus();
}

function hideSearch() {
    document.getElementById("search").style.display = "none";
}
//スライダーの処理
document.addEventListener('DOMContentLoaded', settingSliderParams);
window.addEventListener('resize', settingSliderParams);



document.addEventListener('DOMContentLoaded', function () {
    const options = {
        data : {}
    };
    const elems = document.querySelectorAll('#copyright-modal');
    const instances = M.Modal.init(elems, options);
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

  document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.dropdown-trigger');
    var instances = M.Dropdown.init(elems, {hover:false});
  });

function formatDate(dt) {
  var y = dt.getFullYear();
  var m = dt.getMonth()+1;
  var d = dt.getDate();
  return (y + '年' + m + '月' + d + '日');
}




//検索窓の入力時イベント
document.getElementById("search").addEventListener('input', onChangeSearch);

document.addEventListener('DOMContentLoaded', function() {
    let options = {data: {"autocomplete":null,},
    onAutocomplete:(a)=>console.log(a+"hoge")};
    const elems = document.querySelectorAll('#search');
    const instances = M.Autocomplete.init(elems, options);

});



function onChangeSearch(event){
    console.log(event.target.value);
    let data = {
        search: event.target.value,
        '_xsrf': getCookie("_xsrf")
    }
    ajax('api/search-suggestion', 'QUERY', data).then(data => {
        // document.getElementById(deleteContentform.target.value).remove();
        // UIkit.modal(document.getElementById("delete-confirm-modal")).hide();
        console.log(data);

        let hoge = data.reduce(function(target, key, index) {
          target[key] = null;
          return target;
        }, {})
        const elem = document.getElementById('search');
        const instance = M.Autocomplete.getInstance(elem);

        // console.log(hoge);
        instance.updateData(hoge);
    });

}

function onChangeVolumeSlider(event){
    // console.log(event)
    ActiveLiteYoutube.setVolume(event)
}
getNextContent();

