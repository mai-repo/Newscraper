<script>
    import Captacha from '../shared/Captacha.svelte';
    import Scrape from '../shared/Scrape.svelte';
    import Users from '../shared/Users.svelte';
    import {message} from '../shared/store.ts'

    let verification = false;

// Function to handle reCAPTCHA verification in parent
function handleVerification(success) {
    if (success) {
        verification = true;
        console.log('Verification successful');
        alert($message)
    } else {
        console.log('Verification failed');
    }
}
</script>

<main class="flex flex-col justify-space-evenly gap-2 p-6 bg-pink-200">
    <header class="flex justify-center py-7 px-6">
        <h1 class="text-center text-6xl font-mono text-black">
            User Authentication Required:
            <br /> Click to Confirm You Are Not a Robot
        </h1>
    </header>
    <section class="flex justify-center py-3 px-3">
        <form>
            <Users/>
            <Captacha onVerification={handleVerification} />
        </form>
    </section>
    {#if message && verification === true}
        <Scrape/>
    {/if}
</main>