/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0055FF',
        accent: '#2ECC71',
        error: '#D32F2F',
        warning: '#FF9800',
        neutral: '#FFFFFF',
        text: '#1A1A1A',
      },
      fontFamily: {
        sans: ['Inter', 'Roboto', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        'brand': '12px',
      },
    },
  },
  plugins: [],
}

