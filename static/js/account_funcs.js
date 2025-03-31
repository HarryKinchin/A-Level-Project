// functions for the account page

// this function displays the form to edit a user's subjects
function edit_subjects() {
    document.getElementById('sub_edit').style.display='none'
    document.getElementById('info_edit').style.display='none'
    document.getElementById('account_info').style.display='none'
    document.getElementById('edit_sub_form').style.display='block'
}

// this function displays the form to edit a user's details
function edit_info() {
   document.getElementById('info_edit').style.display='none'
   document.getElementById('sub_edit').style.display='none'
   document.getElementById('account_info').style.display='none'
   document.getElementById('edit_info_div').style.display='block'
}