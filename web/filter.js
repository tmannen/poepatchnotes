var data;
var filteredList;
var maxDisplayLimit = 200;
var displayList = document.getElementById('patchNotes')
var displayTable = document.getElementById('pnotes')
var poeforumroot = "https://www.pathofexile.com/forum/view-thread/"
var list = []
var countMessage = document.querySelector('.count-message');

async function create_list() {
    const response = await fetch('http://s3.eu-north-1.amazonaws.com/poepatchnotes.com/data.json');
    data = await response.json();
    for (var i = 0; i < data.length; i++) {
        var notes = data[i]['notes']
        for (var j = 0; j < notes.length; j++) {
          var note = {'note': notes[j],
                    'url': data[i]['url'],
                    'date': data[i]['date'],
                    'patch': data[i]['patch']}
          list.push(note)
        }
    }

    filteredList = list
    filteredList.sort((a, b) => Date.parse(b['date']) - Date.parse(a['date']))
    generateTable()
}

function myFunction() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    filteredList = list.filter(word => word['note'].toUpperCase().indexOf(filter) > -1);
    filteredList.sort((a, b) => Date.parse(b['date']) - Date.parse(a['date']))
    generateTable()
}


function generateCountMessage() {
  var msg = '',
      matches = filteredList.length;
  switch (true) {
    case (matches === 0):
      msg = 'No matches found';
      break;
    case (matches === 1):
      msg = 'Showing 1 item';
      break;
    case (matches <= maxDisplayLimit):
      msg = 'Showing ' + filteredList.length + ' items';
      break;
    default:
      msg = 'Showing ' + maxDisplayLimit + ' of ' + matches + ' items';
  }
  countMessage.textContent = msg;
}

function generateTable() {
  var frag = document.createDocumentFragment();
  for (var i = 0; i < filteredList.length; i++) {
    if (i < maxDisplayLimit) {
      var item = filteredList[i]
      var tr = document.createElement('tr');
      var pnote = document.createElement('td')
      var date = document.createElement('td')
      var patch = document.createElement('td')
      var url = document.createElement('td')
      pnote.innerHTML = item['note']
      date.innerHTML = item['date']
      patch.innerHTML = item['patch']
      var a = document.createElement('a');
      a.href = poeforumroot.concat(item['url']);
      a.appendChild(document.createTextNode("Source"))
      url.appendChild(a)
      tr.appendChild(pnote)
      tr.appendChild(date)
      tr.appendChild(patch)
      tr.appendChild(url)
      frag.appendChild(tr);
    }
    else break;
  }
  displayTable.innerHTML = '';
  displayTable.appendChild(frag);
  generateCountMessage();
}