const subjectInput =
    document.getElementById("subject");

const chapterInput =
    document.getElementById("chapter");

const totalQuestionsInput =
    document.getElementById("totalQuestions");


const generateBtn =
    document.getElementById("generateBtn");

const printBtn =
    document.getElementById("printBtn");


const sheetSubject =
    document.getElementById("sheetSubject");

const sheetChapter =
    document.getElementById("sheetChapter");

const sheetTotal =
    document.getElementById("sheetTotal");

const groupCount =
    document.getElementById("groupCount");

const completedCount =
    document.getElementById("completedCount");

const progressText =
    document.getElementById("progressText");

const progressBar =
    document.getElementById("progressBar");

const questionsGrid =
    document.getElementById("questionsGrid");


/* GENERATE TRACKER */

generateBtn.addEventListener(
    "click",
    generateTracker
);


function generateTracker() {

    const subject =
        subjectInput.value;

    const chapter =
        chapterInput.value.trim();

    const total =
        parseInt(
            totalQuestionsInput.value
        );


    if (!chapter) {

        alert(
            "Please enter your chapter name."
        );

        chapterInput.focus();

        return;
    }


    if (!total || total <= 0) {

        alert(
            "Please enter valid total PYQs."
        );

        totalQuestionsInput.focus();

        return;
    }


    /* UPDATE HEADER */

    sheetSubject.textContent =
        subject.toUpperCase();

    sheetChapter.textContent =
        chapter;

    sheetTotal.textContent =
        total;


    /* CALCULATE GROUPS */

    const groups =
        Math.ceil(total / 10);

    groupCount.textContent =
        groups;


    /* CLEAR OLD BOXES */

    questionsGrid.innerHTML = "";


    /* CREATE BOXES */

    let start = 1;


    while (start <= total) {

        const end =
            Math.min(
                start + 9,
                total
            );


        const label =
            document.createElement("label");

        label.className =
            "question-box";


        const checkbox =
            document.createElement("input");

        checkbox.type =
            "checkbox";


        const text =
            document.createElement("span");

        text.textContent =
            `Questions ${start}–${end}`;


        checkbox.addEventListener(
            "change",
            function () {

                label.classList.toggle(
                    "checked",
                    checkbox.checked
                );

                updateProgress();

            }
        );


        label.appendChild(
            checkbox
        );

        label.appendChild(
            text
        );

        questionsGrid.appendChild(
            label
        );


        start += 10;
    }


    /* RESET PROGRESS */

    completedCount.textContent =
        `0 / ${groups}`;

    progressText.textContent =
        "0%";

    progressBar.style.width =
        "0%";


    /* SCROLL TO PREVIEW */

    document
        .querySelector(".preview-section")
        .scrollIntoView({
            behavior: "smooth"
        });

}


/* UPDATE PROGRESS */

function updateProgress() {

    const boxes =
        document.querySelectorAll(
            ".question-box input"
        );


    const checked =
        document.querySelectorAll(
            ".question-box input:checked"
        );


    const totalGroups =
        boxes.length;

    const completedGroups =
        checked.length;


    completedCount.textContent =
        `${completedGroups} / ${totalGroups}`;


    let percentage =
        (completedGroups / totalGroups) * 100;


    if (!totalGroups) {

        percentage = 0;
    }


    progressText.textContent =
        Math.round(percentage) + "%";


    progressBar.style.width =
        percentage + "%";
}


/* PRINT */

printBtn.addEventListener(
    "click",
    function () {

        const boxes =
            document.querySelectorAll(
                ".question-box"
            );


        if (boxes.length === 0) {

            alert(
                "Please generate a PYQ tracker first."
            );

            return;
        }


        window.print();

    }
);
