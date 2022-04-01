'use strict';
window.addEventListener('load', function () {
    document.getElementById('sign-out').onclick = function () {
        firebase.auth().signOut();
    }

    var uiConfig = {
        signInSuccessUrl: '/',
        signInOptions: [
            firebase.auth.EmailAuthProvider.PROVIDER_ID
        ]
    };

    var loginInfo = document.getElementById('login-info')
    var authContainer = document.getElementById('firebase-auth-container')


    firebase.auth().onAuthStateChanged(function (user) {
        if (user) {
            if (loginInfo)
                document.getElementById('login-info').hidden = false;
            document.getElementById('nav_login').innerHTML = "My account"
            document.getElementById('sign-out').hidden = false;
            user.getIdToken().then(function (token) {
                document.cookie = "token=" + token + ";path=/";
            });
        } else {
            if (loginInfo)
                document.getElementById('login-info').hidden = true;
            if (authContainer) {
                var ui = new firebaseui.auth.AuthUI(firebase.auth());
                ui.start('#firebase-auth-container', uiConfig);
            }
            document.getElementById('nav_login').innerHTML = "Log in/Register"
            document.getElementById('sign-out').hidden = true;
            document.cookie = "token=" + ";path=/";
        }
    }, function (error) {
        console.log(error);
        alert('Unable to log in: ' + error);
    });
})
