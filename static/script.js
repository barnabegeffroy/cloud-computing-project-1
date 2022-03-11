window.addEventListener('load', function () {
    document.getElementById('sign-out').onclick = function () {
        firebase.auth().signOut();
    }

    firebase.auth().onAuthStateChanged(function (user) {
        if (user) {
            document.getElementById('nav_login').innerHTML = "My account"
            document.getElementById('sign-out').hidden = false;
            user.getIdToken().then(function (token) {
                document.cookie = "token=" + token + ";path=/";
            });
        } else {
            document.getElementById('nav_login').innerHTML = "Log in/Register"
            document.getElementById('sign-out').hidden = true;
            document.cookie = "token=" + ";path=/";
        }
    })
})
