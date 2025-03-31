// functions for the quiz page

// this large function handles the checking of a user's answer, from displaying results to finding keywords
function check_questions(q_num, q_keywords) {
    document.getElementById('check_answers_'+q_num).style.display='none';
    document.getElementById('question_'+q_num).style.display='none';
    document.getElementById('answer_'+q_num).style.display='block';
    var answer = document.getElementById('question_'+q_num+'_answer').value;
    if (answer != '') { // if the user has written an answer, it will be written in the div mentioned
        document.getElementById('question_'+q_num+'_answer_given').innerHTML=answer;
    } else {    // if there is no answer, it will display this
        document.getElementById('question_'+q_num+'_answer_given').innerHTML='No answer given';
    }
    keyword_list = string_to_array(q_keywords);
    found_keywords = [];
    for (i = 0; i < keyword_list.length; i++) {     // this finds all the keywords in a user's answer
        let re = new RegExp(keyword_list[i], 'i');
        found = answer.match(re);
        if (found != null) {
            found_keywords.push(keyword_list[i]);
        } else {
            // pass
        }
    }
    found_keywords_string = array_to_string(found_keywords);
    if (found_keywords_string.length > 0) {     // if the user's answer contains keywords, it will display them
        document.getElementById('question_'+q_num+'_keywords').innerHTML=found_keywords_string;
    } else {    // if there are no keywords, it will display this
        document.getElementById('question_'+q_num+'_keywords').innerHTML='Could not find any keywords in your answer';
    }
}

// function to split a string into an array
function string_to_array(string) {
    string = string.replace(/\*/g, '');
    const array = string.split('-');
    return array
}

// function to convert an array of data into a concatenated string
function array_to_string(array) {
    string = array.toString();
    return string
}