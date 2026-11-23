#!/usr/bin/env bash
# JingHui one-shot server setup for Ubuntu 22.04
# Run AFTER the deploy tarball has been extracted to /opt/jinghui
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive

echo "[1/6] apt install nginx + python3-venv ..."
apt-get update -y -qq
apt-get install -y -qq nginx python3-venv >/dev/null

echo "[2/6] ensure directories ..."
mkdir -p /opt/jinghui/server/static/generated
mkdir -p /opt/jinghui/web/dist

echo "[3/6] create python venv + install requirements ..."
cd /opt/jinghui/server
python3 -m venv .venv
.venv/bin/pip install --upgrade pip -q -i https://pypi.tuna.tsinghua.edu.cn/simple
.venv/bin/pip install -r requirements.txt -q -i https://pypi.tuna.tsinghua.edu.cn/simple

echo "[4/6] write production .env ..."
cat > /opt/jinghui/server/.env <<'ENVEOF'
AI_PROVIDER=demo
ENVEOF

echo "[5/6] install systemd service ..."
cp /opt/jinghui/deploy/jinghui.service /etc/systemd/system/jinghui.service
systemctl daemon-reload
systemctl enable jinghui >/dev/null
systemctl restart jinghui

echo "[6/6] install nginx site ..."
cp /opt/jinghui/deploy/nginx-jinghui.conf /etc/nginx/sites-available/jinghui
ln -sf /etc/nginx/sites-available/jinghui /etc/nginx/sites-enabled/jinghui
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

echo "=== SETUP DONE ==="
sleep 2
systemctl is-active jinghui && echo "backend: ACTIVE"
curl -s -m 5 http://127.0.0.1:8000/api/health || echo "backend health: FAILED"
curl -s -m 5 -o /dev/null -w "nginx front: %{http_code}\n" http://127.0.0.1/ || echo "nginx front: FAILED"
