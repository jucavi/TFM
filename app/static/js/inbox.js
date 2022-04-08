try {
  const url = document.querySelector('#inbox_messages').href + '/__inbox_messages';

  window.onload = async function () {
      try {
        const { data } = await axios.get(url);
        updateNewMessages(data.inbox_messages_count);
      } catch (e) {
        console.log('Error:', e);
      }
  }();

  function updateNewMessages(n) {
    const spanMessages = document.querySelector('#new_messages');
    if (n) {
      spanMessages.innerText = n;
      spanMessages.style.display = ''
    } else {
      spanMessages.style.display = 'none'
    }
  }

  setInterval(async function () {
    try {
      const { data } = await axios.get(url);
      updateNewMessages(data.inbox_messages_count);
    } catch (e) {
      console.log('Error:', e);
    }
  }, 60000);

} catch (e) {
  console.log(e)
}
