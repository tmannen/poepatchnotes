console.clear();
var data;

async function create_list() {
    const response = await fetch('http://s3.eu-north-1.amazonaws.com/poepatchnotes.com/data.json');
    data = await response.json();
    var ul = document.getElementById('patchNotes')
    for (var i = 0; i < data.length; i++) {
        var notes = data[i]['notes']
        for (var j = 0; j < notes.length; j++) {
          var li=document.createElement('li');
          li.innerHTML = notes[j]   // Use innerHTML to set the text
          ul.appendChild(li); 
        }
    }
}

(function() {

var list = data,
    filteredList = [],
    maxDisplayLimit = 10,
    textInput = document.querySelector('#textInput'),
    displayList = document.querySelector('#patchNotes'),
    countMessage = document.querySelector('.count-message');

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

function generateList() {
  var frag = document.createDocumentFragment();
  for (var i = 0; i < filteredList.length; i++) {
    if (i < maxDisplayLimit) {
      var item = filteredList[i],
          li = document.createElement('li');
      frag.appendChild(li);
    }
    else break;
  }
  displayList.innerHTML = '';
  displayList.appendChild(frag);
  generateCountMessage();
}

function textMatch(item) {
  var searchTerm = textInput.value.toLowerCase()
  return item.indexOf(searchTerm) !== -1;
}

function getFilteredItems() {
  filteredList = list.filter(textMatch);
  generateList();
}

textInput.addEventListener('keyup', getFilteredItems);

getFilteredItems();

})();