<script setup>

import { nextTick, ref, watch } from 'vue';
import MarkdownItModule from 'markdown-it';
import MarkdownItAttrs from 'markdown-it-attrs';
import MarkdownItIns from 'markdown-it-ins';
import MarkdownItMark from 'markdown-it-mark';
import TextareaGrow from './TextareaGrow.vue';
import DOMPurify from 'dompurify';

const props = defineProps(['dialog', 'options', 'userInputDisabled']);
const emit = defineEmits(['submit']);

const textareaValue = ref("");
const textareaElem = ref(null);

const md = new MarkdownItModule({})
    .use(MarkdownItAttrs)
    .use(MarkdownItIns)
    .use(MarkdownItMark);

function striped(item) {
    return {
        'bg-stone-100': item.who === 'gpt'
    };
}

function getOption(name, defaultValue) {
    if (props.options === undefined) {
        return defaultValue;
    }
    if (props.options.name === undefined) {
        return defaultValue;
    }
    return props.options.name;
}

function handleButtonClick() {
    emit('submit', textareaValue.value);
    textareaValue.value='';
}

watch(() => { return props.userInputDisabled; }, (newValue) => {
    if (!newValue.value) {
        // When disabled does from true to false, focus the text input
        console.log(textareaElem.value.elem);
        nextTick(() => {
            textareaElem.value.elem.focus();
        });
    }
})
</script>

<template>

    <div class="mx-auto px-4 md:max-w-screen-md">
        <div v-for="item in props.dialog" class="mt-4 mb-4 last:mb-0">
            <div class="flex flex-col">
                <template v-if="item.who === 'human'">
                    <div class="flex justify-end items-end gap-x-1">
                        <div class="shrink-0 order-last mr-1">
                            <img src="/images/anonymous.png" class="w-[72px] h-[72px] aspect-auto rounded-full" width="72" height="72">
                        </div>
                        <div class="bg-blue-500 text-white rounded-2xl px-3 py-2 max-w-[67%] whitespace-normal" style="overflow-wrap: anywhere;">
                            <div
                                class="markdown flex flex-col gap-y-2"
                                v-html="DOMPurify.sanitize(md.render(item.what))"
                            />                                
                        </div>
                    </div>
                </template>
                <template v-if="item.who === 'gpt'">
                    <div class="flex justify-start items-end gap-x-1">
                        <div class="shrink-0 order-first mr-1">
                            <img :src="item.emotion ? `/ashani/${item.emotion}.png` : '/ashani/neutral.png'"
                                class="w-[72px] h-[72px] transition ease-in-out hover:scale-[3.0] aspect-auto rounded-full" width="72" height="72">
                        </div>
                        <div class="bg-stone-200 text-stone-900 rounded-2xl px-3 py-2 max-w-[67%] whitespace-normal" style="overflow-wrap: anywhere;">
                            <div
                                v-if="item.what !== ''"
                                class="markdown flex flex-col gap-y-2"
                                v-html="DOMPurify.sanitize(md.render(item.what))"
                            />                                
                            <div v-if="item.what === ''" class="dot-flashing mx-4" />
                        </div>
                    </div>
                </template>
            </div>
        </div>
        <div class="my-4">
        </div>
    </div>
    <div class="mx-auto px-4 md:max-w-screen-md border-stone-200">
        <div class="w-full p-4 h-fit border-t">
            <div class="flex gap-x-2 items-end">
                <TextareaGrow ref="textareaElem" v-model="textareaValue" @keyup.enter.exact="handleButtonClick" :disabled="userInputDisabled"/>
                <button @click="handleButtonClick" class="flex-none rounded-full align-bottom p-1 mb-1 ml-2 bg-blue-500 transition hover:opacity-75 text-white h-8 w-8">
                    <!-- <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" className="w-6 h-6">
                        <path strokeLinecap="round" strokeLinejoin="round" stroke-width="1.8" d="M4.5 10.5L12 3m0 0l7.5 7.5M12 3v18" />
                    </svg> -->
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                    </svg>
                </button>
            </div>
        </div>
    </div>

</template>
