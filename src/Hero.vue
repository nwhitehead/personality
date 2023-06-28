<script setup>

import { ref, onMounted, onUnmounted } from 'vue';
import Likert from './Likert.vue';
import Quiz from './Quiz.vue';
import KeywordCloud from './KeywordCloud.vue';

import quiz1 from '../quiz1.txt?raw';

import { BarChart } from 'chartist';
import 'chartist/dist/index.css';

function parseQuiz(txt) {
    let result = [];
    const lines = txt.split(/\r?\n/);
    for (const line of lines) {
        if (line !== '' && line !== '--' && line[0] !== '#') {
            result.push(line);
        }
    }
    return result;
}

const questions = parseQuiz(quiz1);

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
        const emotions = ['angry', 'disgust', 'embarrassed', 'frown-1', 'frown-2', 'frown-3', 'neutral', 'sleepy-1', 'smile-2', 'smile-3', 'smirk', 'surprised', 'surprised-2', 'horrified'];
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

onMounted(() => {
    new BarChart('div#chart',
        {
            labels: ['Warm', 'Stable', 'Assertive', 'Talkative', 'Dutiful', 'Friendly', 'Sensitive', 'Distrust', 'Imagination', 'Reserved', 'Anxious', 'Complex', 'Introvert', 'Orderly', 'Emotional'],
            series: [[3.8689434510233935, 4.42701971561154, 3.6790819536953516, 1.7257258826789301, 3.130443315764404, 2.675490331896998, 2.755685967430919, 2.7427192636076674, 2.5915552619917417, 0.6548714831106989, 2.2935515680822465, 0.8830709743506621, 2.8490051872790643, 0.008619933202794194, 3.09361149503031407]],
        }, {
            stackBars: true,
            reverseData: true,
            horizontalBars: true,
            high: 5,
            low: 0,
            axisY: {
                offset: 100,
            },
            axisX: {
                offset: 20,
            },
            showGridBackground: false,
            height: '400px',
        });
});

const keywords = [
    'People focused',
    'Feeling oriented',
    'Giving and caring',
    'Qualitative over quantitative',
    'Calm',
    'Patient and accepting',
    'Level-headed',
    'Competitive',
    'Intense and passionate',
    'Serious and withdrawn',
    'Postive outlook toward authority',
    'Comfortable alone',
    'Tender and forgiving',
    'Assumes honesty',
    'Direct in speech',
    'Emotionally expressive',
];

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
            <img src="/images/ethan.png" title="Ethan" class="w-full min-w-0" />
            <img src="/images/zara.png" title="Zara" class="w-full min-w-0" />
            <img src="/images/julia.png" title="Julia" class="w-full min-w-0" />
            <img src="/images/jaden.png" title="Jaden" class="w-full min-w-0" />
        </div>
        <div class="flex flex-row">
            <img src="/images/eunji.png" title="Eun-ji" class="w-full min-w-0" />
            <img src="/images/ashani.png" title="Ashani" class="w-full min-w-0" />
            <img src="/images/ming.png" title="Ming" class="w-full min-w-0" />
            <img src="/images/emir.png" title="Emir" class="w-full min-w-0" />
        </div>

        <div class="flex flex-row my-16">
            <figure class="pic">
                <img :src="getAshaniEmotionImage()" class="w-64 rounded-full" /><figcaption>Ashani has emotions.</figcaption>
            </figure>
        </div>
    </div>
</section>

<section>
    <div class="container mx-auto max-w-screen-md flex flex-col items-center px-16">
        <div class="w-full">
            <Quiz :name="'Ashani'" :questions="questions" />
            <h3 class="text-lg">Current Personality Assessment - Ashani</h3>
            <div id="chart" style="width: 100%; height: 100%;" />
            <h3 class="text-lg">Current keywords - Ashani</h3>
            <KeywordCloud :keywords="keywords" />
        </div>
    </div>
</section>


</template>
