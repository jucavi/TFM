document.addEventListener('DOMContentLoaded', function () {
  const rows = document.querySelectorAll('tr[data-href]');
  const trashLinks = document.querySelectorAll('.row_delete_link');

  rows.forEach(function (row) {
    row.style.cursor = 'pointer';
    row.addEventListener('click', function () {
      window.location.href = row.dataset.href;
    })
  });

  trashLinks.forEach(function (link) {
    link.addEventListener('click', async function (e) {
      e.preventDefault();
      e.stopImmediatePropagation()
      await axios.delete(e.target.href)
      window.location.href = window.location.href;
    });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const trashLinks = document.querySelectorAll('.row_delete_link');

  trashLinks.forEach(function (link) {
    link.addEventListener('click', async function (e) {
      e.preventDefault();
      e.stopImmediatePropagation();
      await axios.delete(e.target.href);
      location.reload();
    });
  });
});