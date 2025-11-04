# AI-CAD Compiler Web Demo

This is a single-page web application that demonstrates the AI-CAD Compiler running entirely in your browser.

## Features

- **Client-side execution**: Uses [Pyodide](https://pyodide.org) to run Python code directly in the browser
- **No server required**: All computation happens in your browser
- **Real-time compilation**: Enter a design intent and see the generated FeatureScript and CadQuery code instantly
- **Responsive design**: Works on desktop and mobile devices

## How It Works

1. The web app loads Pyodide, a Python runtime compiled to WebAssembly
2. It fetches the AI-CAD Compiler source code from GitHub
3. When you enter a design intent and click "Compile", it runs the compiler in your browser
4. The generated FeatureScript and CadQuery code are displayed in real-time

## Example Intents

- `L-bracket 60x40x3 mm, 2 holes M4 pitch 10`
- `Rectangular plate 100x50x5 mm, 4 corner holes M5`
- `Bracket 80x60x4 mm, single hole M6`

## Local Development

To test the web app locally:

```bash
cd docs
python -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Deployment

This web app is automatically deployed to GitHub Pages via GitHub Actions when changes are pushed to the main branch.

See `.github/workflows/deploy-pages.yml` for the deployment configuration.
