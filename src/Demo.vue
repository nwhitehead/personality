
<script setup>

import { ref, computed } from 'vue';
import Conversation from './Conversation.vue';

const inputText = ref("");
const dialog = [
    { who: 'gpt', what: 'Hello, I\'m Ashani.\n\n*She extends her hand to shake.*\n\nTo whom do I have the pleasure of speaking?' },
    { who: 'human', what: 'Hi, I\'m Nathan.' },
    { who: 'gpt', emotion: 'smile-1', what: 'Hi, Nathan. It\'s nice to meet you. What brings you to my office?' },
    { who: 'human', what: 'I would like to file a complaint.' },
    { who: 'gpt', emotion: 'frown-1', what: 'Oh, I\'m sorry to hear that. What department would you like me to forward it to?' },
    { who: 'human', what: 'Whoever is in charge of college admissions.' },
    { who: 'gpt', emotion: 'frown-1', what: 'Let\'s see, that would be Admissions. What should I tell them the problem is?' },
    { who: 'human', what: 'The rejected my daughter for no reason.' },
    { who: 'gpt', emotion: 'angry', what: 'That is totally unacceptable.' },

];

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
        <Conversation :dialog="dialog" />
    </section>

</template>
