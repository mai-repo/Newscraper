<script>
    import { onMount } from 'svelte'; // Import onMount for lifecycle hook
    import {userData} from './store.ts';
    import {message} from './store.ts';
    import {jwtDecode} from 'jwt-decode';

    // Function for handling user sign-in with Google Identity Services
    async function userSignIn(response) {
        // response.credential contains the token provided by Google
        const token = response.credential;
        const decoded = jwtDecode(token); // Decode JWT

        fetch('https://mai-newscraper.onrender.com/userSignIn', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ token }),
        })
        .then(res => res.json())
        .then(data => {
            console.log(data.message);
            alert(JSON.stringify(data.message));
            userData.set({name: decoded.name});
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

<section class= "mb-4">
    <!-- Include Google Identity Services API (User Login) -->
    <script src="https://accounts.google.com/gsi/client" async defer></script>
    <script src='https://www.googleapis.com/auth/userinfo.profile'></script>
    <!-- Google Identity Services onload configuration -->
    <div id="g_id_onload"
        data-client_id="188533997003-j4rjj645s98u01bcqcbvpe33dcaf3ukd.apps.googleusercontent.com"
        data-callback="userSignIn"
        data-auto_prompt="true">
    </div>

    <!-- Google Sign-In button -->
    <div class="g_id_signin" data-type="standard"></div>
</section>

