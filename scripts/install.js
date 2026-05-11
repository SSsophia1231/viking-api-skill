#!/usr/bin/env node
/**
 * npm postinstall: copies the skill into ~/.claude/skills/viking-api/
 */
const fs = require("fs");
const path = require("path");
const os = require("os");

const skillName = "viking-api";
const src = path.resolve(__dirname, "..");
const dest = path.join(os.homedir(), ".claude", "skills", skillName);

function copyRecursive(srcPath, destPath) {
  const stat = fs.statSync(srcPath);
  if (stat.isDirectory()) {
    fs.mkdirSync(destPath, { recursive: true });
    for (const entry of fs.readdirSync(srcPath)) {
      copyRecursive(path.join(srcPath, entry), path.join(destPath, entry));
    }
  } else {
    fs.copyFileSync(srcPath, destPath);
  }
}

const SKIP = new Set(["node_modules", ".git"]);

try {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src)) {
    if (SKIP.has(entry)) continue;
    copyRecursive(path.join(src, entry), path.join(dest, entry));
  }
  console.log(`✓ viking-api skill installed to ${dest}`);
} catch (err) {
  console.error(`failed to install skill: ${err.message}`);
  process.exit(1);
}
