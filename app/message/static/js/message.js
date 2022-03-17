const recipientsList = document.querySelector('#recipients');
const form = document.querySelector('#send_message');

form.addEventListener('submit', function (event) {
  // event.preventDefault();
  const recipients = document.querySelectorAll('.tag');

  for (let i = 0; i < recipients.length; i++) {
    const input = document.createElement('input');

    input.setAttribute('id', `recipients-${i}`);
    input.setAttribute('name', `recipients-${i}`);
    input.setAttribute('value', recipients[i].innerText);

    const li = document.createElement('li');
    li.append(input);

    recipientsList.append(li);
  }
});
