<script>
    export let onVerification; // Accept the function passed from the parent

    // Function to handle reCAPTCHA verification
    async function notARoboto(event) {
        event.preventDefault();
        const token = grecaptcha.getResponse();

        if (token) {
            // Send the token to the backend for verification
            fetch('http://127.0.0.1:5000/verifyUser', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ token }) // Send the reCAPTCHA token for verification
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                // Call the function passed from parent on success
                onVerification(true);  // Notify parent of success
            })
            .catch(error => {
                console.log(error);
                onVerification(false); // Notify parent of failure
            });
        } else {
            alert('Please complete the reCAPTCHA.');
        }
    }
</script>

<section>
    <!-- Google reCAPTCHA widget -->
    <!-- Include Google reCAPTCHA API -->
    <script src="https://www.google.com/recaptcha/api.js" async defer></script>
    <div class="g-recaptcha" data-sitekey="6LeM28EqAAAAADi454gZP51XpzLYYyb7XVf21wQH"></div>
    <button type="submit" on:click={notARoboto}>Submit</button>
</section>
