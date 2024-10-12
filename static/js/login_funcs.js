// functions for the login page

function login_account() {
    document.getElementById('create_acc').style.display='none'
    document.getElementById('login_acc').style.display='none'
    document.getElementById('login_form').style.display='block'
    document.getElementById('choice_text').innerHTML='Login to your account'
}
function create_account() {
    document.getElementById('create_acc').style.display='none'
    document.getElementById('login_acc').style.display='none'
    document.getElementById('create_form').style.display='block'
    document.getElementById('create_check').style.display='block'
    document.getElementById('choice_text').innerHTML='Create an account'
}