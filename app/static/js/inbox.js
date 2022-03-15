const inBox = document.querySelector('.inbox-messages');

inBox.addEventListener('click', async (event) => {
  event.preventDefault();
  const { data } = await axios.get('http://localhost:5000/messages');
  try {
    const inBoxDiv = document.querySelector('.inbox')
    inBoxDiv.innerHTML = data
  } catch (e) {
    console.log(e)
  }

});