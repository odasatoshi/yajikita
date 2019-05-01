class Main {
  race_id: string;
  session: string;
  user_id: string;
  div_members: HTMLDivElement;

  constructor(race_id?: string) {
    this.race_id = race_id;
    if (race_id) {
      alert('not implemented');
      location.href = './';
      return;
    }
    const tmp = localStorage.getItem('session');
    if (!tmp) {
      location.href = './';
      return;
    }
    this.session = tmp;
    this.user_id = this.session.substring(0, this.session.indexOf(':'));
    this.div_members = <HTMLDivElement>document.getElementById('members');

    this._init_button();
    this._fetch_friends();
  }

  _init_button() {
    const submit_btn = document.getElementById('submit');
    if (this.race_id) {
      submit_btn.textContent = '更新';
      submit_btn.addEventListener('click', () => { this._update(); });
    } else {
      submit_btn.textContent = '作成';
      submit_btn.addEventListener('click', () => { this._create(); });
    }
    document.getElementById('cancel').addEventListener('click', () => {
      location.href = './';
    });
  }

  _fetch_friends() {
    let xhr = new XMLHttpRequest();
    xhr.addEventListener("load", () => {
      const resp = xhr.response;
      resp.forEach((x) => {
        if (x['type'] != 'person') return;
        const attr = x['attributes'];
        this._add_member_item(x['id'], attr['name'], attr['avatar']);
      });
    });
    xhr.responseType = "json";
    xhr.open("GET", "api/friends?session=" + this.session);
    xhr.send();
  }

  _add_member_item(user_id: string, name?: string, avatar?: string) {
    const row = document.createElement('div');
    const chk = document.createElement('input');
    chk.setAttribute('type', 'checkbox');
    chk.setAttribute('value', user_id);
    row.appendChild(chk);
    const img = document.createElement('img');
    if (avatar) {
      img.setAttribute('src', avatar);
    }
    row.appendChild(img);
    const uname = document.createElement('div');
    uname.textContent = name ? name : user_id;
    row.appendChild(uname);
    row.addEventListener('click', (e) => {
      chk.checked = !chk.checked;
    });
    chk.addEventListener('click', (e) => {
      e.stopPropagation();  // rowのclickを発生させないように
    });
    this.div_members.appendChild(row);
  }

  _update() {
  }

  _create() {
    const req = {
      'name': (<HTMLInputElement>document.getElementById('title')).value,
      'start': (<HTMLInputElement>document.getElementById('start')).value,
      'end': (<HTMLInputElement>document.getElementById('end')).value,
      'members': [this.user_id]
    };
    const tmp: Array<HTMLInputElement> = <any>document.querySelectorAll('input[type="checkbox"]'); // hack
    tmp.forEach((x) => {
      if (!x.checked) return;
      req['members'].push(x.value);
    });

    let xhr = new XMLHttpRequest();
    xhr.addEventListener("load", () => {
      const resp = xhr.response;
      if (xhr.status !== 200) {
        alert(resp);
      } else {
        location.href = './';
      }
    });
    xhr.open("POST", "api/race?session=" + this.session);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(req));
  }
}

{
  const q = window.location.search;
  let race_id = null;
  if (q && q[0] === '?') {
    q.substring(1).split('&').forEach((kv) => {
      const items = kv.split('=', 2);
      if (items.length === 2 && items[0] === 'id')
        race_id = items[1];
    });
  }
  if (race_id) {
    document.title = 'レースを編集';
  } else {
    document.title = '新しくレースを作成';
  }
  window.addEventListener("DOMContentLoaded", () => new Main(race_id));
}
