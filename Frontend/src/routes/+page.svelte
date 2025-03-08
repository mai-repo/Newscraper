<script>
    // Import necessary modules and components
    import { Router, Route, navigate } from 'svelte-routing';
    import Captacha from './components/Captacha.svelte';
    import Scrape from './Scrape/+page.svelte'
    import Users from './components/Users.svelte';
    import { message } from './components/store.ts';

    // Initialize verification state
    let verification = false;

    // Function to handle reCAPTCHA verification in parent
    function handleVerification(success) {
        if (success) {
            verification = true; // Set verification to true if successful
            console.log('Verification successful');
            if (verification && $message === true) {
                navigate('/Scrape'); // Navigate to Scrape page if verification and message are true
            }
        } else {
            console.log('Verification failed'); // Log verification failure
        }
    }
</script>

<Router>
    <!-- Main Page -->
    <Route path="/" let:params>
        <main class="flex flex-col justify-space-evenly gap-2 p-6 bg-pink-200">
            <header class="flex justify-center py-7 px-6">
                <h1 class="text-center text-6xl font-mono text-black">
                    User Authentication Required:
                    <br /> Click to Confirm You Are Not a Robot
                </h1>
            </header>
            <section class="flex justify-center py-3 px-3">
                <form class="p-5 bg-white rounded-lg">
                    <Users/> <!-- Users component for user input -->
                    <Captacha onVerification={handleVerification} /> <!-- Captacha component with verification handler -->
                </form>
            </section>
        </main>
    </Route>

    <!-- Scrape page -->
    <Route path="/Scrape">
        <Scrape/> <!-- Scrape component for scraping functionality -->
    </Route>
</Router>