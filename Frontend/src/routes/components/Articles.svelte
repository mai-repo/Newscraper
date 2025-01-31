<script>
    import { onMount } from "svelte";
    let articles = {}

    async function fetchNews() {
        try {
            const response = await fetch('http://127.0.0.1:5000/scrape');
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

<main class="flex flex-col justify-center items-center py-5 gap-3">
    <h1 class="text-3xl text-red-400"> Articles from the Atlantic </h1>
    {#if articles.length > 0}
        <!-- content here -->
        {#each articles as article}
            <div class="p-4 bg-white w-1/2 rounded-lg">
                <h1 class="mb-2 text-2xl text-blue-800">Headline: {article.headline}</h1>
                <p class="mb-2">{article.summary}</p>
                <a class="text-sm text-indigo-500" href="{article.link}" target="_blank">Read more</a>
            </div>
            <span class="p-1 bg-black"></span>
        {/each}
    {/if}
</main>