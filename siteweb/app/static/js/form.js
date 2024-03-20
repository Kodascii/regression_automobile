$(document).ready(function() {
    $('.field-wrap input, .field-wrap textarea').on('focus', function() {
      $(this).siblings('label').hide();
    }).on('blur', function() {
      $(this).siblings('label').show();
    });
  });