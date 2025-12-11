# Dolphain Interactive Portal

This is a browser-based portal for interacting with the Dolphain library and EARS data.

## How to Run

Because this application uses Pyodide (WebAssembly) and loads local files (the `.whl` package), it **must be served via a web server**. It will not work if you just open `index.html` directly in your browser due to security restrictions (CORS).

### Quick Start

1. Open a terminal in this directory:
   ```bash
   cd site/portal
   ```

2. Start a simple Python web server:
   ```bash
   python3 -m http.server 8000
   ```

3. Open your browser and go to:
   [http://localhost:8000](http://localhost:8000)

## Features

- **Zero Installation:** Runs entirely in the browser.
- **Interactive Python:** Write and run code to analyze data.
- **Live Visualization:** See waveforms and spectrograms generated on the fly.
- **Data Access:** Browses the GoMRI-17 dataset from HuggingFace.

## Troubleshooting

- **Loading stuck?** Check the browser console (F12) for errors.
- **Network Error?** Ensure you have an internet connection to download the Pyodide runtime and HuggingFace data.
