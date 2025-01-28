<script>
    import Captacha from '../shared/Captacha.svelte';
    import Users from '../shared/Users.svelte';

    let verification = false;
    let message = false;
</script>

<main class="flex flex-col justify-space-evenly gap-2 p-6 bg-pink-200">
    <header class="flex justify-center py-7 px-6">
        <h1 class="text-center text-6xl font-mono text-black">
            User Authentication Required:
        <br /> Click to Confirm You Are Not a Robot
        </h1>
    </header>
    <section class="flex justify-center py-3 px-3">
        <form class="text-center bg-white rounded-lg shadow-lg" onsubmit="{notARobot()}">
        <Users>
        </Users>
        <Captacha>
        </Captacha>
        <button type="submit" class="p-4 bg-indigo-300 rounded-lg mt-4">
        Submit
        </button>
        </form>
    </section>
    <!-- {#if message === true && verification === true}
        {window.location.href = "/scrape_page"}
    {/if} -->
</main>