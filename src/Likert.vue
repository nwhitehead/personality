<script setup>

import { ref } from 'vue';

const props = defineProps(['question', 'choices']);

let selected = ref('');

</script>

<style>
.likert-scale {
    margin-bottom: 1em;
    border: none;
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    align-items: flex-start;
    justify-content: space-between;
}
.likert-legend {
    flex: 1 1 auto;
}
.likert-band {
    flex-grow: 4;
    flex-shrink: 0;
    flex-basis: auto;
    display: flex;
    padding-top: 0.6em;
    align-self: stretch;
}
.likert-response {
    flex-grow: 1;
    flex-shrink: 1;
    flex-basis: 0;
    min-width: 1.6em;
    text-align: center;
    position: relative;
}
.likert-line {
    display: inline-block;
    width: 50%;
    vertical-align: top;
    margin-top: 1.0em;
    border-top: 3px solid dimgray;
}
.likert-response:first-child .likert-line:first-child {
    visibility: hidden;
}
.likert-response:last-child > .likert-line:nth-child(2) {
    visibility: hidden;
}
.likert-indicator {
    display: inline-block;
    width: 2em;
    height: 2em;
    border-radius: 1em;
    border: thin solid #006fc4;
    background-color: #faeabd;
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    top: 0;
    box-sizing: border-box;
    transition: all linear 200ms;
}
.likert-response:hover .likert-indicator {
    background-color: white;
    border-width: 3px;
    transition: all linear 200ms;
}
.likert-text {
    display: inline-block;
    padding-top: 0.4em;
    padding-left: 0.4em;
    padding-right: 0.4em;
    width: 100%;
    box-sizing: border-box;
}
.likert-scale .likert-response > input:focus ~ .likert-indicator {
    box-shadow: 0 0 5px 2px rgba(0, 119, 195, 0.5);
}
.likert-response > input:checked + .likert-indicator {
    background-color: #006fc4;
}
.visually-hidden {
    position: absolute;
    overflow: hidden;
    clip: rect(0 0 0 0);
    height: 1px;
    width: 1px;
    margin: -1px;
    padding: 0;
    border: 0;
}

</style>

<template>

        <fieldset className="likert-scale" aria-labelled-by="likert-legend">
            <div id="likert-legend" class="likert-legend">{{question}}</div>
            <div class="likert-band">
                <template v-for="(choice, index) in choices">
                    <label class="likert-response">
                        <span class="likert-line" />
                        <span class="likert-line" />
                        <input type="radio" :id="index" :value="choice" class="visually-hidden" v-model="selected" />
                        <span class="likert-indicator" />
                        <span class="likert-text">{{choice}}</span>
                    </label>
                </template>
            </div>
        </fieldset>

</template>
