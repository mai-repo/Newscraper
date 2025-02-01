<script>
    import DeleteButton from './DeleteButton.svelte';
    import { userData, favArticles } from './store.ts';
    let userName;
    $: userName = $userData.name;

    async function getFav() {
        try {
            const response = await fetch(`http://127.0.0.1:5000/favorites/${userName}`);
            const data = await response.json();
            favArticles.set(data.favorites);
            alert('Successfully grabbed the favorites');
        } catch (error) {
            console.error('Error fetching the favorite articles:', error);
            return { error: 'Error fetching the favorite articles' }; // Return an error JSON object
        }
    }
</script>
<div class="p-4">
    <button on:click={getFav}> See All Your Favorite Articles </button>
    {#if $favArticles.length > 0}
    <!-- content here -->
    {#each $favArticles as favorite}
        <div class="p-4 bg-white w-1/2 rounded-lg mb-2">
            <h1 class="mb-2 text-2xl text-blue-800">Headline: {favorite.headline}</h1>
            <p class="mb-2">{favorite.summary}</p>
            <a class="text-sm text-indigo-500" href="{favorite.link}" target="_blank">Read more</a>
            <DeleteButton id={favorite.id}> Delete Article </DeleteButton>
        </div>
    {/each}
    {/if}
</div>