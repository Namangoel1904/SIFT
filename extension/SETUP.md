# Extension Setup Guide

## Prerequisites

- Node.js 16+ and npm
- Chrome or Chromium-based browser

## Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Build the extension:**
   ```bash
   npm run build
   ```

3. **Load in Chrome:**
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top-right)
   - Click "Load unpacked"
   - Navigate to the `extension/dist` directory and select it

## Development

For development with hot reload:

```bash
npm run dev
```

Note: After making changes, you'll need to rebuild with `npm run build` and reload the extension in Chrome.

## Icons

Create icon files in the `icons/` directory:
- `icon16.png` (16x16)
- `icon48.png` (48x48)
- `icon128.png` (128x128)

See `icons/README.md` for more details.

## Troubleshooting

- **Extension doesn't load**: Check browser console and extension error page
- **API errors**: Ensure backend is running at `http://localhost:8000`
- **Build errors**: Run `npm install` again and check Node.js version

