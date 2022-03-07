const addCollab = document.querySelector('#add-collab');
const collab = document.querySelector('#collab');

addCollab.addEventListener('click', async (e) => {
  e.preventDefault();
  email = collab.value;
  const res = await axios(document.URL, {
    method: 'POST',
    data: {email: email}
  });
  const status = await res.data;

  if (!status.success) {
    const errors = document.querySelector('.errors');
    errors.innerText = status.msg;
  }
  collab.value = '';
});
