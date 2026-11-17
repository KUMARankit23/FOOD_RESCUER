/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: { 400: '#3F654A', 600: '#294A35' },
        sage: { 300: '#829B78' },
        'soft-sage': '#E8EFE5',
        cream: '#F8F5ED',
        ivory: '#FFFDF8',
        sand: '#EDE5D7',
        beige: '#E7D8C2',
        terracotta: '#C77C55',
        'soft-orange': '#E6A46E',
        'golden-yellow': '#E8C77B',
        'text-primary': '#29362C',
        'text-secondary': '#727B70',
        'text-muted': '#A0A69B',
        success: '#43865B',
        warning: '#D69B43',
        danger: '#C65C50',
        info: '#6689A4',
      },
      fontFamily: {
        heading: ['Plus Jakarta Sans', 'system-ui', 'sans-serif'],
        body: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['Fira Code', 'monospace'],
      },
      borderRadius: {
        sm: '8px',
        md: '12px',
        lg: '16px',
      },
    },
  },
  plugins: [],
}
