# MkDocs Material Theme Reference

Reusable theme for MkDocs Material documentation sites. Copy the files below into your project to apply the same design.

---

## Setup

### 1. Requirements

```txt
mkdocs>=1.5,<2.0
mkdocs-material>=9.5
mkdocstrings[python]>=0.24
pymdown-extensions>=10.0
```

### 2. mkdocs.yml Configuration

```yaml
site_name: YOUR_PROJECT_NAME
site_description: "Your project description"
site_author: "Your Name"
site_url: https://your-username.github.io/YOUR_PROJECT_NAME/
repo_url: https://github.com/your-username/YOUR_PROJECT_NAME
repo_name: your-username/YOUR_PROJECT_NAME

docs_dir: docs

theme:
  name: material
  logo: assets/logo.png
  favicon: assets/logo.png
  font:
    text: Outfit
    code: JetBrains Mono
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: deep purple
      accent: amber
      toggle:
        icon: material/weather-sunny
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: deep purple
      accent: amber
      toggle:
        icon: material/weather-night
        name: Switch to light mode
  icon:
    repo: fontawesome/brands/github
    admonition:
      note: fontawesome/solid/note-sticky
  features:
    - content.tabs.link
    - navigation.tabs
    - navigation.tabs.sticky
    - navigation.sections
    - navigation.top
    - navigation.instant
    - navigation.tracking
    - navigation.footer
    - search.highlight
    - search.suggest
    - content.code.copy
    - content.code.annotate
    - toc.follow
    - header.autohide

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: google
            show_source: true
            show_root_heading: true
            members_order: source
            heading_level: 3
            separate_signature: true
            merge_init_into_class: true
            show_signature_annotations: true

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - tables
  - attr_list
  - md_in_html
  - def_list
  - toc:
      permalink: true

extra_css:
  - stylesheets/extra.css

extra_javascript:
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js

extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/your-username/YOUR_PROJECT_NAME

nav:
  - Home:
      - Overview: index.md
      # Add your pages here
```

---

### 3. Custom CSS (`docs/stylesheets/extra.css`)

