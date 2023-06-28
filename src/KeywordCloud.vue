<script setup>

const props = defineProps(["keywords"]);

</script>

<template>
    <p class="w-full leading-loose">
        <template v-for="keyword in props.keywords">
            <span class="whitespace-nowrap rounded-full bg-blue-100 px-2.5 py-0.5 text-sm text-blue-700">{{keyword}}</span>
            <span class="whitespace-normal">&nbsp;</span>
        </template>
    </p>
</template>
