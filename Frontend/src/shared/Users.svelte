<script>
    import { onMount } from 'svelte'; // Import onMount for lifecycle hook
    import {userData} from './store.ts';
    import {message} from './store.ts';

    // Function for handling user sign-in with Google Identity Services
    async function userSignIn(response) {
        // response.credential contains the token provided by Google
        const token = response.credential;
        fetch('http://127.0.0.1:5000/userSignIn', {
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
            userData.update(() => data);
            message.set(true);
        })
        .catch(error => {
            console.log(error);
        });
    }
    onMount(() => {
    window.userSignIn = userSignIn;
    });
</script>

<section>
    <!-- Include Google Identity Services API (User Login) -->
    <script src="https://accounts.google.com/gsi/client" async defer></script>
    <!-- Google Identity Services onload configuration -->
    <div id="g_id_onload"
        data-client_id="188533997003-j4rjj645s98u01bcqcbvpe33dcaf3ukd.apps.googleusercontent.com"
        data-callback="userSignIn"
        data-auto_prompt="false">
    </div>

    <!-- Google Sign-In button -->
    <div class="g_id_signin" data-type="standard"></div>
</section>

