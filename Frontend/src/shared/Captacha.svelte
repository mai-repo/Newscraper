<script>
    let verification = false;
    // Function to handle reCAPTCHA verification
    async function notARoboto(event) {
        event.preventDefault()
        const token = grecaptcha.getResponse();

        if(token) {
            // Send the token to the backend for verification
            fetch('/verifyUser', {
                method: 'POST',
                header: {
                    contentType: 'application/json'
                },
                body: JSON.stringify({ token: token }) // Send the reCAPTCHA token for verification
            })
            .then (response => response.json())
            .then(data => {
                console.log(data);
                verification = true;
            }).catch(error =>
                console.log(error)
            )
        }
    }
</script>

<section>
    <!-- Google reCAPTCHA widget -->
    <div class="g-recaptcha" data-sitekey="6LeM28EqAAAAADi454gZP51XpzLYYyb7XVf21wQH"></div>

</section>