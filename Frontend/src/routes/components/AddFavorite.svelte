<script>
    import { API_BASE_URL } from '../../config.js';

    // Import the userData store from the store.ts file
    import {userData} from './store.ts'

    // Declare a prop for the news_id
    export let news_id

    // Declare a variable for the username
    let username

    // Reactive statement to update the username whenever userData changes
    $: username = $userData.name

    // Function to add a favorite news item
    async function addFavorite() {
        try {
            // Send a POST request to the server to add the favorite
            const response = await fetch(`${API_BASE_URL}/addFavorites`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    news_id: news_id,
                    username: username
                }),
            });

            // Check if the response is successful
            if (response.ok) {
                console.log("Favorite is added");
                alert("Favorite added successfully!");
            } else if (response.status === 400) {
                // Handle the case where the favorite is already added
                alert("You already added this!");
            }
        } catch (error) {
            // Log any errors that occur during the fetch
            console.error('Error adding to Favorites!', error);
        }
    }
</script>

<div class="py-2">
    <!-- Button to trigger the addFavorite function -->
    <button class="bg-blue-800 hover:bg-blue-700 text-white py-2 px-4 rounded" on:click={addFavorite}>Add to Favorites</button>
</div>