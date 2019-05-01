var Main = (function () {
    function Main(race_id) {
        this.race_id = race_id;
        if (race_id) {
            alert('not implemented');
            location.href = './';
            return;
        }
        var tmp = localStorage.getItem('session');
        if (!tmp) {
            location.href = './';
            return;
        }
        this.session = tmp;
        this.user_id = this.session.substring(0, this.session.indexOf(':'));
        this.div_members = document.getElementById('members');
        this._init_button();
        this._fetch_friends();
    }
    Main.prototype._init_button = function () {
        var _this = this;
        var submit_btn = document.getElementById('submit');
        if (this.race_id) {
            submit_btn.textContent = '更新';
            submit_btn.addEventListener('click', function () { _this._update(); });
        }
        else {
            submit_btn.textContent = '作成';
            submit_btn.addEventListener('click', function () { _this._create(); });
        }
        document.getElementById('cancel').addEventListener('click', function () {
            location.href = './';
        });
    };
    Main.prototype._fetch_friends = function () {
        var _this = this;
        var xhr = new XMLHttpRequest();
        xhr.addEventListener("load", function () {
            var resp = xhr.response;
            resp.forEach(function (x) {
                if (x['type'] != 'person')
                    return;
                var attr = x['attributes'];
                _this._add_member_item(x['id'], attr['name'], attr['avatar']);
            });
        });
        xhr.responseType = "json";
        xhr.open("GET", "api/friends?session=" + this.session);
        xhr.send();
    };
    Main.prototype._add_member_item = function (user_id, name, avatar) {
        var row = document.createElement('div');
        var chk = document.createElement('input');
        chk.setAttribute('type', 'checkbox');
        chk.setAttribute('value', user_id);
        row.appendChild(chk);
        var img = document.createElement('img');
        if (avatar) {
            img.setAttribute('src', avatar);
        }
        row.appendChild(img);
        var uname = document.createElement('div');
        uname.textContent = name ? name : user_id;
        row.appendChild(uname);
        row.addEventListener('click', function (e) {
            chk.checked = !chk.checked;
        });
        chk.addEventListener('click', function (e) {
            e.stopPropagation();
        });
        this.div_members.appendChild(row);
    };
    Main.prototype._update = function () {
    };
    Main.prototype._create = function () {
        var req = {
            'name': document.getElementById('title').value,
            'start': document.getElementById('start').value,
            'end': document.getElementById('end').value,
            'members': [this.user_id]
        };
        var tmp = document.querySelectorAll('input[type="checkbox"]');
        tmp.forEach(function (x) {
            if (!x.checked)
                return;
            req['members'].push(x.value);
        });
        var xhr = new XMLHttpRequest();
        xhr.addEventListener("load", function () {
            var resp = xhr.response;
            if (xhr.status !== 200) {
                alert(resp);
            }
            else {
                location.href = './';
            }
        });
        xhr.open("POST", "api/race?session=" + this.session);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify(req));
    };
    return Main;
})();
{
    var q = window.location.search;
    var race_id = null;
    if (q && q[0] === '?') {
        q.substring(1).split('&').forEach(function (kv) {
            var items = kv.split('=', 2);
            if (items.length === 2 && items[0] === 'id')
                race_id = items[1];
        });
    }
    if (race_id) {
        document.title = 'レースを編集';
    }
    else {
        document.title = '新しくレースを作成';
    }
    window.addEventListener("DOMContentLoaded", function () { return new Main(race_id); });
}
