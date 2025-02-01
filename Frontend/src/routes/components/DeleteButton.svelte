<script>
    import { favArticles } from './store.ts'; // Import the favArticles store
    export let id; // Declare a prop to receive the article id

    // Function to delete an article by id
    async function deleteArticle(id) {
        try {
            // Send a DELETE request to the server
            const response = await fetch(`http://127.0.0.1:5000/deleteFavorite/${id}`, {
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

<div>
    <!-- Button to trigger the deleteArticle function -->
    <button on:click={() => deleteArticle(id)}>Delete Article</button>
</div>