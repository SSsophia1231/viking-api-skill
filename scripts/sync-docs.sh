#!/bin/bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
ARCOSITE_DIR="/Users/bytedance/Documents/产品文档-Arcosite"
TMP_DIR="/tmp/viking-docs-latest"
LOG="$SKILL_DIR/scripts/sync.log"
PYTHON="/Users/bytedance/.venv314/bin/python3"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"; }

log "=== sync start ==="

# 加载 AK/SK
source "$ARCOSITE_DIR/envs.sh"

# 下载最新文档
log "downloading docs from Arcosite..."
rm -rf "$TMP_DIR"
"$PYTHON" "$ARCOSITE_DIR/arcosite.py" download \
  --out-dir "$TMP_DIR" \
  --include-path "Viking 知识库/API参考"

# 同步到 resources/，只取 API参考 子目录内容，跳过 version/meta.json
log "syncing to resources/..."
rsync -av --delete "$TMP_DIR/Viking 知识库/API参考/" "$SKILL_DIR/resources/" \
  --exclude='.arcosite_meta.json' \
  --exclude='version' \
  --exclude='meta.json' \
  --exclude='飞书/' \
  --exclude='文档解析/' \
  --exclude='文档/文档处理报错处理手册.md'

# 脱敏：替换文档中的示例 AK 值，避免触发 GitHub secret scanning
find "$SKILL_DIR/resources" -name "*.md" -exec sed -i '' 's/AK[A-Z][A-Za-z0-9+\/=]\{20,\}/AK****/g' {} +

# 检查是否有变化（包括新增的未追踪文件）
cd "$SKILL_DIR"
if [ -z "$(git status --porcelain resources/)" ]; then
  log "no changes detected, skipping release"
  exit 0
fi

log "changes detected, building release..."

# 生成新 version 和 meta.json
VERSION=$(date +%Y-%m-%d)
"$PYTHON" "$SKILL_DIR/scripts/build_release.py" "$VERSION"

# commit + push
git add resources/
git commit -m "sync: update API docs $VERSION"
git push
log "pushed to GitHub"

# npm publish
npm version patch --no-git-tag-version
npm publish
log "published to npm"

log "=== sync done ==="
