---
title: Preview documentation changes locally
---

## Strategy 1: Run MyST web server

1. Navigate to the `docs` directory and run
   ```bash
   myst start
   ```
2. Connect to the specific URL in your web browser.

3. Make changes to the documentation while previewing the HTML.

## Strategy 2: Build HTML

1. Navigate to the `docs` directory and run
   ```bash
   myst build
   ```
2. Open the content in the `_build` directory in your browser.
