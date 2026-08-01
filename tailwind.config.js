/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        paper: "#F4F6F9",
        ink: {
          DEFAULT: "#14182B",
          soft: "#1D2238",
          muted: "#2A2F49",
        },
        slate: {
          text: "#5B6478",
        },
        signal: {
          DEFAULT: "#FFB100",
          soft: "#FFE3A8",
        },
        ready: {
          DEFAULT: "#14B8A6",
          soft: "#CFF5F0",
        },
        gap: {
          DEFAULT: "#FF6B5E",
          soft: "#FFDAD6",
        },
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Public Sans'", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      borderRadius: {
        card: "18px",
      },
      boxShadow: {
        card: "0 1px 2px rgba(20, 24, 43, 0.04), 0 8px 24px rgba(20, 24, 43, 0.05)",
      },
    },
  },
  plugins: [],
};
