<script>
    import {userData} from './store.ts'
    export let news_id
    let username
    $: username = $userData.name

    async function addFavorite() {
        try {
            const response = await fetch(`http://127.0.0.1:5000/addFavorites`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    news_id: news_id,
                    username: username
                }),
            });

            if (response.ok) {
                console.log("Favorite is added");
                alert("Favorite added successfully!");
            } else if (response.status === 400) {
                alert("You already added this!");
            }
        } catch (error) {
            console.error('Error adding to Favorites!', error);
        }
    }
</script>

<div>
    <button on:click={addFavorite}>Add to Favorites</button>
</div>