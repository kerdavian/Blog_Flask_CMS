document.querySelector('#createPost').addEventListener('click', function (e) {
  // if the text area has no text in it, we'll alert the user
  const data = CKEDITOR.instances.body.getData();
  if (!data) {
    alert('Article content is required.');
    e.preventDefault();
  }
});

// if there are toasts visible
// https://picturepan2.github.io/spectre/components/toasts.html
// this will make it dissapear, if the user clicks on the X
const toasts = document.querySelectorAll('.toast button');

toasts.forEach(el => el.addEventListener('click', event => {
  event.target.closest('.toast').remove()
}));