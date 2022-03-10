window.addEventListener('load', function () {
    firebase.auth().onAuthStateChanged(function (user) {
        if (user) {

            document.getElementById('edit-car').onclick = function () {
                document.getElementById('edit-car-form').hidden = false;
                document.getElementById('edit-car').hidden = true;
                document.getElementById('hide-edition').hidden = false;
            }
            document.getElementById('hide-edition').onclick = function () {
                document.getElementById('edit-car-form').hidden = true;
                document.getElementById('edit-car').hidden = false;
                document.getElementById('hide-edition').hidden = true;
            }
        } else {
            document.getElementById('edit-car').hidden = true;
            document.getElementById('delete-car-form').hidden = true;
        }
    })
})