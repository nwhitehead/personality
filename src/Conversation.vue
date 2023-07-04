<script setup>

import MarkdownItModule from 'markdown-it';
import MarkdownItAttrs from 'markdown-it-attrs';
import MarkdownItIns from 'markdown-it-ins';
import MarkdownItMark from 'markdown-it-mark';

import DOMPurify from 'dompurify';

const props = defineProps(['dialog', 'options']);
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

</script>

<template>

    <div class="mx-auto px-4 md:max-w-screen-md">
        <div v-for="item in props.dialog" class="mt-4 mb-4 last:mb-0">
            <div class="flex flex-col">
                <template v-if="item.who === 'human'">
                    <div class="flex justify-end items-end gap-x-1">
                        <div class="shrink-0 order-last mr-1">
                            <img src="/images/anonymous.png" class="w-[36px] h-[36px] aspect-auto rounded-full" width="36" height="36">
                        </div>
                        <div class="bg-blue-500 text-white rounded-2xl px-3 py-2 max-w-[67%] whitespace-normal" style="overflow-wrap: anywhere;">
                            <div class="flex flex-col gap-y-2">
                                <div
                                    class="markdown"
                                    v-html="DOMPurify.sanitize(md.render(item.what))"
                                />                                
                            </div>
                        </div>
                    </div>
                </template>
                <template v-if="item.who === 'gpt'">
                    <div class="flex justify-start items-end gap-x-1">
                        <div class="shrink-0 order-first mr-1">
                            <img :src="item.emotion ? `/ashani/${item.emotion}.png` : '/ashani/neutral.png'"
                                class="w-[36px] h-[36px] aspect-auto rounded-full" width="36" height="36">
                        </div>
                        <div class="bg-stone-200 text-stone-900 rounded-2xl px-3 py-2 max-w-[67%] whitespace-normal" style="overflow-wrap: anywhere;">
                            <div class="flex flex-col gap-y-2">
                                <div
                                    class="markdown"
                                    v-html="DOMPurify.sanitize(md.render(item.what))"
                                />                                
                            </div>
                        </div>
                    </div>
                </template>
            </div>
        </div>
    </div>

</template>
