<script>
    import DeleteButton from './DeleteButton.svelte';
    import { userData, favArticles } from './store.ts';
    import UpdateHeadline from './UpdateHeadline.svelte';
    $: userName = $userData.name;

    // Function to fetch favorite articles for the user
    async function getFav() {
        try {
            const response = await fetch(`http://127.0.0.1:5000/favorites/${userName}`);
            const data = await response.json();
            favArticles.set(data.favorites); // Update the store with fetched favorite articles
            alert('Successfully grabbed the favorites');
        } catch (error) {
            console.error('Error fetching the favorite articles:', error);
            return { error: 'Error fetching the favorite articles' }; // Return an error JSON object
        }
    }
</script>

<div class="p-4">
    <!-- Button to trigger fetching of favorite articles -->
    <button class="px-4 py-2 mb-4 bg-blue-700 text-white rounded hover:bg-blue-700" on:click={getFav}> See All Your Favorite Articles </button>

    {#if $favArticles.length > 0}
    <!-- Loop through each favorite article and display its details -->
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
    {/if}
</div>