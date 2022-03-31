const hiddenElemetsDiv = document.querySelector('#hidden_elements');
// { elements: [list of hidden elements] }
const tagContainer = document.querySelector('.tag_container');
const input = document.querySelector('#label_input');
let tags = [];

const elements = (window.onload = function (hiddenElementsDiv) {
  try {
    const elements = JSON.parse(hiddenElementsDiv.innerHTML).elements;

    hiddenElemetsDiv.innerHTML = '';
    return elements;
  } catch (e) {
    return [];
  }
})(hiddenElemetsDiv);

function bestMatch(elements, input) {
  if (!input) return [];

  return elements.filter((element) => {
    return element.startsWith(input);
  });
}

function createTags(label) {
  const div = document.createElement('div');
  div.setAttribute('class', 'tag border my-1 me-1');
  const span = document.createElement('span');
  span.setAttribute('class', 'label_value');
  span.innerHTML = label;
  const closeBtn = document.createElement('i');
  closeBtn.setAttribute('class', 'fa-solid fa-xmark ps-3');
  closeBtn.setAttribute('tag-data', label);

  div.appendChild(span);
  div.appendChild(closeBtn);
  return div;
}

function reset() {
  document.querySelectorAll('.tag').forEach(function (tag) {
    tag.parentElement.removeChild(tag);
  });
}

function addTags() {
  reset();
  for (let tag of [...tags].reverse()) {
    const input = createTags(tag);
    tagContainer.prepend(input);
  }
  input.value = '';
  input.focus();
}

input.addEventListener('keydown', function (e) {
  if (e.key === 'Enter') e.preventDefault();
});

let find = false;
input.addEventListener('keyup', function (e) {
  const completeDiv = document.querySelector('#text_suggest');
  match = bestMatch(elements, input.value);

  completeDiv.innerText = match[0] ? match[0] : '';

  if (e.key === 'Enter') {
    if (this.value) {
      if (find === false) {
        e.preventDefault();
        this.value = match[0] || this.value;
        find = true;
      } else {
        tags.push(this.value);
        addTags();
        completeDiv.innerText = '';
        find = false;
      }
    }
  }
});

document.addEventListener('click', function (event) {
  if (event.target.tagName === 'I') {
    const label = event.target.getAttribute('tag-data');
    const index = tags.indexOf(label);
    tags = [...tags.slice(0, index), ...tags.slice(index + 1)];
    addTags();
  }
});
