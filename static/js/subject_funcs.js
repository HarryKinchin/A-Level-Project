// functions for the subject page

// this function displays the options for a subject (create quiz or question) and hides the other subjects
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

// this function displays the form to create a quiz for a given subject
function create_quiz(subject) {
    document.getElementById('available_subjects').style.display='none'
    document.getElementById('welcome_text').innerHTML='Create a '+subject+' quiz'
    document.getElementById('create_'+subject+'_quiz_form').style.display='block'
}

// this function displays the form to create a question for a given topic
function create_question(subject) {
    document.getElementById('welcome_text').innerHTML='Create a '+subject+' question'
    document.getElementById('create_'+subject+'_form').style.display='block'
}