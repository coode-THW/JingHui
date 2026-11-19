/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        paper: '#f6f2e9', ink: '#252a28', cinnabar: '#a94b3c', azure: '#2e4858', gilt: '#b59461'
      },
      fontFamily: { serif: ['"Noto Serif SC"', 'serif'], sans: ['"Noto Sans SC"', 'sans-serif'] }
    }
  },
  plugins: []
}
