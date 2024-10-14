// functions for the login page

// function to display account login form on button press
function login_account() {
    document.getElementById('create_acc').style.display='none'
    document.getElementById('login_acc').style.display='none'
    document.getElementById('login_form').style.display='block'
    document.getElementById('choice_text').innerHTML='Login to your account'
}
// function to display create account form on button press
function create_account() {
    document.getElementById('create_acc').style.display='none'
    document.getElementById('login_acc').style.display='none'
    document.getElementById('create_form').style.display='block'
    document.getElementById('choice_text').innerHTML='Create an account'
}

// defining of vaiables for password security checking
var pword_input = document.getElementById('new_pword');
var pword_length = document.getElementById('len_check');
var pword_lower = document.getElementById('lower_check');
var pword_upper = document.getElementById('upper_check');
var pword_number = document.getElementById('num_check');
var pword_special = document.getElementById('spec_check');
// defining all regex of characters
var lower_case_letters = /[a-z]/g;
var upper_case_letters = /[A-Z]/g;
var numbers = /[0-9]/g;
var special_characters = /[-’/`~!#*$@_%+=.,^&(){}[\]|;:”<>?\\]/g

// starts checking the user's inputs
pword_input.onkeyup = function() {
    // length validation
    if(pword_input.value.length >= 8) {
        pword_length.classList.remove('invalid');
        pword_length.classList.add('valid');
    } else {
        pword_length.classList.remove('valid');
        pword_length.classList.add('invalid');
    }
    // lowercase validation
    if(pword_input.value.match(lower_case_letters)) {
        pword_lower.classList.remove('invalid')
        pword_lower.classList.add('valid')
    } else {
        pword_lower.classList.remove('valid')
        pword_lower.classList.add('invalid')
    }
    // uppercase validation
    if(pword_input.value.match(upper_case_letters)) {
        pword_upper.classList.remove('invalid');
        pword_upper.classList.add('valid');
    } else {
        pword_upper.classList.remove('valid');
        pword_upper.classList.add('invalid');
    }
    // number validation
    if(pword_input.value.match(numbers)) {
        pword_number.classList.remove('invalid');
        pword_number.classList.add('valid');
    } else {
        pword_number.classList.remove('valid');
        pword_number.classList.add('invalid');
    }
    // special character validation
    if(pword_input.value.match(special_characters)) {
        pword_special.classList.remove('invalid')
        pword_special.classList.add('valid')
    } else {
        pword_special.classList.remove('valid')
        pword_special.classList.add('invalid')
    }
}