```css
/* ==========================================================================
   MkDocs Material — Custom Theme
   Aesthetic: Precision Laboratory
   Fonts: Syne (headings) + Outfit (body) + JetBrains Mono (code)
   Colors: Violet primary + amber accent, with prismatic gradient effects
   ========================================================================== */

/* ===== 1. Fonts ===== */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&display=swap');

/* ===== 2. Color System ===== */
:root {
  --e2e-violet-50: #f5f3ff;
  --e2e-violet-100: #ede9fe;
  --e2e-violet-200: #ddd6fe;
  --e2e-violet-400: #a78bfa;
  --e2e-violet-500: #8b5cf6;
  --e2e-violet-600: #7c3aed;
  --e2e-violet-700: #6d28d9;
  --e2e-violet-800: #5b21b6;
  --e2e-violet-900: #4c1d95;

  --e2e-amber: #f59e0b;
  --e2e-blue: #3b82f6;
  --e2e-cyan: #06b6d4;
  --e2e-emerald: #10b981;
  --e2e-rose: #f43f5e;

  --e2e-card-bg: #ffffff;
  --e2e-card-border: rgba(109, 40, 217, 0.06);
  --e2e-card-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 6px 16px rgba(0, 0, 0, 0.03);
  --e2e-card-shadow-hover: 0 8px 24px rgba(109, 40, 217, 0.1), 0 2px 8px rgba(0, 0, 0, 0.04);
  --e2e-text: #1e1b4b;
  --e2e-text-muted: #64748b;
  --e2e-divider: rgba(109, 40, 217, 0.06);
  --e2e-prism: linear-gradient(
    90deg,
    #6d28d9,
    #3b82f6,
    #06b6d4,
    #10b981,
    #f59e0b,
    #f43f5e,
    #6d28d9
  );

  --md-primary-fg-color: #6d28d9;
  --md-primary-fg-color--light: #8b5cf6;
  --md-primary-fg-color--dark: #4c1d95;
  --md-accent-fg-color: #f59e0b;
}

[data-md-color-scheme="slate"] {
  --e2e-card-bg: rgba(255, 255, 255, 0.03);
  --e2e-card-border: rgba(139, 92, 246, 0.12);
  --e2e-card-shadow: 0 1px 3px rgba(0, 0, 0, 0.3),
    0 6px 16px rgba(0, 0, 0, 0.2);
  --e2e-card-shadow-hover: 0 8px 24px rgba(139, 92, 246, 0.2),
    0 2px 8px rgba(0, 0, 0, 0.3);
  --e2e-text: #e2e8f0;
  --e2e-text-muted: #94a3b8;
  --e2e-divider: rgba(139, 92, 246, 0.1);

  --md-primary-fg-color: #8b5cf6;
  --md-primary-fg-color--light: #a78bfa;
  --md-primary-fg-color--dark: #6d28d9;
  --md-accent-fg-color: #fbbf24;
}

/* ===== 3. Global Base ===== */
html {
  scroll-behavior: smooth;
}

.md-grid {
  max-width: 1200px;
}

::selection {
  background: var(--e2e-violet-200);
  color: var(--e2e-violet-900);
}

[data-md-color-scheme="slate"] ::selection {
  background: var(--e2e-violet-800);
  color: var(--e2e-violet-100);
}

/* ===== 4. Typography ===== */
.md-typeset h1 {
  font-family: "Syne", var(--md-text-font-family), sans-serif;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.1;
}

.md-typeset h2 {
  font-family: "Syne", var(--md-text-font-family), sans-serif;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-top: 2.5rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid var(--e2e-divider);
}

.md-typeset h3 {
  font-family: "Syne", var(--md-text-font-family), sans-serif;
  font-weight: 600;
  letter-spacing: -0.01em;
  margin-top: 1.8rem;
}

.md-typeset h2 code,
.md-typeset h3 code {
  background: transparent;
  color: inherit;
  font-size: 0.9em;
  padding: 0;
}

/* ===== 5. Hero Section ===== */
.e2e-hero {
  position: relative;
  padding: 4.5rem 2.5rem 3.5rem;
  margin: -0.4rem -0.8rem 2.5rem;
  border-radius: 16px;
  background: var(--e2e-violet-50);
  overflow: hidden;
  text-align: center;
  animation: fade-up 0.6s ease-out both;
}

/* Prismatic gradient overlay */
.e2e-hero::before {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(
      ellipse 600px 400px at 15% 40%,
      rgba(109, 40, 217, 0.12) 0%,
      transparent 70%
    ),
    radial-gradient(
      ellipse 500px 350px at 85% 30%,
      rgba(59, 130, 246, 0.1) 0%,
      transparent 70%
    ),
    radial-gradient(
      ellipse 400px 300px at 50% 90%,
      rgba(245, 158, 11, 0.06) 0%,
      transparent 70%
    );
  pointer-events: none;
}

/* Dot grid pattern */
.e2e-hero::after {
  content: "";
  position: absolute;
  inset: 0;
  background-image: radial-gradient(
    rgba(109, 40, 217, 0.07) 1px,
    transparent 1px
  );
  background-size: 24px 24px;
  pointer-events: none;
}

[data-md-color-scheme="slate"] .e2e-hero {
  background: #13111c;
}

[data-md-color-scheme="slate"] .e2e-hero::before {
  background: radial-gradient(
      ellipse 600px 400px at 15% 40%,
      rgba(109, 40, 217, 0.25) 0%,
      transparent 70%
    ),
    radial-gradient(
      ellipse 500px 350px at 85% 30%,
      rgba(59, 130, 246, 0.15) 0%,
      transparent 70%
    ),
    radial-gradient(
      ellipse 400px 300px at 50% 90%,
      rgba(245, 158, 11, 0.08) 0%,
      transparent 70%
    );
}

[data-md-color-scheme="slate"] .e2e-hero::after {
  background-image: radial-gradient(
    rgba(139, 92, 246, 0.08) 1px,
    transparent 1px
  );
}

/* Hero title — gradient text */
.e2e-hero h1 {
  font-size: 3.2rem !important;
  margin-bottom: 1rem !important;
  position: relative;
  background: linear-gradient(
    135deg,
    var(--e2e-violet-700) 0%,
    var(--e2e-blue) 50%,
    var(--e2e-violet-500) 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

[data-md-color-scheme="slate"] .e2e-hero h1 {
  background: linear-gradient(
    135deg,
    var(--e2e-violet-400) 0%,
    #60a5fa 50%,
    var(--e2e-violet-200) 100%
  );
  -webkit-background-clip: text;
  background-clip: text;
}

.e2e-hero > p {
  position: relative;
  max-width: 640px;
  margin: 0 auto 2rem !important;
  font-size: 1.1rem;
  line-height: 1.7;
  color: var(--e2e-text-muted);
}

.e2e-hero .md-button {
  position: relative;
  margin: 0.3rem;
  border-radius: 8px;
  font-weight: 600;
  letter-spacing: 0.01em;
  padding: 0.7rem 1.6rem;
  transition: all 0.25s;
}

.e2e-hero .md-button--primary {
  background: var(--md-primary-fg-color);
  border-color: var(--md-primary-fg-color);
  color: #fff;
  box-shadow: 0 2px 8px rgba(109, 40, 217, 0.25);
}

.e2e-hero .md-button--primary:hover {
  background: var(--e2e-violet-800);
  border-color: var(--e2e-violet-800);
  box-shadow: 0 4px 16px rgba(109, 40, 217, 0.35);
  transform: translateY(-1px);
}

.e2e-hero .md-button:not(.md-button--primary):hover {
  transform: translateY(-1px);
  border-color: var(--md-primary-fg-color);
  color: var(--md-primary-fg-color);
}

/* Badge / label */
.e2e-badge {
  display: inline-block;
  position: relative;
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--md-primary-fg-color);
  background: var(--e2e-violet-100);
  padding: 0.35rem 1rem;
  border-radius: 100px;
  margin-bottom: 1.5rem;
}

[data-md-color-scheme="slate"] .e2e-badge {
  background: rgba(139, 92, 246, 0.15);
  color: var(--e2e-violet-400);
}

/* ===== 6. Pipeline Visualization ===== */
/* A horizontal flowchart: Node -> Connector -> Node -> ...           */
/* Use e2e-pipeline__node--primary for highlighted stages.            */
/* Connectors have an animated prismatic (rainbow) gradient.          */

.e2e-pipeline {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  padding: 1.5rem 0;
  margin: 1.5rem 0;
  flex-wrap: nowrap;
  animation: fade-up 0.5s ease-out 0.15s both;
}

.e2e-pipeline__node {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.55rem 1.1rem;
  border-radius: 8px;
  font-family: "JetBrains Mono", var(--md-code-font-family), monospace;
  font-size: 0.78rem;
  font-weight: 500;
  background: var(--e2e-card-bg);
  border: 1px solid var(--e2e-card-border);
  color: var(--e2e-text-muted);
  white-space: nowrap;
  transition: all 0.3s;
}

.e2e-pipeline__node:hover {
  border-color: var(--md-primary-fg-color--light);
  box-shadow: 0 2px 8px rgba(109, 40, 217, 0.08);
}

.e2e-pipeline__node--primary {
  background: var(--md-primary-fg-color);
  border-color: var(--md-primary-fg-color);
  color: #ffffff;
  font-weight: 600;
}

.e2e-pipeline__node--primary:hover {
  background: var(--e2e-violet-800);
  border-color: var(--e2e-violet-800);
  box-shadow: 0 2px 12px rgba(109, 40, 217, 0.2) !important;
}

[data-md-color-scheme="slate"] .e2e-pipeline__node--primary {
  background: var(--e2e-violet-700);
  border-color: var(--e2e-violet-600);
}

.e2e-pipeline__connector {
  width: 2.5rem;
  height: 2px;
  background: var(--e2e-prism);
  background-size: 300% 100%;
  position: relative;
  flex-shrink: 0;
  animation: prism-flow 4s linear infinite;
}

.e2e-pipeline__connector::after {
  content: "";
  position: absolute;
  right: -1px;
  top: 50%;
  transform: translateY(-50%) rotate(45deg);
  width: 5px;
  height: 5px;
  border-right: 2px solid var(--md-primary-fg-color);
  border-top: 2px solid var(--md-primary-fg-color);
}

/* ===== 7. Feature Cards ===== */
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(14.5rem, 1fr));
  gap: 1.2rem;
  margin: 2rem 0;
}

.feature-card {
  position: relative;
  border: 1px solid var(--e2e-card-border);
  border-radius: 12px;
  padding: 1.5rem 1.6rem 1.3rem;
  background: var(--e2e-card-bg);
  box-shadow: var(--e2e-card-shadow);
  transition: box-shadow 0.35s, border-color 0.35s, transform 0.35s;
  overflow: hidden;
}

/* Prismatic top bar on hover */
.feature-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--e2e-prism);
  background-size: 300% 100%;
  opacity: 0;
  transition: opacity 0.4s;
}

.feature-card:hover {
  border-color: var(--md-primary-fg-color--light);
  box-shadow: var(--e2e-card-shadow-hover);
  transform: translateY(-3px);
}

.feature-card:hover::before {
  opacity: 1;
  animation: prism-flow 3s linear infinite;
}

.feature-card h3 {
  margin-top: 0 !important;
  padding-bottom: 0 !important;
  border-bottom: none !important;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--e2e-text);
}

.feature-card h3 a {
  color: var(--md-primary-fg-color);
  text-decoration: none;
  transition: color 0.2s;
}

.feature-card h3 a:hover {
  color: var(--e2e-violet-500);
}

.feature-card p {
  font-size: 0.85rem;
  line-height: 1.65;
  color: var(--e2e-text-muted);
  margin-bottom: 0;
}

/* Staggered card animation */
.feature-card {
  animation: fade-up 0.5s ease-out both;
}

.feature-card:nth-child(1) {
  animation-delay: 0.1s;
}
.feature-card:nth-child(2) {
  animation-delay: 0.2s;
}
.feature-card:nth-child(3) {
  animation-delay: 0.3s;
}
.feature-card:nth-child(4) {
  animation-delay: 0.35s;
}

/* ===== 8. Code Blocks ===== */
.md-typeset pre > code {
  border-radius: 10px;
}

.md-typeset code {
  border-radius: 4px;
  font-size: 0.82em;
}

/* ===== 9. Navigation & Header ===== */
.md-header {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}

.md-tabs {
  box-shadow: 0 1px 0 var(--e2e-divider);
}

.md-tabs__link {
  font-weight: 500;
  letter-spacing: 0.01em;
  font-size: 0.82rem;
}

.md-nav__link {
  font-size: 0.85rem;
}

.md-nav__item--active > .md-nav__link {
  font-weight: 600;
  color: var(--md-primary-fg-color);
}

/* ===== 10. Tables ===== */
.md-typeset table:not([class]) {
  border-radius: 10px;
  overflow: hidden;
  box-shadow: var(--e2e-card-shadow);
  border: 1px solid var(--e2e-card-border);
}

.md-typeset table:not([class]) th {
  background: var(--md-primary-fg-color);
  color: #ffffff;
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.72rem;
  letter-spacing: 0.06em;
  padding: 0.85rem 1.1rem;
}

.md-typeset table:not([class]) td {
  padding: 0.7rem 1.1rem;
  border-bottom: 1px solid var(--e2e-divider);
  font-size: 0.88rem;
}

.md-typeset table:not([class]) tr:last-child td {
  border-bottom: none;
}

.md-typeset table:not([class]) tbody tr {
  transition: background 0.2s;
}

.md-typeset table:not([class]) tbody tr:hover {
  background: var(--e2e-violet-50);
}

[data-md-color-scheme="slate"] .md-typeset table:not([class]) tbody tr:hover {
  background: rgba(139, 92, 246, 0.05);
}

/* ===== 11. Admonitions ===== */
.md-typeset .admonition,
.md-typeset details {
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
  border-left-width: 4px;
}

.md-typeset .admonition-title,
.md-typeset summary {
  font-weight: 600;
  letter-spacing: 0.01em;
}

/* ===== 12. API Documentation (mkdocstrings) ===== */
.doc-heading {
  border-top: 2px solid var(--e2e-divider);
  padding-top: 1rem;
  margin-top: 2rem;
}

.doc-signature {
  font-size: 0.85em;
  background: var(--md-code-bg-color);
  padding: 0.6em 0.9em;
  border-radius: 8px;
  border-left: 3px solid var(--e2e-amber);
}

.doc-param-details {
  margin-left: 1rem;
  font-size: 0.92em;
}

.doc-label {
  font-size: 0.65em;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 0.2em 0.55em;
  border-radius: 4px;
  background: var(--md-primary-fg-color);
  color: #ffffff;
  vertical-align: middle;
}

.doc-children .doc-heading {
  margin-top: 1.2rem;
  padding-top: 0.6rem;
  border-top: 1px solid var(--e2e-divider);
}

.doc-source summary {
  font-size: 0.8em;
  color: var(--e2e-text-muted);
}

/* ===== 13. Footer ===== */
.md-footer {
  margin-top: 3rem;
}

/* ===== 14. Content Spacing ===== */
.md-typeset hr {
  border-color: var(--e2e-divider);
  margin: 2.5rem 0;
}

/* Plain code blocks (e.g. directory trees) */
.md-typeset pre:has(code:not([class])) {
  background: var(--md-code-bg-color);
  border-radius: 10px;
  border: 1px solid var(--e2e-divider);
}

/* ===== 15. Scrollbar ===== */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: var(--e2e-violet-200);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--e2e-violet-400);
}

[data-md-color-scheme="slate"] ::-webkit-scrollbar-thumb {
  background: rgba(139, 92, 246, 0.2);
}

[data-md-color-scheme="slate"] ::-webkit-scrollbar-thumb:hover {
  background: rgba(139, 92, 246, 0.4);
}

/* ===== 16. Animations ===== */
@keyframes fade-up {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes prism-flow {
  0% {
    background-position: 0% 0;
  }
  100% {
    background-position: 300% 0;
  }
}

.e2e-pipeline {
  animation: fade-up 0.5s ease-out 0.15s both;
}

/* ===== 17. Responsive ===== */
@media (max-width: 768px) {
  .e2e-hero {
    padding: 3rem 1.5rem 2.5rem;
    margin: -0.4rem -0.4rem 2rem;
  }

  .e2e-hero h1 {
    font-size: 2.2rem !important;
  }

  .e2e-hero > p {
    font-size: 0.95rem;
  }

  .e2e-pipeline {
    flex-direction: column;
    gap: 0;
    flex-wrap: wrap;
  }

  .e2e-pipeline__connector {
    width: 2px;
    height: 1.5rem;
    background: var(--e2e-prism);
    background-size: 100% 300%;
    animation: prism-flow-v 4s linear infinite;
  }

  .e2e-pipeline__connector::after {
    right: 50%;
    top: auto;
    bottom: -1px;
    transform: translateX(50%) rotate(135deg);
  }

  .feature-grid {
    grid-template-columns: 1fr;
  }
}

@keyframes prism-flow-v {
  0% {
    background-position: 0 0%;
  }
  100% {
    background-position: 0 300%;
  }
}
```

