<script setup>

import { ref, onMounted, watch, nextTick } from 'vue';
const elem = ref(null);
const props = defineProps(['modelValue']);
const emit = defineEmits(['update:modelValue']);

function resize() {
    elem.value.style.height = '';
    elem.value.style.height = elem.value.scrollHeight + 4 + 'px';
}

function handleInput(evt) {
    resize();
    // Also send value update
    emit('update:modelValue', evt.target.value);
}

watch(props, () => {
    // If the value changes, resize
    // Needs to be next tick to avoid native element changing size now
    nextTick(() => {
        resize();
        elem.value.scrollIntoView({ behavior: 'smooth' });
    });
});

onMounted(() => {
    resize();
});

defineExpose({
    elem,
});
</script>

<template>
    <textarea :value="props.modelValue" ref="elem" @input="handleInput" class="flex grow w-full rounded-md bg-transparent px-3 py-2 text-normal
        resize-none overflow-hidden
        focus-visible:outline-none
        focus-visible:ring-2
        disabled:cursor-not-allowed
        disabled:opacity-50
        border-stone-400 border-2
        placeholder:text-stone-400"
        rows="1"
        placeholder="Write your text here"
        autofocus>
    </textarea>
</template>
