const memberSelect = document.querySelector('#members');
const emailsOptions = memberSelect.querySelectorAll('option');
const mailListInput = document.querySelector('.mailList');
mailListInput.name = memberSelect.name;
memberSelect.name = '';

const mailList = []

emailsOptions.forEach(option => {
  if (option.value) {
    option.addEventListener('click', addEmailToList);
  }
});

function addEmailToList() {
  this.style.display = 'none';
  this.parentNode.firstChild.selected = true;
  mailList.push(this.value);

  mailListInput.value = mailList.join(', ');
}