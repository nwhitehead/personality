
import { createRouter, createWebHistory } from 'vue-router';

import Demo from './Demo.vue';
import Hero from './Hero.vue';
import NotFound from './NotFound.vue';

export const SERVER = (import.meta.env.MODE === 'development') ? 'http://localhost:5050' : location.origin;
export const WS_SERVER = (import.meta.env.MODE === 'development') ? 'ws://localhost:5050' : location.origin;

export const routes = [
    { path: '/', component: Hero },
    { path: '/demo', component: Demo },
    { path: '/:pathMatch(.*)', component: NotFound },
];

export const router = createRouter({
    history: createWebHistory(),
    routes,
});

let uuid = 0;

export function generateUUID() {
    uuid++;
    return uuid.toString();
}
