export function inputPages() {
  const input = document.getElementById('page_input');
  const form = document.getElementById('pageForm');

  if (!input || !form) return;

  input.addEventListener('change', function () {
    form.submit();
  });
}
