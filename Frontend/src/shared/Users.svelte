<script>
    let userData = {};
    let message = null 

    // Function for handling user sign-in with Google Identity Services
    async function userSignIn(response) {
        // response.credential contains the token provided by Google
        const token = response.credential;
        fetch('/userSignIn', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ token }),
        })
        .then(res => res.json())
        .then(data => {
            console.log(data.message);
            alert("Successfully Signed-In");
            userData = data;
            message = true
        })
        .catch(error => {
            console.log(error);
            message = false
        });
    }
</script>

<main>
        <!-- Google Identity Services onload configuration -->
    <div id="g_id_onload"
        data-client_id="188533997003-j4rjj645s98u01bcqcbvpe33dcaf3ukd.apps.googleusercontent.com"
        data-login_uri="https://accounts.google.com/o/oauth2/auth"
        data-callback="userSignIn">
    </div>
    <!-- Google Sign-In button -->
    <div class="g_id_signin" data-type="standard"></div>

</main>

