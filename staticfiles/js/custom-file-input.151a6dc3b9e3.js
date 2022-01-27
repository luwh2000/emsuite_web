
// Small script for animating Bootstrap's .custom-file-input element.

var elem = document.querySelector('.custom-file-input');
if (elem) {
  elem.addEventListener('change', function (e) {
    var fileName = e.target.files[0].name;
    var label = document.querySelector('label.custom-file-label[for="' + e.target.id + '"]');
    label.innerText = fileName;
  });
}
