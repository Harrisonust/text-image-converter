var body = document.getElementById("body");
var convert_btn = document.getElementById("convert-btn");
body.addEventListener("keydown", function (event) {
    if (event.keyCode === 13) {
        convert_btn.click();
    }
});

function submitForm() {
    var target = document.getElementById("target").value;
    console.log(target);
    var xhr = new XMLHttpRequest();
    var url = 'https://vup8szlkwc.execute-api.ap-east-1.amazonaws.com/default/text-image-converter2';
    xhr.open('POST', url);
    xhr.setRequestHeader('Content-Type', 'application/json');

    var data = {
        "target": target,
        "width": parseInt(document.getElementById("menu").value),
        "horizontal": document.getElementById("flip-cb").checked,
    };

    var canvas = document.getElementById("canvas");
    if (target.length > 0) {
        xhr.send(JSON.stringify(data));
        canvas.innerHTML = "Processing...";
    } else {
        canvas.innerHTML = "Please enter text!";
    }

    // render the canvas
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            console.log(response);
            const canvas = document.getElementById("canvas");
            const flipCb = document.getElementById("flip-cb");
            const fillerInput = document.getElementById("filler-input");
            canvas.innerHTML = "";

            response.forEach((row, i) => {
                row.forEach((cell, j) => {
                    if (flipCb.checked) {
                        if (cell == 1) {
                            const targetIndex = Math.floor(j / parseInt(document.getElementById("menu").value));
                            const filler = fillerInput.value || target[targetIndex];
                            canvas.innerHTML += filler;
                        } else {
                            canvas.innerHTML += "&#12288";
                        }
                    } else {
                        cell.forEach((subCell, k) => {
                            if (subCell == 1) {
                                const filler = fillerInput.value || target[i];
                                canvas.innerHTML += filler;
                            } else {
                                canvas.innerHTML += "&#12288";
                            }
                        });
                        canvas.innerHTML += "<br>";
                    }
                });
                if (flipCb.checked) {
                    canvas.innerHTML += "<br>";
                }
            });
        } else if (xhr.readyState === 4 && xhr.status !== 200) {
            document.getElementById("canvas").innerHTML = "Error! Please try again.";
        }
    };

}

function copyToClipboard() {
    var result = document.getElementById("canvas").innerText;
    var el = document.createElement('textarea');
    el.value = result;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    var hint = document.getElementById("copy-btn");
    hint.innerHTML = "Copied!";
    setTimeout(function () {
        hint.innerHTML = "Copy Result";
    }, 2000);
}