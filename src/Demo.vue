
<script setup>

import { ref, computed } from 'vue';
import { get_encoding, encoding_for_model } from "@dqbd/tiktoken";

const encoder = get_encoding("gpt2");

const inputText = ref("");

const stats = computed(() => {
    return {
        characters: inputText.value.length,
        tokens: encoder.encode(inputText.value).length,
    };
});

</script>

<template>

    <section>
        <div class="container mx-auto max-w-screen-xl flex flex-col items-center justify-center px-16">

            <div class="text-4xl md:text-5xl font-display font-semibold text-blue-950">
                <p class="text-center leading-relaxed">
                    Token Counter
                </p>
            </div>
        </div>
    </section>

    <section>
        <p>Enter text here:</p>
        <textarea rows="10" cols="50" v-model="inputText">
        </textarea>
        <p>
        <br>Characters: {{ stats.characters }}
        <br>Tokens: {{ stats.tokens }}
        </p>
    </section>

</template>
