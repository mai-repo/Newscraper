import { writable } from "svelte/store";


export const userData = writable({});
export const message = writable(false);
export const articlesData = writable([]);
export const favArticles = writable([]);
export const news = writable([]);