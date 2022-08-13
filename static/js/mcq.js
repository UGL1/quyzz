console.log("script loaded OK");
const slides = document.getElementsByClassName('slide');
const progressBar = document.getElementById('questionProgress')
const questionNumberLabel = document.getElementById('questionNumberLabel');
console.log(slides.length);
let questionCounter = 0;
displayQuestion()

function displayQuestion() {
    for (let i = 0; i < slides.length; i++) {
        if (i === questionCounter) {
            slides[i].style.display = 'block';
        } else {
            slides[i].style.display = 'none';
        }
    }
    let text = (questionCounter + 1).toString() + " / " + slides.length.toString();
    let value = Math.floor((questionCounter + 1) / slides.length * 100).toString();
    console.log("value", value);
    questionNumberLabel.innerText = "question " + text;
    progressBar.style.width = value + "%";


}

function buttonTest(element) {
    questionCounter += 1;
    questionCounter %= slides.length;
    displayQuestion()

}