---

### 4. Landing Page Template (`docs/index.md`)

Replace the placeholder text with your project-specific content. The HTML classes are styled by the CSS above.

````markdown
<section class="e2e-hero" markdown>

<span class="e2e-badge">Your Badge Text</span>

# Your Project Name

**Your one-line description** — a longer sentence expanding on what the project does and why it matters.

[Get Started](quickstart.md){ .md-button .md-button--primary }
[API Reference](api/index.md){ .md-button }

</section>

<!-- Pipeline visualization (optional) — customize node labels -->
<div class="e2e-pipeline">
  <div class="e2e-pipeline__node">Input</div>
  <div class="e2e-pipeline__connector"></div>
  <div class="e2e-pipeline__node e2e-pipeline__node--primary">Module A</div>
  <div class="e2e-pipeline__connector"></div>
  <div class="e2e-pipeline__node e2e-pipeline__node--primary">Module B</div>
  <div class="e2e-pipeline__connector"></div>
  <div class="e2e-pipeline__node e2e-pipeline__node--primary">Module C</div>
  <div class="e2e-pipeline__connector"></div>
  <div class="e2e-pipeline__node">Output</div>
</div>

---

<div class="feature-grid" markdown>
<div class="feature-card" markdown>
### Feature One
Description of the first key feature of your project.
</div>
<div class="feature-card" markdown>
### Feature Two
Description of the second key feature of your project.
</div>
<div class="feature-card" markdown>
### Feature Three
Description of the third key feature of your project.
</div>
</div>

