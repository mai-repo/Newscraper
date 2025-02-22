<script>
    import { NavBrand, Navbar, NavUl } from 'flowbite-svelte';
    import DeleteButton from '../components/DeleteButton.svelte';
    import FavPokemon from '../components/FavPokemon.svelte';
    import { userData, favArticles } from '../components/store.ts';
    import UpdateHeadline from '../components/UpdateHeadline.svelte';
    import { HomeSolid } from 'flowbite-svelte-icons';

    $: userName = $userData.name;

    let showPokemon = false; // State variable to control display

    // Function to fetch favorite articles for the user
    async function getFav() {
        try {
            const response = await fetch(`http://127.0.0.1:5000/favorites/${userName}`);
            const data = await response.json();
            favArticles.set(data.favorites); // Update the store with fetched favorite articles
            showPokemon = false; // Ensure articles are shown
            alert('Successfully grabbed your favorite Articles');
        } catch (error) {
            console.error('Error fetching the favorite articles:', error);
            alert("data.error")
        }
    }

    // Function to fetch favorite Pokemon
    async function getPokemon() {
        // Add your logic to fetch Pokemon here
        showPokemon = true; // Ensure Pokemon are shown
        alert('Successfully grabbed the Pokemon');
    }
</script>

<div class="p-6 flex flex-col items-center">
    <!-- Button to trigger fetching of favorite articles -->
    <Navbar class="bg-pink-200 w-full">
        <NavBrand href="/Scrape" class="text-2xl text-blue-700 p-4">
            <HomeSolid class="text-blue-700 w-10 h-10"> </HomeSolid> Home
        </NavBrand>
        <NavUl>
            <button class="px-4 py-2 mb-4 bg-blue-700 text-white rounded hover:bg-blue-700" on:click={getFav}> See All Your Favorite Articles </button>
            <button class="px-4 py-2 mb-4 bg-green-700 text-white rounded hover:bg-green-700" on:click={getPokemon}> Get Favorite Pokemon </button>
        </NavUl>
    </Navbar>

    {#if showPokemon}
        <div class="mt-4 w-full flex justify-center">
            <FavPokemon/>
        </div>
    {:else}
        {#if $favArticles.length > 0}
        <!-- Loop through each favorite article and display its details in a grid -->
            <div class="w-full max-w-6xl grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {#each $favArticles as favorite}
                    <div class="p-4 bg-white rounded-lg mb-2">
                        <h1 class="mb-2 text-2xl text-blue-800">Headline: {favorite.headline}</h1>
                        <!-- Component to update the article's title -->
                        <UpdateHeadline headline={favorite.headline}> Change Title </UpdateHeadline>
                        <p class="mb-2">{favorite.summary}</p>
                        <a class="text-sm text-indigo-500" href="{favorite.link}" target="_blank">Read more</a>
                        <!-- Component to delete the article -->
                        <DeleteButton id={favorite.id}> Delete Article </DeleteButton>
                    </div>
                {/each}
            </div>
        {/if}
    {/if}
</div>