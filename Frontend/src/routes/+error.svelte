<script lang="ts">
  import {page} from '$app/state'
  import { onMount } from 'svelte';

  onMount(() => {

    console.log('Error status:', page.status);
    console.log('Error message:', page.error?.message);

    if (page.status === 404) {
      window.location.href = 'https://mai-newscraper.onrender.com/33'; // Redirect for 404 errors
    }

    if (page.status === 500) {
      window.location.href = "https://mai-newscraper.onrender.com/500" // Redirect for 500 errors
    }
    if (!page.status && page.error?.message) {
      console.error('Exception message:', page.error.message);
      window.location.href = "https://mai-newscraper.onrender.com/error"; // redirect for exceptions
    }
  });
</script>