---

## Quick Install

```bash
pip install your-package
```

## Get Started

<div class="feature-grid" markdown>
<div class="feature-card" markdown>
### [Installation](installation.md)
How to install and configure the project
</div>
<div class="feature-card" markdown>
### [Quickstart](quickstart.md)
A minimal working example to get started
</div>
<div class="feature-card" markdown>
### [API Reference](api/index.md)
Complete class and function documentation
</div>
<div class="feature-card" markdown>
### [Examples](examples.md)
Tutorials and worked examples
</div>
</div>
````

---

## Design System Reference

### Fonts
| Role     | Font           | Weights   | Source       |
|----------|----------------|-----------|--------------|
| Headings | Syne           | 600-800   | CSS @import  |
| Body     | Outfit         | 300-600   | mkdocs.yml   |
| Code     | JetBrains Mono | 400       | mkdocs.yml   |

### Color Palette

| Token                | Light Mode   | Dark Mode              |
|----------------------|--------------|------------------------|
| Primary              | `#6d28d9`    | `#8b5cf6`              |
| Primary Light        | `#8b5cf6`    | `#a78bfa`              |
| Primary Dark         | `#4c1d95`    | `#6d28d9`              |
| Accent               | `#f59e0b`    | `#fbbf24`              |
| Card Background      | `#ffffff`    | `rgba(255,255,255,0.03)` |
| Card Border          | `rgba(109,40,217,0.06)` | `rgba(139,92,246,0.12)` |
| Text                 | `#1e1b4b`    | `#e2e8f0`              |
| Text Muted           | `#64748b`    | `#94a3b8`              |
| Divider              | `rgba(109,40,217,0.06)` | `rgba(139,92,246,0.1)` |

