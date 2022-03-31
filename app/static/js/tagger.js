const hiddenElemetsDiv = document.querySelector('#hidden_elements');
const input = document.querySelector('#tag_input');
const tagsContainer = document.querySelector('#tags_container');
let tags = new Set();

// Getting elements send from flask, add to <datalist> as options and remove from html
window.onload = (function (hiddenElementsDiv) {
  try {
    const elements = JSON.parse(hiddenElementsDiv.innerHTML).elements;
    const datalist = document.querySelector('#elements');
    hiddenElemetsDiv.innerHTML = '';

    for (let element of elements) {
      const option = document.createElement('option');

      option.value = element;
      datalist.appendChild(option);
    }
    return elements;
  } catch (e) {
    return [];
  }
})(hiddenElemetsDiv);

function newTag(tagLabel) {
  const tag = document.createElement('span');
  const tagContent = document.createTextNode(tagLabel);
  tag.setAttribute('class', 'tag');
  tag.setAttribute('tag-data', tagLabel);
  tag.appendChild(tagContent);


  const close = document.createElement('span');
  close.setAttribute('class', 'remove-tag');
  close.innerHTML = 'x';
  close.onclick = handleRemoveTag;

  tag.appendChild(close);
  return tag
}

function reset(parent) {
  while (parent.firstChild) {
    parent.removeChild(parent.firstChild);
  }
}

function addTags() {
  reset(tagsContainer);
  for (let tag of [...tags].reverse()) {
    const divTag = newTag(tag);
    tagsContainer.prepend(divTag);
  }
  input.value = '';
  input.focus();
}

// Prevent default form behavior
input.addEventListener('keydown', function (e) {
  if (e.key === 'Enter') e.preventDefault();
});

// add tag
input.addEventListener('keyup', function (e) {
  e.preventDefault();
  if (e.key === 'Enter' && this.value) {
    tags.add(this.value);
    addTags(tags);
    this.value = '';
  }
});

// remove tag
const handleRemoveTag = function (event) {
  const label = event.target.parentNode.getAttribute('tag-data');
  if (label) {
    tags.delete(label)
    addTags();
  }
};

