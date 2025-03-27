// functions for the subject page

function display_subject_options(subject, user) {
    if (document.getElementById(subject+'_options').style.display=='none') {
        document.getElementById(subject+'_options').style.display='block'
        document.getElementById('welcome_text').innerHTML=(subject + ' has been selected')
        var forms = document.querySelectorAll('form')
        for (let i = 0; i < forms.length; i++) {
            forms[i].style.display='none'
        }
    }
    else {
        document.getElementById(subject+'_options').style.display='none'
        document.getElementById('welcome_text').innerHTML=('Here are your subjects, '+user)
        var forms = document.querySelectorAll('form')
        for (let i = 0; i < forms.length; i++) {
            forms[i].style.display='none'
        }
    }
}
function create_quiz(subject) {
    document.getElementById('available_subjects').style.display='none'
    document.getElementById('welcome_text').innerHTML='Create a '+subject+' quiz'
    document.getElementById('create_'+subject+'_quiz_form').style.display='block'
}
function create_question(subject) {
    document.getElementById('welcome_text').innerHTML='Create a '+subject+' question'
    document.getElementById('create_'+subject+'_form').style.display='block'
}