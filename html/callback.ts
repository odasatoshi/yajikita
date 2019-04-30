class Main {
  constructor() {
    const q = window.location.search;
    let pos = q.indexOf('code=');
    if (pos < 0) {
      alert('login failed');
      location.href = './';
      return;
    }
    pos += 5;
    let pos2 = q.indexOf('&', pos);
    if (pos2 < 0)
      pos2 = q.length;
    const code = q.substring(pos, pos2);
    let xhr = new XMLHttpRequest();
    xhr.addEventListener("load", () => {
      const resp = xhr.response;
      localStorage.setItem('session', resp['session']);
      location.href = './';
    });
    xhr.responseType = "json";
    xhr.open("GET", "api/oauth_callback?code=" + code);
    xhr.send();
  }
}
new Main();
