<script setup>

import MarkdownItModule from 'markdown-it';
import MarkdownItAttrs from 'markdown-it-attrs';
import MarkdownItIns from 'markdown-it-ins';
import MarkdownItMark from 'markdown-it-mark';
import { Codemirror } from "vue-codemirror";

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
                                class="w-[72px] h-[72px] aspect-auto rounded-full" width="72" height="72">
                        </div>
                        <div class="bg-stone-200 text-stone-900 rounded-2xl px-3 py-2 max-w-[67%] whitespace-normal" style="overflow-wrap: anywhere;">
                            <div
                                class="markdown flex flex-col gap-y-2"
                                v-html="DOMPurify.sanitize(md.render(item.what))"
                            />                                
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
                <textarea class="flex grow w-full rounded-md bg-transparent px-3 py-2 text-normal
                    resize-y
                    focus-visible:outline-none
                    focus-visible:ring-2
                    disabled:cursor-not-allowed
                    disabled:opacity-50
                    border-stone-400 border-2
                    placeholder:text-stone-400
                    min-h-[45px]"
                    rows="1"
                    placeholder="Write your text here"></textarea>
            </div>
        </div>
    </div>

</template>
