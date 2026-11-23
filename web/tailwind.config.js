/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    // 项目 CSS 全部使用 max-width 断点；若后续用工具类表达「≤768」，必须用 max-md:/max-lg:/max-sm:，不要写 md:。
    screens: { sm: '480px', md: '768px', lg: '1080px' },
    extend: {
      colors: {
        paper: '#f6f2e9', ink: '#252a28', cinnabar: '#a94b3c', azure: '#2e4858', gilt: '#b59461'
      },
      fontFamily: { serif: ['"Noto Serif SC"', 'serif'], sans: ['"Noto Sans SC"', 'sans-serif'] }
    }
  },
  plugins: []
}
