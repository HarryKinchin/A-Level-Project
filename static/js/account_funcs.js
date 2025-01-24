// functions for the account page

function edit_subjects() {
    document.getElementById('sub_edit').style.display='none'
    document.getElementById('account_info').style.display='none'
    document.getElementById('edit_form').style.display='block'
    if (document.getElementById('maths_sub').innerHTML='Mathematics') {
        document.getElementById('maths_check').checked=true
    } else {
        document.getElementById('maths_checked').checked=false
    }
    if (document.getElementById('comp_sub').innerHTML='Computer Science') {
        document.getElementById('comp_check').checked=true
    } else {
        document.getElementById('comp_checked').checked=false
    }
}