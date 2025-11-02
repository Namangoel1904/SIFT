// Build script to copy all extension files to dist
import { copyFileSync, mkdirSync, readdirSync, statSync, existsSync } from 'fs';
import { resolve, join } from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

function copyRecursive(src, dest) {
  if (!existsSync(src)) {
    return;
  }
  const isDir = statSync(src).isDirectory();
  if (isDir) {
    mkdirSync(dest, { recursive: true });
    const entries = readdirSync(src);
    for (const entry of entries) {
      const srcPath = join(src, entry);
      const destPath = join(dest, entry);
      if (statSync(srcPath).isDirectory()) {
        copyRecursive(srcPath, destPath);
      } else {
        copyFileSync(srcPath, destPath);
      }
    }
  }
}

const distPath = resolve(__dirname, 'dist');

// Copy manifest
if (existsSync(resolve(__dirname, 'manifest.json'))) {
  copyFileSync(
    resolve(__dirname, 'manifest.json'),
    resolve(distPath, 'manifest.json')
  );
  console.log('✓ Copied manifest.json');
}

// Copy src directory
const srcPath = resolve(__dirname, 'src');
if (existsSync(srcPath) && statSync(srcPath).isDirectory()) {
  copyRecursive(srcPath, resolve(distPath, 'src'));
  console.log('✓ Copied src/ directory');
}

// Copy icons if they exist
const iconsPath = resolve(__dirname, 'icons');
if (existsSync(iconsPath) && statSync(iconsPath).isDirectory()) {
  copyRecursive(iconsPath, resolve(distPath, 'icons'));
  console.log('✓ Copied icons/ directory');
} else {
  console.log('⚠ Icons directory not found - extension will work but may show placeholder icons');
}

console.log('✓ Extension files copied to dist/');

