function hideQuestions(){
    var questions = document.getElementsByClassName("card");
    for(var i = 0; i < questions.length; i++){
        questions[i].style.display = "none";
    }
}

function changeActivePage(new_active){
    var pages = document.getElementsByClassName("page-item")
    for(var i = 0; i < pages.length; i++){
        if (pages[i].getAttribute('for') == new_active){
            pages[i].classList.add('active');
            pages[i].style = 'cursor: default'
        } else {
            pages[i].classList.remove('active');
            pages[i].style = 'cursor: pointer'
        };
    }
}

function showQuestion(question_id) {
    hideQuestions()
    var question = document.getElementById(question_id);
    question.style.display = "block";
    changeActivePage(question_id)
}

function checkAllAnswered() {
    var questions = document.getElementsByClassName("card")
    for(var i = 0; i < questions.length; i++){
        var options = questions[i].getElementsByClassName('form-check-input')
        have_answer = false
        for(var j = 0; j < options.length; j++){
            have_answer = have_answer || options[j].checked
        }
        if (!have_answer){
            submit_btn = document.getElementsByClassName('btn')[0]
            submit_btn.disabled=true
            return null
        }
    }
    submit_btn.disabled=false
}