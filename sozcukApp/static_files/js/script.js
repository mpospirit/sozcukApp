var steps = [
    { question: question_1, answer: answer_1 },
    { question: question_2, answer: answer_2 },
    { question: question_3, answer: answer_3 },
    { question: question_4, answer: answer_4 },
    { question: question_5, answer: answer_5 },
    { question: question_6, answer: answer_6 },
    { question: question_7, answer: answer_7 },
    { question: question_8, answer: answer_8 },
    { question: question_9, answer: answer_9 },
    { question: question_10, answer: answer_10 },
    { question: question_11, answer: answer_11 },
    { question: question_12, answer: answer_12 },
    { question: question_13, answer: answer_13 },
    { question: question_14, answer: answer_14 },
];

// anchor

var score = 0;
var finalScoreToDisplay = 0;
var currentStep = 0;
var revealedLetters = [];
var questionScoreToDisplay = 400;
var answerInput = document.getElementById('answer');
var questionText = document.getElementById('question');
var timer = startTimer(4 * 60, "timer", function () {modal.style.display = "block";});
let elem = document.getElementById("greenBar");
let intervalId;
var arrayOfIndexes = [];
var allLettersAreRevealed = false;
var isEventListenerEnabled = false;
var modal = document.getElementById("myModal");
var btn = document.getElementById("myBtn");
var span = document.getElementsByClassName("close")[0];

function initializeGame() {
    document.addEventListener('keydown', handleKeyDown);
    document.getElementById('score').textContent = score;
    document.getElementById('finalScoreToDisplay').textContent = finalScoreToDisplay;
    questionText.textContent = steps[currentStep].question;
    createAnswerBoxes(steps[currentStep].answer.length);
    document.getElementById('questionScore').textContent = questionScoreToDisplay;
}

function openModal() {
    modal.style.display = "block";
  }

function closeModal() {
    modal.style.display = "none";
}

function createAnswerBoxes(length) {
    answerInput.innerHTML = '';
    for (var i = 0; i < length; i++) {
        var input = document.createElement('input');
        input.setAttribute('type', 'text');
        input.setAttribute('maxlength', '1');
        answerInput.appendChild(input);
        // get all input elements
        var inputs = document.querySelectorAll('input');

        // add event listeners to each input element
        inputs.forEach(function (input, index) {
            // move focus to next input element when a character is entered
            input.addEventListener('input', function () {
                if (this.value.length === 1) {
                    var next = getNextEmptyInput(index);
                    if (next !== undefined) {
                        next.focus();
                    }
                }
            });

            // move focus to previous input element when backspace is pressed
            input.addEventListener('keydown', function (e) {
                if (e.keyCode === 8 && this.value.length === 0) {
                    var previous = getPreviousEmptyInput(index);
                    if (previous !== undefined) {
                        previous.focus();
                    }
                }
            });
        });

        // get the next empty input element
        function getNextEmptyInput(index) {
            for (var i = index + 1; i < inputs.length; i++) {
                if (inputs[i].value.length === 0) {
                    return inputs[i];
                }
            }
        }

        // get the previous empty input element
        function getPreviousEmptyInput(index) {
            for (var i = index - 1; i >= 0; i--) {
                if (inputs[i].value.length === 0) {
                    return inputs[i];
                } else if (inputs[i].disabled || inputs[i].readOnly) {
                    continue;
                } else {
                    return inputs[i];
                }
            }
        }
    }
    disableAllInputBoxes();
}

function enableEventListener() {
    isEventListenerEnabled = true;
}

function disableEventListener() {
    isEventListenerEnabled = false;
}

function handleKeyDown(event) {
    if (isEventListenerEnabled && event.keyCode === 13) {
        disableEventListener();
        checkAnswer();
    }
}

// creating a function disable all input boxes
function disableAllInputBoxes() {
    var inputElements = answerInput.getElementsByTagName('input');
    for (var i = 0; i < inputElements.length; i++) {
        inputElements[i].setAttribute('disabled', 'disabled');
    }
}

// creating a function to enable all input boxes
function enableAllInputBoxes() {
    var inputElements = answerInput.getElementsByTagName('input');
    for (var i = 0; i < inputElements.length; i++) {
        inputElements[i].removeAttribute('disabled');
    }
}

function enableEmptyInputBoxes() {
    var inputElements = answerInput.getElementsByTagName('input');
    for (var i = 0; i < inputElements.length; i++) {
        if (inputElements[i].value.length === 0) {
            inputElements[i].removeAttribute('disabled');
        }
    }
}


function flashScore(duration, color) {
    document.getElementById('score').style.color = color;
    setTimeout(function () {
        document.getElementById('score').style.color = 'black';
    }, duration * 1000);
}

