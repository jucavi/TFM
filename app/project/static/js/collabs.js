const collabsList = document.querySelector('#collabs');
const form = document.querySelector('#add_collabs');

form.addEventListener('submit', function (event) {
  const collabs = document.querySelectorAll('.tag');

  // event.preventDefault();
  while (collabsList.lastChild) {
    collabsList.removeChild(collabsList.lastChild);
  }

  for (let i = 0; i < collabs.length; i++) {
    const value = collabs[i].getAttribute('tag-data')

    if (value) {
      const input = document.createElement('input');

      input.setAttribute('id', `collabs-${i}`);
      input.setAttribute('name', `collabs-${i}`);
      input.setAttribute('value', value);

      const li = document.createElement('li');
      li.append(input);

      collabsList.append(li);
    }
  }
});
