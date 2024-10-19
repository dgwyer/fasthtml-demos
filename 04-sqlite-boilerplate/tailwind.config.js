/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["**/*.py"],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
