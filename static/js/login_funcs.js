// functions for the login page, including: changing from the 'create/login' to whichever is chosen

function login_account() {
    document.getElementById('create_acc').style.display='none'
    document.getElementById('login_acc').style.display='none'
    document.getElementById('login_form').style.display='block'
}
function create_account() {
    document.getElementById('create_acc').style.display='none'
    document.getElementById('login_acc').style.display='none'
    document.getElementById('create_form').style.display='block'
}
function password_check() {
    var1 = document.getElementById('new_pword').getValue()
    console.log(var1)
}