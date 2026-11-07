// Landing page CSS (contrl.ai/index.html), built ahead of time instead of the Tailwind Play CDN
// (which compiled the styles in every visitor's browser before the page could paint).
// Rebuild after changing classes in index.html:  tools/tailwind/build.sh
// The deploy workflow also rebuilds it, so a missed rebuild never ships missing styles.
module.exports = {
  content: ['./index.html'],
  theme: {
    extend: {
      fontFamily: { sans: ['Pretendard', '-apple-system', 'BlinkMacSystemFont', 'system-ui', 'sans-serif'] },
      colors: { accent: '#F27A2E', cocoa: '#524438', cream: '#f9f6f2' },
    },
  },
};
