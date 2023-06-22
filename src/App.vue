<script setup>

import { computed, reactive, ref, onMounted, watch } from 'vue';

</script>

<template>
    <div class="w-full top-0 bg-stone-50">
        <div class="max-w-screen-xl px-16 py-20 lg:mx-auto flex justify-between items-center h-16 min-w-[350px]">
            <div class="flex flex-row items-center w-full">
                <div class="bg-blue-500 w-[5px] h-[2em]">
                </div>
                <router-link to="/" class="sm:text-2xl font-bold flex flex-row px-4">
                    ShimmerAI PRO
                </router-link>
                <div class="grow" />
                <router-link to="/team" class="px-4">Team</router-link>
                <router-link to="/features" class="px-4">Features</router-link>
            </div>
        </div>
    </div>

    <div class="min-w-[300px] w-full bg-stone-50">
        <div>
            <router-view>
            </router-view>
        </div>
    </div>

<footer>
    <div class="mx-auto max-w-screen-xl px-4 pt-0 pb-16 md:px-12">
        <div class="mt-8 border-t border-stone-100 pt-8 text-sm text-stone-600">
            <div class="sm:flex sm:justify-between">
                <p>
                    &copy; 2023. Nathan Whitehead. All rights reserved.
                </p>
                <nav aria-label="Footer Navigation - Support" class="mt-4 sm:mt-0">
                    <ul class="flex flex-wrap justify-start gap-4 text-xs lg:justify-end">
                        <li>
                            <router-link to="/" class="legal-link">
                                Home
                            </router-link>
                        </li>
                        <li>
                            <router-link to="/team" class="legal-link">
                                Team
                            </router-link>
                        </li>
                        <li>
                            <router-link to="/terms" class="legal-link">
                                Terms & Conditions
                            </router-link>
                        </li>
                        <li>
                            <router-link to="/privacy" class="legal-link">
                                Privacy Policy
                            </router-link>
                        </li>
                        <li>
                            <router-link to="/cookies" class="legal-link">
                                Cookies
                            </router-link>
                        </li>
                        <li>
                            <router-link to="/contact" class="legal-link">
                                Contact
                            </router-link>
                        </li>
                    </ul>
                </nav>
            </div>
            <div class="flex flex-row">
                <p class="pr-2">Made with</p><div class="grayscale hover:grayscale-0 hover:animate-wiggle hover:cursor-default">💖</div>
            </div>
        </div>
    </div>
</footer>

</template>
