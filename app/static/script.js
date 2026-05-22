function carica() {
  var endpoint = document.getElementById('serie').value;
  var da = document.getElementById('da').value;
  var a = document.getElementById('a').value;
  var msg = document.getElementById('msg');
  var tabella = document.getElementById('tabella');
  var tbody = document.getElementById('tbody');

  msg.textContent = '';
  tabella.style.display = 'none';
  tbody.innerHTML = '';

  if (parseInt(a) < parseInt(da)) {
    msg.textContent = 'Errore: "A anno" deve essere >= "Da anno"';
    return;
  }

  var url = endpoint + '?da_anno=' + da + '&a_anno=' + a;

  fetch(url)
    .then(function(res) {
      if (!res.ok) {
        return res.json().then(function(e) { throw new Error(e.detail || res.statusText); });
      }
      return res.json();
    })
    .then(function(dati) {
      if (dati.length === 0) {
        msg.textContent = 'Nessun dato nel range selezionato.';
        return;
      }
      for (var i = 0; i < dati.length; i++) {
        var r = dati[i];
        var tr = document.createElement('tr');
        tr.innerHTML = '<td>' + r.anno + '</td><td>' + (r.area || 'Nazionale') + '</td><td>' + r.valore.toFixed(2) + '</td>';
        tbody.appendChild(tr);
      }
      tabella.style.display = '';
      msg.style.color = 'green';
      msg.textContent = dati.length + ' record caricati.';
    })
    .catch(function(e) {
      msg.style.color = 'red';
      msg.textContent = 'Errore: ' + e.message;
    });
}

carica();
