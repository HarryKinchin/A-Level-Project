// functions for the account page

function edit_subjects() {
    document.getElementById('sub_edit').style.display='none'
    document.getElementById('account_info').style.display='none'
    if (document.getElementById('maths_sub').innerHTML='Mathematics') {
        document.getElementById('maths_check').checked=false
    } else {
        document.getElementById('maths_checked').checked=true
    }
    if (document.getElementById('comp_sub').innerHTML='Computer Science') {
        document.getElementById('comp_check').checked=false
    } else {
        document.getElementById('comp_check').checked=true
    }
    document.getElementById('edit_form').style.display='block'
}