### Key CSS Classes

| Class                          | Usage                                           |
|--------------------------------|-------------------------------------------------|
| `.e2e-hero`                    | Hero section wrapper (`<section>` with `markdown`) |
| `.e2e-badge`                   | Small uppercase label inside the hero            |
| `.e2e-pipeline`                | Horizontal flowchart container                   |
| `.e2e-pipeline__node`          | Pipeline stage (default style)                   |
| `.e2e-pipeline__node--primary` | Highlighted pipeline stage                       |
| `.e2e-pipeline__connector`     | Animated prismatic arrow between nodes           |
| `.feature-grid`                | CSS grid container for cards                     |
| `.feature-card`                | Individual card with hover effects               |

### Key Visual Effects

- **Prismatic gradient** (`--e2e-prism`): A rainbow gradient animating via `prism-flow` keyframes. Used on card hover borders and pipeline connectors.
- **Hero background**: Three overlapping radial gradients (violet, blue, amber) + a dot-grid pattern via `::after`.
- **Gradient text**: Hero `h1` uses `background-clip: text` with a violet-blue gradient.
- **Fade-up animation**: Elements animate in from 16px below with opacity transition on page load.
- **Staggered cards**: Feature cards use incremental `animation-delay` (0.1s, 0.2s, 0.3s, 0.35s).

### Required MkDocs Extensions

These extensions must be in `mkdocs.yml` for the HTML/markdown patterns to work:

- `attr_list` — enables `{ .md-button .md-button--primary }` syntax
- `md_in_html` — enables `markdown` attribute on HTML elements like `<section>`, `<div>`
