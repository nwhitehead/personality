<script setup>

import { ref, reactive } from 'vue';
import Conversation from './Conversation.vue';
import { WS_SERVER, generateUUID } from './config.js';

let connection = new WebSocket(`${WS_SERVER}/api/v1/wschat`);
// A map with keys of id and values of:
//   data: current value
//   update_callback: callback to call on updated incremental values
let response_map = {};

const userSpeaking = ref(true);

const dialog = reactive([
    { who: 'gpt', what: 'Hello, I\'m Ashani.\n\n*She extends her hand to shake.*\n\nTo whom do I have the pleasure of speaking?' },
]);


connection.addEventListener("message", (event) => {
    const msg = JSON.parse(event.data);
    console.log('Vue app got message', msg);
    if (msg.id === undefined) {
        console.log('Message did not include id, ignoring');
        return;
    }
    let resp = response_map[msg.id];
    if (response_map[msg.id] === undefined) {
        console.log('Could not find incremental response to update');
        return;
    }
    if (msg.tag === 'update') {
        response_map[msg.id].data += msg.data;
        const done = false;
        response_map[msg.id].update_callback(response_map[msg.id].data, done);
    } else if (msg.tag === 'done') {
        const done = true;
        response_map[msg.id].update_callback(response_map[msg.id].data, done, msg.data);
        delete response_map[msg.id];
    } else {
        console.log('Unknown msg.tag');
    }
});

function applyDelta(data, delta) {
    for (const [key, value] of Object.entries(delta)) {
        if (key in data) {
            if (typeof data[key] === 'string') {
                data[key] += value;
            } else {
                applyDelta(data[key], value);
            }
        } else {
            data[key] = value;
        }
    }
}
// Call with data having OpenAI fields (e.g. model, messages, etc)
// callback is called on incremental update and for final update
// Always called with latest value, second arg is "final" (true on final update)
async function callChat(data, update_callback) {
    const id = generateUUID();
    const request = { id, tag: "chat", data };
    response_map[id] = { data: "", update_callback };
    connection.send(JSON.stringify(request));
}

function handleSubmit(v) {
    if (v !== '\n') {
        dialog.push({ who: 'human', what: v});
    }
    console.log(connection);
    userSpeaking.value = false;

    callChat({
        model: "gpt-3.5-turbo",
        messages: [
            {role: "system", content:"You are a helpful cheerful assistant."}, 
            {role: "user", content: v},
        ],
        temperature: 0.5,
        max_tokens: 200,
        stream: true,
    }, (txt, done, reason) => {
        console.log('Update partial result: ', txt, done, reason);
        dialog.contents.dialog[1].what = txt;
        if (done) {
            userSpeaking.value = true;
        }
    });
}

</script>

<template>
    <section>
        <Conversation :dialog="dialog" @submit="handleSubmit" :userInputDisabled="!userSpeaking" />
    </section>
</template>
