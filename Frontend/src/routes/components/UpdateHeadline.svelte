<script>
    import { favArticles } from "./store.js";
    export let headline;
    let old_headline = headline; // Store the initial headline
    let newHeadline = ''; // Variable to hold the new headline input
    let showForm = false; // State to toggle the form visibility

    // Function to handle the headline update
    async function updateHeadline(event) {
        event.preventDefault(); // Prevent the default form submission behavior

        try {
            // Send a PUT request to update the headline
            const response = await fetch('http://127.0.0.1:5000/editHeadline', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ old_headline: headline, new_headline: newHeadline }) // Send old and new headlines in the request body
            });

            const result = await response.json(); // Parse the JSON response

            if (response.ok) {
                // Update the headline in the favArticles store
                favArticles.update(articles =>
                    articles.map(article =>
                        article.headline === headline ? { ...article, headline: newHeadline } : article
                    )
                );
                alert(result.message); // Show success message
                showForm = false; // Hide form after successful update
            } else {
                alert(result.error); // Show error message if the response is not ok
            }
        } catch (error) {
            console.error('Error:', error); // Log any errors to the console
            alert('An error occurred while updating the headline.'); // Show a generic error message
        }
    }

    // Function to toggle the form visibility
    function toggleForm() {
        showForm = !showForm;
    }
</script>

<div class="my-5">
    <!-- Button to toggle the update form -->
    <button type="button" class="bg-blue-500 text-white border-none py-2 px-4 cursor-pointer rounded text-sm hover:bg-blue-700" on:click={toggleForm}>Update Headline</button>
    {#if showForm}
        <!-- Form to input the new headline -->
        <form class="mt-2" on:submit={updateHeadline}>
            <input type="text" class="py-2 text-sm mr-2 border border-gray-300 rounded" bind:value={newHeadline} placeholder={old_headline} required/>
            <button type="submit" class="bg-green-500 text-white border-none py-2 px-4 cursor-pointer rounded text-sm hover:bg-green-700">Submit</button>
        </form>
    {/if}
</div>
