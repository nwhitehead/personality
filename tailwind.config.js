/** @type {import('tailwindcss').Config} */

import forms from '@tailwindcss/forms';

export default {
  content: [
    "./**/*.{js,html,vue}",
  ],
  theme: {
    extend: {
        screens: {
            print: {raw: 'print'},
        },
        fontFamily: {
            'special': ['Lato', 'sans-serif'],
        },
    },
  },
  plugins: [
    forms,
  ],
}
