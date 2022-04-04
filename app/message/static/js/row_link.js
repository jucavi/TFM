document.addEventListener('DOMContentLoaded', function () {
  const rows = document.querySelectorAll('tr[data-href]');

  rows.forEach(function (row) {
    row.style.cursor = 'pointer';
    row.addEventListener('click', function () {
      window.location.href = row.dataset.href;
    })
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const trashLinks = document.querySelectorAll('.row_delete_link');

  trashLinks.forEach(function (link) {
    link.addEventListener('click', async function (event) {
      event.preventDefault();
      event.stopImmediatePropagation();
      try {
        await axios.delete(this.href);
        location.reload();
      } catch (e) {
        console.log(e);
      }
    });
  });
});