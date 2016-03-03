"use strict";
// JQuery that submits a hidden form
// that copies and pastes all of the HTML
// on the prescription dashboard page
// so that flask can email user their information

var emailButton = $("#email-button");

function updateForm() {
    $('#prescription-html')[0].value = $('#prescription-html')[0].innerHTML;

}

// Event Listener
emailButton.click(updateForm);