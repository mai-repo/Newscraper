<script>
    import { onMount } from "svelte";
    let articles = { }

    async function fetchNews() {
        try {
            const response = await fetch('/scrape');
            const data = await response.json();
            alert(data.message);
            articles = data;
        } catch (error) {
            console.error('Error fetching news:', error);
        }

    }
    onMount(() => {
        fetchNews();
    });
</script>

<main class="flex flex-grow items-center justify-center py-3 px-3">
    {#if articles.length > 0}
        <!-- content here -->
        {#each articles as article}
            <h1>{article.headline}</h1>
            <p>{article.summary}</p>
            <a href="{article.link}">Read more</a>
        {/each}
    {/if}

</main>