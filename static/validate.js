window.onload = function () {

    Array.from(document.getElementsByClassName("min")).forEach(min => {
        min.addEventListener("change", function () {
            let v = parseInt(this.value);
            let max = parseInt(min.parentElement.parentElement.lastElementChild.firstElementChild.value);
            if (v > max) this.value = max;
        });
    });

    Array.from(document.getElementsByClassName("max")).forEach(max => {
        max.addEventListener("change", function () {
            let v = parseInt(this.value);
            let min = parseInt(max.parentElement.parentElement.firstElementChild.lastElementChild.value);
            if (v < min) this.value = min;
        });
    });

}

function dosubmit(formId) {
    var name = document.getElementById("name").setAttribute("form", formId);
    var manufacturer = document.getElementById("manufacturer").setAttribute("form", formId);
    document.getElementById(formId).submit();
}