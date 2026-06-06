# Lingxing ERP — systemd 部署

## 文件清单

| 文件 | 作用 |
|---|---|
| `lingxing-erp.target` | 聚合 unit，启停入口 |
| `lingxing-erp.service` | FastAPI Dashboard（uvicorn，0.0.0.0:8000）|
| `lingxing-scheduler.service` | APScheduler 同步任务（领星 API 拉取、飞书日报）|
| `lingxing-erp.timer` | 兜底重启（每 10 分钟强拉 target）|

## 安装步骤

```bash
# 1) 创建系统用户(无登录权限)
sudo useradd -r -s /usr/sbin/nologin -d /opt/lingxing-erp lingxing

# 2) 部署代码
sudo mkdir -p /opt/lingxing-erp
sudo rsync -a --exclude='.venv' --exclude='__pycache__' \
    /path/to/source/  /opt/lingxing-erp/
sudo chown -R lingxing:lingxing /opt/lingxing-erp

# 3) 装依赖
cd /opt/lingxing-erp && poetry install --only=main
# 或
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# 4) 放 .env (权限 600)
sudo cp .env.example /opt/lingxing-erp/.env
sudo chmod 600 /opt/lingxing-erp/.env
sudo chown lingxing:lingxing /opt/lingxing-erp/.env

# 5) 跑 alembic 落库
sudo -u lingxing -E /opt/lingxing-erp/.venv/bin/alembic upgrade head

# 6) 安装 unit 文件
sudo cp deploy/systemd/*.service *.target *.timer /etc/systemd/system/
sudo systemctl daemon-reload

# 7) 开机自启 + 启动
sudo systemctl enable --now lingxing-erp.target
sudo systemctl enable --now lingxing-erp.timer
```

## 常用命令

```bash
# 看整体状态
sudo systemctl status lingxing-erp.target

# 看 dashboard 日志
sudo journalctl -u lingxing-erp.service -f

# 看 scheduler 日志
sudo journalctl -u lingxing-scheduler.service -f

# 重启某个组件
sudo systemctl restart lingxing-erp.service
sudo systemctl restart lingxing-scheduler.service

# 停整套
sudo systemctl stop lingxing-erp.target
```

## 路径假设

unit 文件里硬编码了：
- 代码目录 `/opt/lingxing-erp`
- venv 路径 `/opt/lingxing-erp/.venv`
- 配置文件 `/opt/lingxing-erp/.env`
- 系统用户 `lingxing`

如部署到非标准路径,需用 `sed -i 's|/opt/lingxing-erp|/your/path|g' *.service *.target *.timer` 替换。
