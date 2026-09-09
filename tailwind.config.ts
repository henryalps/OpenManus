import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Brand Factory studio palette — calm dark workbench so product
        // colours and logos read accurately against neutral chrome.
        canvas: {
          bg: "#0e1116",
          panel: "#161b22",
          panel2: "#1c232c",
          border: "#2a323d",
          hover: "#222a34",
        },
        ink: {
          DEFAULT: "#e6edf3",
          muted: "#9aa7b4",
          faint: "#6b7682",
        },
        brand: {
          DEFAULT: "#ff6b2c", // Brand Factory orange
          soft: "#ffb38a",
          deep: "#c84e16",
        },
        ok: "#3fb950",
        warn: "#d29922",
        danger: "#f85149",
      },
      fontFamily: {
        sans: ["var(--font-sans)", "system-ui", "sans-serif"],
        mono: ["ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
      },
      borderRadius: {
        xl: "0.9rem",
      },
    },
  },
  plugins: [],
};

export default config;
