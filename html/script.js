var Main = (function () {
    function Main() {
        this.session = localStorage.getItem('session');
        if (!this.session) {
            this.login();
            return;
        }
        this.setup_dashboard();
    }
    Main.prototype.setup_dashboard = function () {
        var _this = this;
        var container = document.getElementById("races");
        var xhr = new XMLHttpRequest();
        xhr.addEventListener("load", function () {
            var resp = xhr.response;
            if (!resp) {
                if (xhr.status === 401)
                    _this.login();
                else if (xhr.status === 500)
                    alert('Internal Server Error');
                return;
            }
            var self_id = resp['user_id'];
            var races = resp['races'];
            var users = resp['users'];
            document.getElementById('profile_avatar').setAttribute('src', resp['avatar']);
            document.getElementById('profile_name').textContent = resp['name'] + ' (id: ' + self_id + ')';
            document.getElementById('profile_race').textContent = resp['n_races']['running'] + ' レース参加中';
            var q = document.querySelectorAll('.loggedin');
            q.forEach(function (e) { e.classList.remove('loggedin'); });
            races.forEach(function (race) {
                var e_race = document.createElement('div');
                e_race.setAttribute('class', 'race');
                container.appendChild(e_race);
                var e_race_title = document.createElement('div');
                e_race_title.appendChild(document.createTextNode(race['name']));
                e_race_title.setAttribute('class', 'title');
                e_race.appendChild(e_race_title);
                var e_race_graph = document.createElement('div');
                e_race_graph.setAttribute('class', 'graph');
                e_race.appendChild(e_race_graph);
                var max_steps = (race['members'] && race['members'][0] ? race['members'][0]['steps'] : 1);
                race['members'].forEach(function (m) {
                    var u = users[m['user_id']];
                    var e_u = document.createElement('div');
                    e_u.setAttribute('class', 'item');
                    e_race_graph.appendChild(e_u);
                    var e_u_avatar = document.createElement('img');
                    e_u_avatar.setAttribute('class', 'avatar');
                    e_u_avatar.setAttribute('src', u['avatar']);
                    e_u.appendChild(e_u_avatar);
                    var e_u_bar = document.createElement('div');
                    e_u_bar.setAttribute('class', 'bar');
                    e_u.appendChild(e_u_bar);
                    var e_u_bar2 = document.createElement('div');
                    e_u_bar2.style.width = Math.ceil(m['steps'] * 100 / max_steps) + '%';
                    if (self_id === m['user_id']) {
                        e_u_bar2.setAttribute('class', 'self');
                    }
                    e_u_bar2.appendChild(document.createTextNode(u['name']));
                    e_u_bar.appendChild(e_u_bar2);
                    var e_u_steps = document.createElement('div');
                    e_u_steps.setAttribute('class', 'steps');
                    e_u_steps.appendChild(document.createTextNode(m['steps']));
                    e_u.appendChild(e_u_steps);
                });
            });
        });
        xhr.responseType = "json";
        xhr.open("GET", "api/dashboard?session=" + this.session);
        xhr.send();
    };
    Main.prototype.login = function () {
        var xhr = new XMLHttpRequest();
        xhr.addEventListener("load", function () {
            var resp = xhr.response;
            location.href = resp['url'];
        });
        xhr.responseType = "json";
        xhr.open("GET", "api/oauth_info");
        xhr.send();
    };
    return Main;
})();
window.addEventListener("DOMContentLoaded", function () { return new Main(); });
