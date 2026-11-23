// main.ts — THE WORLD TODAY, Monday 23 November 2026.
// Copies the pre-rendered front page (entry.png) to /output/entry.png.
// Validates PNG magic + 1 MiB cap; honours MAKEFUN_OUTPUT_DIR.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const repoRoot = new URL(".", import.meta.url).pathname;
const src = join(repoRoot, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dst = join(outDir, "entry.png");

const buf = readFileSync(src);
if (buf.length === 0 || buf.length > 1048576) {
  throw new Error(`entry.png size ${buf.length} out of range (1..1048576)`);
}
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!buf.subarray(0, 8).equals(pngMagic)) {
  throw new Error("entry.png is not a PNG (bad magic bytes)");
}
// IHDR: width + height are big-endian uint32 at bytes 16 and 20.
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width === 0 || width > 1024 || height === 0 || height > 1024) {
  throw new Error(`entry.png dimensions ${width}x${height} out of range (max 1024x1024)`);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
console.log(`wrote ${dst} (${buf.length} bytes)`);
