var Main = (function () {
    function Main() {
        var q = window.location.search;
        var pos = q.indexOf('code=');
        if (pos < 0) {
            alert('login failed');
            location.href = './';
            return;
        }
        pos += 5;
        var pos2 = q.indexOf('&', pos);
        if (pos2 < 0)
            pos2 = q.length;
        var code = q.substring(pos, pos2);
        var xhr = new XMLHttpRequest();
        xhr.addEventListener("load", function () {
            var resp = xhr.response;
            localStorage.setItem('session', resp['session']);
            location.href = './';
        });
        xhr.responseType = "json";
        xhr.open("GET", "api/oauth_callback?code=" + code);
        xhr.send();
    }
    return Main;
})();
new Main();
