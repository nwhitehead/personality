<script setup>

import { ref, onMounted, onUnmounted } from 'vue';
import ethan_png from '../images/ethan.png';
import ashani_png from '../images/ashani.png';
import julia_png from '../images/julia.png';
import emir_png from '../images/emir.png';

const ashaniEmotion = ref('smile-1');

function getAshaniEmotionImage() {
    return `/ashani/${ashaniEmotion.value}.png`;
}

function blink() {
    // Constants and amount of delay are purely based on what "seems" good
    const delay = 5000 + (Math.random() * 3000 - 1500);
    setTimeout(() => {
        // Check if we are in smile-1 state, if so blink, otherwise wait again
        if (ashaniEmotion.value === 'smile-1') {
            ashaniEmotion.value = 'smile-1-blink';
            const delay = 150 + (Math.random() * 50 - 25);
            setTimeout(() => {
                ashaniEmotion.value = 'smile-1';
                blink();
            }, delay);
        } else {
            blink();
        }
    }, delay);
}

function randomEmotion() {
    const delay = 3000 + (Math.random() * 3000);
    setTimeout(() => {
        const emotions = ['angry', 'disgust', 'embarrassed', 'frown-1', 'frown-2', 'frown-3', 'neutral', 'sleepy-1', 'smile-2', 'smile-3', 'smirk', 'surprised', 'surprised-2'];
        const emotion = emotions[Math.floor(Math.random() * emotions.length)];
        if (Math.random() < 0.5) {
            ashaniEmotion.value = 'smile-1';
        } else {
            ashaniEmotion.value = emotion;
        }
        randomEmotion();
    }, delay);
}

onMounted(() => {
    blink();
    randomEmotion();
});

</script>

<style>
.pic {
    @apply w-full;
}
figure {
    text-align: center;
}
</style>
<template>

<section>
    <div class="container mx-auto max-w-screen-xl flex flex-col items-center justify-center px-16">

        <div class="text-4xl md:text-5xl font-display font-semibold text-orange-950">
            <p class="text-center leading-relaxed">
                <span class="text-orange-700 drop-shadow-lg">Create personalities</span> that can talk and play
            </p>
            <p class="text-center leading-relaxed text-3xl">
                Easy conversational and emotion technology at your fingertips
            </p>
        </div>
    </div>
</section>

<section>
    <div class="container mx-auto max-w-screen-xl flex flex-col items-center px-16">
        <div class="flex flex-row">
            <img :src="ethan_png" class="w-full min-w-0" />
            <img :src="ashani_png" class="w-full min-w-0" />
            <img :src="julia_png" class="w-full min-w-0" />
            <img :src="emir_png" class="w-full min-w-0" />
        </div>
        <!-- <div class="flex flex-row">
            <img src="images/eunji.png" class="w-full" />
            <img src="images/jaden.png" class="w-full" />
            <img src="images/emily.png" class="w-full" />
            <img src="images/zara.png" class="w-full" />
        </div> -->

        <div class="flex flex-row my-64">
            <figure class="pic">
                <img :src="getAshaniEmotionImage()" class="w-64 rounded-full" /><figcaption>Ashani has emotions.</figcaption>
            </figure>
        </div>
    </div>
</section>

<section>
<!-- Content -->
</section>

</template>
