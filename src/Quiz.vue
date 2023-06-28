<script setup>
///
/// Component for a Quiz
///
/// Props are:
/// name - String that will be used as $name in questions
/// questions - array of questions, each one has:
///    question - text of question (maybe with $name for name)
///    choices - array of choices

import Likert from './Likert.vue';

const props = defineProps(['name', 'questions']);

</script>

<style>
</style>

<template>

    <div class="w-full">
    <p class="text-lg">How would {{name}} answer the following questions?</p>
    <template v-for="(question, index) in questions">
        <Likert :choices="question.choices">
            <span class="text-base">{{question.question}}</span>
        </Likert>
    </template>
    <span class="float-right">→</span>
    </div>
</template>
