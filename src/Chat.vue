<script setup>

import { ref, reactive } from 'vue';
import Conversation from './Conversation.vue';

const userSpeaking = ref(true);

const dialog = reactive([
    { who: 'gpt', what: 'Hello, I\'m Ashani.\n\n*She extends her hand to shake.*\n\nTo whom do I have the pleasure of speaking?' },
]);

function handleSubmit(v) {
    if (v !== '\n') {
        dialog.push({ who: 'human', what: v});
    }
    userSpeaking.value = false;
    setTimeout(() => {
        userSpeaking.value = true;
    }, 1000);
}

</script>

<template>
    <section>
        <Conversation :dialog="dialog" @submit="handleSubmit" :userInputDisabled="!userSpeaking" />
    </section>
</template>
