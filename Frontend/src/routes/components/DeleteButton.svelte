<script>
    import { API_BASE_URL } from '../../config.js';
    import { favArticles } from './store.ts'; // Import the favArticles store
    export let id;

    // Function to delete an article by id
    async function deleteArticle(id) {
        try {
            // Send a DELETE request to the server
            const response = await fetch(`${API_BASE_URL}/deleteFavorite/${id}`, {
                method: 'DELETE',
            });

            if (response.ok) {
                // If the response is ok, show a success message
                alert('Favorite deleted successfully');
                // Update the favArticles store to remove the deleted article
                favArticles.update(favorites => favorites.filter(fav => fav.id !== id));
            } else {
                // If the response is not ok, show an error message
                const error = await response.json();
                alert(`Error: ${error.error}`);
            }
        } catch (error) {
            // Log and show an error message if the request fails
            console.error('Error deleting article:', error);
            alert('Failed to delete the article.');
        }
    }
</script>

<div class="pt-4">
    <!-- Button to trigger the deleteArticle function -->
    <button class=" p-2 text-white  bg-red-500  hover:bg-blue-700 rounded" on:click={() => deleteArticle(id)}>Delete Article</button>
</div>