const collabsList = document.querySelector('#collabs');
const form = document.querySelector('#add_collabs');

form.addEventListener('submit', function (event) {
  // event.preventDefault();
  const collabs = document.querySelectorAll('.tag')

  for (let i = 0; i < collabs.length; i++) {
    const input = document.createElement('input')

    input.setAttribute('id', `collabs-${i}`)
    input.setAttribute('name', `collabs-${i}`)
    input.setAttribute('value', collabs[i].innerText)

    const li = document.createElement('li')
    li.append(input)

    collabsList.append(li)
  }
});

