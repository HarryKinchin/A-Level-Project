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

// creating setup for username, email, and password validation
document.getElementById("submit").disabled = true;
var email_valid = false;
var pword_valid = false;
var uname_valid = false;

// creating regex and input reading for username validation
var uname_input = document.getElementById('new_uname');
var uname_regex = /[A-Za-z0-9]+/g;

// username 
uname_input.onkeyup = function() {
    var char_bool = false;
    var length_bool = false;

    if (uname_input.value.match(uname_regex)) {
        char_bool = true;
    } else {
        char_bool = false
    }
    if (uname_input.value.length > 2 && uname_input.value.length < 17) {
        length_bool = true;
    } else {
        length_bool = false;
    }
    if (char_bool == true && length_bool == true) {
        uname_valid = true;
    } else {
        uname_valid = false;
    }
    all_valid()
}
// defining of vaiables for password security checking
var pword_input = document.getElementById('new_password');
var pword_length = document.getElementById('len_check');
var pword_lower = document.getElementById('lower_check');
var pword_upper = document.getElementById('upper_check');
var pword_number = document.getElementById('num_check');
var pword_special = document.getElementById('spec_check');

// defining all regex for password validation
var lower_case_letters = /[a-z]/g;
var upper_case_letters = /[A-Z]/g;
var numbers = /[0-9]/g;
var special_characters = /[^\d\w]/g

// starts checking the user's inputs
pword_input.onkeyup = function() {
    var length_bool = false;
    var lower_bool = false;
    var upper_bool = false;
    var num_bool = false;
    var spec_bool = false;
    // length validation
    if (pword_input.value.length > 7 && pword_input.value.length < 17) {
        pword_length.classList.remove('invalid');
        pword_length.classList.add('valid');
        length_bool = true;
    } else {
        pword_length.classList.remove('valid');
        pword_length.classList.add('invalid');
        length_bool = false;
    }
    // lowercase validation
    if (pword_input.value.match(lower_case_letters)) {
        pword_lower.classList.remove('invalid');
        pword_lower.classList.add('valid');
        lower_bool = true;
    } else {
        pword_lower.classList.remove('valid');
        pword_lower.classList.add('invalid');
        lower_bool = false;
    }
    // uppercase validation
    if (pword_input.value.match(upper_case_letters)) {
        pword_upper.classList.remove('invalid');
        pword_upper.classList.add('valid');
        upper_bool = true;
    } else {
        pword_upper.classList.remove('valid');
        pword_upper.classList.add('invalid');
        upper_bool = false;
    }
    // number validation
    if (pword_input.value.match(numbers)) {
        pword_number.classList.remove('invalid');
        pword_number.classList.add('valid');
        num_bool = true;
    } else {
        pword_number.classList.remove('valid');
        pword_number.classList.add('invalid');
        num_bool = false;
    }
    // special character validation
    if (pword_input.value.match(special_characters)) {
        pword_special.classList.remove('invalid');
        pword_special.classList.add('valid');
        spec_bool = true;
    } else {
        pword_special.classList.remove('valid');
        pword_special.classList.add('invalid');
        spec_bool = false;
    }
    if (length_bool == true && lower_bool == true && upper_bool == true && num_bool == true && spec_bool == true) {
        pword_valid = true;
    } else {
        pword_valid = false;
    }
    all_valid()
}

// Setting up variables for email validation (regex for email found using the RFC2822 Email formatting)
var email_input = document.getElementById('new_email');
var email_regex = /[-!"£$%^&*(){}[\]#~'@;:?.>,<A-Za-z0-9]+[@][-!"£$%^&*(){}[\]#~'@;:?.>,<A-Za-z0-9]+[.][a-z]+/g;

// Function for making sure email is in a valid format: "abc@def.ghi"
email_input.onkeyup = function() {
    if (email_input.value.match(email_regex)) {
        email_valid = true;
    } else {
        email_valid = false;
    }
    all_valid()
}

// function to check for a valid email and password before submission
function all_valid() {
    if (pword_valid == true && email_valid == true && uname_valid == true) {
        document.getElementById("submit").disabled = false;
    } else {
        document.getElementById("submit").disabled = true;
    }
}
