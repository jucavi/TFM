document.addEventListener('DOMContentLoaded', function () {
  const rows = document.querySelectorAll('tr[data-href]');

  rows.forEach(function (row) {
    row.style.cursor = 'pointer';
    row.addEventListener('click', function () {
      window.location.href = row.dataset.href;
    })
  });
});