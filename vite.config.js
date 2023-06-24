
import { defineConfig } from 'vite';
import wasm from "vite-plugin-wasm";
import topLevelAwait from "vite-plugin-top-level-await";
import vue from '@vitejs/plugin-vue';

export default defineConfig({
    plugins: [ wasm(), topLevelAwait(), vue(), ],
})