function checkAnswer() {
    var userAnswer = '';
    var inputElements = answerInput.getElementsByTagName('input');
    for (var i = 0; i < inputElements.length; i++) {
        userAnswer += inputElements[i].value;
    }

    if (userAnswer.toLocaleLowerCase('tr-TR') === steps[currentStep].answer) {
        displayFeedback('Tebrikler!', 'green');
        // questionScore = 100 * enabled input boxes count
        var questionScore = 100 * (steps[currentStep].answer.length - document.querySelectorAll('input[disabled]').length);
        score = score + questionScore;
        finalScoreToDisplay = score;
        // score = score + 100 * empty input boxes count
        // score = score + 100 * (steps[currentStep].answer.length);

        flashScore(3, 'green')

        setTimeout(function () {
            document.getElementById('score').style.color = 'black';
        }, 1000);
        currentStep++;
        if (currentStep < steps.length) {
            setTimeout(function () {
                initializeGame();
                document.getElementById('score').textContent = score;
                document.getElementById('finalScoreToDisplay').textContent = finalScoreToDisplay;
                document.getElementById('scoreInput').value = score;
            }, 1000);
        } else {
            setTimeout(function () {
                document.getElementById('score').textContent = score;
                document.getElementById('finalScoreToDisplay').textContent = finalScoreToDisplay;
                document.getElementById('scoreInput').value = score;
                flashScore(3, 'blue')
                openModal();
            }, 1000);
        }
    }
    else {
        displayFeedback('Yanlış', 'red');
        currentStep++;

        flashScore(3, 'red')

        if (currentStep < steps.length) {
            setTimeout(function () {
                document.getElementById('score').textContent = score;
                initializeGame();
            }, 1000);
        } else {
            setTimeout(function () {
                document.getElementById('score').textContent = score;
                flashScore(3, 'blue')
                openModal();
            }, 1000);
            timer.pause();
        }
    }
}

function displayFeedback(message, color) {
    var feedback = document.getElementById('feedback');
    feedback.textContent = message;
    feedback.style.color = color;
    // Clear feedback after 1 second unless it is game completed message
    if (message !== '🎉 Yarışma tamamlandı!') {
        setTimeout(function () {
            feedback.textContent = null;
        }, 1000);
    }
}

function startTimer(seconds, container, oncomplete) {
    var startTime, timer, obj, ms = seconds * 1000,
        display = document.getElementById(container);
    obj = {};
    obj.resume = function () {
        startTime = new Date().getTime();
        timer = setInterval(obj.step, 250); // adjust this number to affect granularity
        // lower numbers are more accurate, but more CPU-expensive
    };
    obj.pause = function () {
        ms = obj.step();
        clearInterval(timer);
    };
    obj.step = function () {
        var now = Math.max(0, ms - (new Date().getTime() - startTime)),
            m = Math.floor(now / 60000), s = Math.floor(now / 1000) % 60;
        s = (s < 10 ? "0" : "") + s;
        display.innerHTML = m + ":" + s;
        if (now == 0) {
            clearInterval(timer);
            obj.resume = function () { };
            if (oncomplete) oncomplete();
        }
        return now;
    };
    obj.resume();
    return obj;
}

function move() {
    let stepValue = 0;
    intervalId = setInterval(frame, 150);

    function frame() {
        if (stepValue > 100) {
            clearInterval(intervalId);
            gonder();
        } else {
            stepValue = (stepValue + 1);
            elem.style.width = (stepValue + 1) + "%";
        }
    }
}

function resetProgressBar() {
    // Stop the animation and reset the width of the progress bar
    clearInterval(intervalId);
    elem.style.width = 0;
}


function harfAl() {
    // displaying the question score
    if (questionScoreToDisplay !== 0) {
        questionScoreToDisplay = questionScoreToDisplay - 100;
    }
    else {
        questionScoreToDisplay = 0;
    }
    document.getElementById('questionScore').textContent = questionScoreToDisplay;

    // revealing a random letter and disabling the textbox

    // checking if the array is empty and creating it if it is
    if (arrayOfIndexes.length === 0) {
        var inputElements = answerInput.getElementsByTagName('input');
        for (var i = 0; i < inputElements.length; i++) {
            arrayOfIndexes.push(i);
        }
    }

    // drawing a random index from the array and removing it from the array
    var randomIndex = Math.floor(Math.random() * arrayOfIndexes.length);
    var randomIndexValue = arrayOfIndexes[randomIndex];
    arrayOfIndexes.splice(randomIndex, 1);

    // revealing the letter
    var inputElements = answerInput.getElementsByTagName('input');
    inputElements[randomIndexValue].value = steps[currentStep].answer[randomIndexValue];
    inputElements[randomIndexValue].disabled = true;

    if (arrayOfIndexes.length === 2) {
        document.getElementById('harfAl').disabled = true;
    }
}

function benjamin() {
    timer.pause();
    move();
    enableEmptyInputBoxes();
    // creating an event listener for enter key to run the checkAnswer function


    // focus on the first empty input box
    var inputElements = answerInput.getElementsByTagName('input');
    for (var i = 0; i < inputElements.length; i++) {
        if (inputElements[i].value.length === 0) {
            inputElements[i].focus();
            break;
        }
    }

    document.getElementById('gonder').disabled = false;
    document.getElementById('benjamin').disabled = true;
    document.getElementById('harfAl').disabled = true;

    // Add animation to "benjaminBar" element
    var benjaminBar = document.getElementById('benjaminBar');
    benjaminBar.style.animation = 'collapse-bar 2s forwards';
}

function gonder() {
    checkAnswer();
    disableAllInputBoxes();
    questionScoreToDisplay = 100 * steps[currentStep].answer.length;
    timer.resume();
    resetProgressBar();
    // clearing the array of indexes
    arrayOfIndexes = [];
    document.getElementById('gonder').disabled = true;
    document.getElementById('benjamin').disabled = false;
    document.getElementById('harfAl').disabled = false;
    allLettersAreRevealed = false;
}

initializeGame();

// TODO
// fix enter key bug