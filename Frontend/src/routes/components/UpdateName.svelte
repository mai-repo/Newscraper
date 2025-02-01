<script>
    import { favArticles } from "./store.ts";
    export let headline;
    let old_headline = headline;
    let newHeadline = '';
    let showForm = false;

    async function updateHeadline(event) {
        event.preventDefault();

        try {
            const response = await fetch('http://127.0.0.1:5000/editHeadline', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ old_headline: headline, new_headline: newHeadline })
            });

            const result = await response.json();

            if (response.ok) {
                favArticles.update(articles =>
                    articles.map(article =>
                        article.headline === headline ? { ...article, headline: newHeadline } : article
                    )
                );
                alert(result.message);
                showForm = false; // Hide form after successful update
            } else {
                alert(result.error);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while updating the headline.');
        }
    }

    function toggleForm() {
        showForm = !showForm;
    }
</script>

<div class="my-5">
    <button type="button" class="bg-blue-500 text-white border-none py-2 px-4 cursor-pointer rounded text-sm hover:bg-blue-700" on:click={toggleForm}>Update Headline</button>
    {#if showForm}
        <form class="mt-2" on:submit={updateHeadline}>
            <input type="text" class="py-2 text-sm mr-2 border border-gray-300 rounded" bind:value={newHeadline} placeholder={old_headline} />
            <button type="submit" class="bg-green-500 text-white border-none py-2 px-4 cursor-pointer rounded text-sm hover:bg-green-700">Submit</button>
        </form>
    {/if}
</div>
