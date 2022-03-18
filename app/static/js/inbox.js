const url = document.querySelector('#inbox_messages').href + '__inbox_messages';

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
  const { data } = await axios.get(url);
  updateNewMessages(data.inbox_messages_count);
}, 60000)