
import { createRouter, createWebHistory } from 'vue-router';

import Chat from './Chat.vue';
import Demo from './Demo.vue';
import Hero from './Hero.vue';
import NotFound from './NotFound.vue';
import TokenDemo from './TokenDemo.vue';

export const SERVER = (import.meta.env.MODE === 'development') ? 'http://localhost:5050' : location.origin;
export const WS_SERVER = (import.meta.env.MODE === 'development') ? 'ws://localhost:5050' : location.origin;

export const routes = [
    { path: '/', component: Hero },
    { path: '/chat', component: Chat },
    { path: '/demo', component: Demo },
    { path: '/tokens', component: TokenDemo },
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
