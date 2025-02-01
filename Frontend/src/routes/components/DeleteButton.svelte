<script>
    import { favArticles } from './store.ts';
    export let id;

    async function deleteArticle(id) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/deleteFavorite/${id}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            alert('Favorite deleted successfully');
            favArticles.update(favorites => favorites.filter(fav => fav.id !== id));
        } else {
            const error = await response.json();
            alert(`Error: ${error.error}`);
        }
        } catch (error) {
            console.error('Error deleting article:', error);
            alert('Failed to delete the article.');
        }
    }
</script>

<div>
    <button on:click={() => deleteArticle(id)}>Delete Article</button>
</div>