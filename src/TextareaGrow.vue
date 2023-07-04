<script setup>

import { ref, onMounted } from 'vue';
const elem = ref(null);

function resize() {
    elem.value.style.height = '';
    elem.value.style.height = elem.value.scrollHeight + 4 + 'px';
}
</script>

<template>
    <textarea ref="elem" @input="resize" class="flex grow w-full rounded-md bg-transparent px-3 py-2 text-normal
        resize-none overflow-hidden
        focus-visible:outline-none
        focus-visible:ring-2
        disabled:cursor-not-allowed
        disabled:opacity-50
        border-stone-400 border-2
        placeholder:text-stone-400"
        rows="1"
        placeholder="Write your text here"></textarea>
</template>
