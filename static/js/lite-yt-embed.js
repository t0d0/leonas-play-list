/**
 * A lightweight youtube embed. Still should feel the same to the user, just MUCH faster to initialize and paint.
 *
 * Thx to these as the inspiration
 * https://storage.googleapis.com/amp-vs-non-amp/youtube-lazy.html
 * https://autoplay-youtube-player.glitch.me/
 *
 * Once built it, I also found these:
 * https://github.com/ampproject/amphtml/blob/master/extensions/amp-youtube (👍👍)
 * https://github.com/Daugilas/lazyYT
 * https://github.com/vb/lazyframe
 */
class LiteYTEmbed extends HTMLElement {
    static ActiveLiteYoutube = undefined;
    static CurrentTitle = undefined;
    static onPlayFunction = undefined;
    static onPauseFunction = undefined;
    static hasNextAction = false;
    connectedCallback() {
        this.videoId = this.getAttribute('videoid');
        let playBtnEl = this.querySelector('.lty-playbtn');
        // A label for the button takes priority over a [playlabel] attribute on the custom-element
        this.playLabel = (playBtnEl && playBtnEl.textContent.trim()) || this.getAttribute('playlabel') || 'Play';
        /**
         * Lo, the youtube placeholder image! (aka the thumbnail, poster image, etc)
         *
         * See https://github.com/paulirish/lite-youtube-embed/blob/master/youtube-thumbnail-urls.md
         *
         * TODO: Do the sddefault->hqdefault fallback
         * - When doing this, apply referrerpolicy (https://github.com/ampproject/amphtml/pull/3940)
         * TODO: Consider using webp if supported, falling back to jpg
         */
        if (!this.style.backgroundImage) {
            this.style.backgroundImage = `url("https://i.ytimg.com/vi/${this.videoId}/hqdefault.jpg")`;
        }

        // Set up play button, and its visually hidden label
        if (!playBtnEl) {
            playBtnEl = document.createElement('button');
            playBtnEl.type = 'button';
            playBtnEl.classList.add('lty-playbtn');
            this.append(playBtnEl);
        }
        if (!playBtnEl.textContent) {
            const playBtnLabelEl = document.createElement('span');
            playBtnLabelEl.className = 'lyt-visually-hidden';
            playBtnLabelEl.textContent = this.playLabel;
            playBtnEl.append(playBtnLabelEl);
        }

        // On hover (or tap), warm up the TCP connections we're (likely) about to use.
        this.addEventListener('pointerover', LiteYTEmbed.warmConnections, {
            once: true
        });

        // Once the user clicks, add the real iframe and drop our play button
        // TODO: In the future we could be like amp-youtube and silently swap in the iframe during idle time
        // We'd want to only do this for in-viewport or near-viewport ones: https://github.com/ampproject/amphtml/pull/5003
        this.addEventListener('click', this.addIframe);
    }

    // // TODO: Support the the user changing the [videoid] attribute
    // attributeChangedCallback() {
    // }

    /**
     * Add a
     <link rel={preload | preconnect} ...> to the head
     */
    static addPrefetch(kind, url, as) {
        const linkEl = document.createElement('link');
        linkEl.rel = kind;
        linkEl.href = url;
        if (as) {
            linkEl.as = as;
        }
        document.head.append(linkEl);
    }

    /**
     * Begin pre-connecting to warm up the iframe load
     * Since the embed's network requests load within its iframe,
     * preload/prefetch'ing them outside the iframe will only cause double-downloads.
     * So, the best we can do is warm up a few connections to origins that are in the critical path.
     *
     * Maybe `
     <link rel=preload as=document>` would work, but it's unsupported: http://crbug.com/593267
     * But TBH, I don't think it'll happen soon with Site Isolation and split caches adding serious complexity.
     */
    static warmConnections() {
        if (LiteYTEmbed.preconnected) return;

        // The iframe document and most of its subresources come right off youtube.com
        LiteYTEmbed.addPrefetch('preconnect', 'https://www.youtube-nocookie.com');
        // The botguard script is fetched off from google.com
        LiteYTEmbed.addPrefetch('preconnect', 'https://www.google.com');

        // Not certain if these ad related domains are in the critical path. Could verify with domain-specific throttling.
        LiteYTEmbed.addPrefetch('preconnect', 'https://googleads.g.doubleclick.net');
        LiteYTEmbed.addPrefetch('preconnect', 'https://static.doubleclick.net');

        LiteYTEmbed.preconnected = true;
    }

    addIframe(e) {
        const params = Object.fromEntries((new URLSearchParams(this.getAttribute('params'))));
        if (this.classList.contains('lyt-activated')) return;
        this.classList.add('lyt-activated');
        this.removeAttribute("style");
        let tag = document.createElement('script');

        tag.src = "https://www.youtube.com/iframe_api";
        let firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

        // onPlayerStateChange.bind(this);
        const divEl = document.createElement('div');
        divEl.id = `player-${this.getAttribute("id")}`;
        this.append(divEl);
        this.player = new YT.Player(
            `player-${this.getAttribute("id")}`, {
                width: '640',
                height: '360',

                videoId: encodeURIComponent(this.videoId),

                playerVars: {
                    'autoplay': 1,
                    'controls': 0
                },

                events: {
                    /* イベント */
                    "onReady": onPlayerReady,
                    "onStateChange": (event) => {

                        if (event.data == YT.PlayerState.PLAYING) {
                            event.target.setVolume(getController('controller').querySelector('[name=volume]').value);
                            if (LiteYTEmbed.ActiveLiteYoutube &&
                                LiteYTEmbed.ActiveLiteYoutube.getAttribute('id') !== this.getAttribute('id')) {LiteYTEmbed.hasNextAction = true;
                                LiteYTEmbed.ActiveLiteYoutube.stop();
                            }
                            LiteYTEmbed.ActiveLiteYoutube = this;
                            if (LiteYTEmbed.onPlayFunction) {
                                setTimeout(LiteYTEmbed.onPlayFunction, 100);
                            }
                        }
                        if (event.data == YT.PlayerState.PAUSED) {
                            if (LiteYTEmbed.onPauseFunction) {
                                    LiteYTEmbed.onPauseFunction();
                            }
                        }
                    }
                }
            }
        );

        function onPlayerReady(event) {
            console.log("onPlayerReady")
            console.log(params.start);
            event.target.startSeconds = params.start;
            event.target.playVideo();
            event.target.setVolume(getController('controller').querySelector('[name=volume]').value);
        }

        return;
    }

    setVolume(volume) {
        this.player.setVolume(volume);
    }

    start() {
        console.log("start2")
        this.player.playVideo();
    }

    stop() {
        this.player.pauseVideo();
    }
}

function getController(controller) {
    return document.getElementById(controller);
}


// Register custom element
customElements.define('lite-youtube', LiteYTEmbed);
