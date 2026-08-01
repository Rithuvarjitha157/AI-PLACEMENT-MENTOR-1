@tailwind base;
@tailwind components;
@tailwind utilities;

html,
body {
  font-family: "Public Sans", sans-serif;
  background-color: #f4f6f9;
  color: #14182b;
}

h1,
h2,
h3,
.font-display {
  font-family: "Space Grotesk", sans-serif;
}

.font-mono-score {
  font-family: "JetBrains Mono", monospace;
  font-variant-numeric: tabular-nums;
}

/* Visible keyboard focus ring, kept consistent across custom components */
:focus-visible {
  outline: 2px solid #ffb100;
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.001ms !important;
  }
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}
::-webkit-scrollbar-thumb {
  background: #d7dce6;
  border-radius: 8px;
}
