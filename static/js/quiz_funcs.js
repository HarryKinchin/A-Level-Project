function check_questions(q_num, q_keywords) {
    document.getElementById('check_answers_'+q_num).style.display='none';
    document.getElementById('question_'+q_num).style.display='none';
    document.getElementById('answer_'+q_num).style.display='block';
    var answer = document.getElementById('question_'+q_num+'_answer').value;
    if (answer != '') {
        document.getElementById('question_'+q_num+'_answer_given').innerHTML=answer;
    } else {
        document.getElementById('question_'+q_num+'_answer_given').innerHTML='No answer given';
    }
    keyword_list = string_to_array(q_keywords);
    found_keywords = [];
    for (i = 0; i < keyword_list.length; i++) {
        let re = new RegExp(keyword_list[i], 'i');
        found = answer.match(re);
        if (found != null) {
            found_keywords.push(keyword_list[i]);
        } else {
            // pass
        }
    }
    console.log(found_keywords)
    found_keywords_string = array_to_string(found_keywords);
    console.log(found_keywords_string)
    if (found_keywords_string.length > 0) {
        document.getElementById('question_'+q_num+'_keywords').innerHTML=found_keywords_string;
    } else {
        document.getElementById('question_'+q_num+'_keywords').innerHTML='Could not find question keywords';
    }
}
function string_to_array(string) {
    string = string.replace(/\*/g, '');
    const array = string.split('-');
    return array
}
function array_to_string(array) {
    string = array.toString();
    return string
}