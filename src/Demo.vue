
<script setup>

import { reactive } from 'vue';
import Conversation from './Conversation.vue';
import cholcov_matrix from './cholcov.json';

import randn from '@stdlib/random/base/randn';

const dialog = reactive([
    { who: 'gpt', what: 'Hello, I\'m Ashani.\n\n*She extends her hand to shake.*\n\nTo whom do I have the pleasure of speaking?' },
    { who: 'human', what: 'Hi, I\'m Nathan.' },
    { who: 'gpt', emotion: 'smile-1', what: 'Hi, Nathan. It\'s nice to meet you. What brings you to my office?' },
    { who: 'human', what: 'I would like to file a complaint.' },
    { who: 'gpt', emotion: 'frown-1', what: 'Oh, I\'m sorry to hear that. What department would you like me to forward it to?' },
    { who: 'human', what: 'Whoever is in charge of college admissions.' },
    { who: 'gpt', emotion: 'frown-1', what: 'Let\'s see, that would be Admissions. What should I tell them the problem is?' },
    { who: 'human', what: 'They rejected my daughter for no reason.' },
    { who: 'gpt', emotion: 'angry', what: 'That is totally unacceptable.' },
    { who: 'human', what: 'I know' },
    { who: 'gpt', emotion: 'angry', what: '' },
]);

const choices = [
    "What are you trying to say?",
    "Yeah, that's what I thought as well.",
    "Hmm, I'm not sure.",
    "How about we play a game of number trivia? I'll give you a number, and you have to tell me if it's prime or not.",
];

/// A is 1 x m (vector)
/// B is m x n (matrix)
/// result is A @ B, 1 x n (vector)
function matrix_mult_vm(m, n, A, B) {
    let C = new Array(n);
    for (let i = 0; i < n; i++) {
        C[i] = 0;
    }
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            C[j] += A[i] * B[i][j];
        }
    }
    return C;
}
function handleSubmit(v) {
    const P = 16;
    let z = [];
    for (let i = 0; i < P; i++) {
        z.push(randn());
    }
    let zc = matrix_mult_vm(P, P, z, cholcov_matrix);
    console.log(cholcov_matrix);
    console.log(z, zc);
    let zz = [1,1];
    for (let i = 0; i < 14; i++) {
        zz.push(0);
    }
    let zzc = matrix_mult_vm(P, P, zz, cholcov_matrix);
    console.log('TEST', zzc);
    if (v !== '\n') {
        dialog.push({ who: 'human', what: v});
    }
    
}
</script>

<template>

    <section>
        <div class="container mx-auto max-w-screen-xl flex flex-col items-center justify-center px-16">

            <div class="text-4xl md:text-5xl font-display font-semibold text-blue-950">
                <p class="text-center leading-relaxed">
                    Conversation
                </p>
            </div>
        </div>
    </section>

    <section>
        <Conversation :dialog="dialog" @submit="handleSubmit" :choices="choices" />
    </section>

</template>
