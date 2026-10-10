(function () {
  'use strict';
  var PHONE_RE = /^\+?[\d\s\-()]{7,19}$/;

  document.querySelectorAll('form[data-enquiry-form]').forEach(function (form) {
    var phone = form.querySelector('[name="phone"]');
    var button = form.querySelector('[data-submit]');
    var label = button ? button.textContent : '';

    function checkPhone() {
      if (!phone) return;
      var digits = phone.value.replace(/\D/g, '').length;
      phone.setCustomValidity(PHONE_RE.test(phone.value.trim()) && digits >= 7 ? '' : 'Enter a valid phone number.');
    }

    // Clear server-side error styling once the person edits a field.
    form.addEventListener('input', function (e) { e.target.classList.remove('is-invalid'); });

    form.addEventListener('submit', function (e) {
      checkPhone();
      if (!form.checkValidity()) {
        e.preventDefault();
        e.stopPropagation();
        form.classList.add('was-validated');
        var first = form.querySelector(':invalid');
        if (first) first.focus();
        return;
      }
      if (button) { button.disabled = true; button.textContent = 'Sending…'; }
    });

    // Restore the button if the user comes back with the browser Back button.
    window.addEventListener('pageshow', function () {
      if (button) { button.disabled = false; button.textContent = label; }
    });
  });
})();
