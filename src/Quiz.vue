<script setup>
///
/// Component for a Quiz
///
/// Props are:
/// name - String that will be used as $name in questions
/// questions - array of strings, with $name

import Likert from './Likert.vue';

const props = defineProps(['name', 'questions']);

</script>

<style>
</style>

<template>

    <template v-for="(question, index) in questions">
        <Likert>
            <span class="text-base">{{question.replace("$name", props.name)}}</span>
        </Likert>
    </template>

</template>
