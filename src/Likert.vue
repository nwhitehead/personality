<script setup>
///
/// Component for Likert scale
/// This shows a horizontal line with circles for choices
/// Usual choices are things like "Strongly disagree", "Disagree", "Neither agree nor disagree", "Agree", "Strongly agree"
///
/// Slot is:
/// Prompt for response
///
/// Props are:
/// choices - Array of choice text
///
/// You can set CSS styling by setting CSS variables in parent elements to get non-default values:
///   --likert-circle-color
///   --likert-border-color
///   --likert-border-width
///   --likert-circle-size
///   --likert-line-width
///   --likert-line-color
///   --likert-selected-color

import { ref } from 'vue';

const props = defineProps(['choices']);
const choices = props.choices || ['Strongly disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly agree'];

let selected = ref('');

</script>

<style>
.likert-scale {
    width: 100%;
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
    margin-top: calc(var(--likert-circle-size, 2em) / 2 - var(--likert-line-width, 3px) / 2);
    border-top-width: var(--likert-line-width, 3px);
    border-top-color: var(--likert-line-color, #b45309);
}
.likert-response:first-child .likert-line:first-child {
    visibility: hidden;
}
.likert-response:last-child > .likert-line:nth-child(2) {
    visibility: hidden;
}
.likert-indicator {
    display: inline-block;
    width: var(--likert-circle-size, 2em);
    height: var(--likert-circle-size, 2em);
    border-radius: calc(var(--likert-circle-size, 2em) / 2);
    border-width: var(--likert-border-width, 3px);
    border-color: var(--likert-border-color, #b45309);
    background-color: var(--likert-circle-color, #e7e5e4);
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    top: 0;
    box-sizing: border-box;
    transition: all linear 200ms;
}
.likert-response:hover .likert-indicator {
    background-color: white;
    border-width: calc(var(--likert-border-width, 3px) + 2px);
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
    box-shadow: 0 0 5px 2px color-mix(in srgb, var(--likert-circle-color, #b45309) 50%, transparent);
}
.likert-response > input:checked + .likert-indicator {
    background-color: var(--likert-selected-color, #b45309);
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
            <div id="likert-legend" class="likert-legend"><slot /></div>
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
