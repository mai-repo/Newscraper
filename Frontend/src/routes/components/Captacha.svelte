<script>
    export let onVerification;

    // Function to handle reCAPTCHA verification
    async function notARoboto(event) {
        event.preventDefault();
        const token = grecaptcha.getResponse();

        if (token) {
            // Send the token to the backend for verification
            fetch('https://mai-newscraper.onrender.com/verifyUser', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    token: 'token'
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                onVerification(true);
            })
            .catch((error) => {
                console.error('Error:', error);
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
    <div class="mb-3 g-recaptcha" data-sitekey="6LeM28EqAAAAADi454gZP51XpzLYYyb7XVf21wQH"></div>
    <button class = "p-2 bg-blue-300 rounded-lg" type="submit" on:click={notARoboto}>Submit</button>
</section>
