"""纯控制台测试：验证领星 API 签名 + Token + productList 调用。

不依赖 Redis / PostgreSQL，直接 httpx 调用，结果打印到控制台。
用法: .venv/Scripts/python.exe scripts/test_api.py
"""

import asyncio
import json
import os
import sys
import time

# 自动添加 src 到 sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import httpx

from lingxing.auth.sign import generate_sign

from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("LX_APP_ID", os.getenv("lx_app_id", ""))
APP_SECRET = os.getenv("LX_APP_SECRET", os.getenv("lx_app_secret", ""))
API_BASE = os.getenv("LX_API_BASE", os.getenv("lx_api_base", "https://openapi.lingxing.com"))

if not APP_ID or not APP_SECRET:
    print("错误: 请在 .env 中配置 lx_app_id 和 lx_app_secret")
    sys.exit(1)


async def fetch_token(client: httpx.AsyncClient) -> str:
    print("\n===== Step 1: 获取 access_token =====")
    form_data = {"appId": APP_ID, "appSecret": APP_SECRET}
    resp = await client.post("/api/auth-server/oauth/access-token", data=form_data)
    print(f"  状态码: {resp.status_code}")
    data = resp.json()
    print(f"  响应码: {data.get('code')}")
    print(f"  消息: {data.get('message', data.get('msg', ''))}")

    if str(data.get("code")) != "200":
        print(f"  完整响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        raise SystemExit("Token 获取失败")

    inner = data.get("data", {})
    token = inner.get("access_token", "")
    expires_in = inner.get("expires_in", 0)
    print(f"  access_token: {token[:20]}...{token[-8:]}  (共 {len(token)} 字符)")
    print(f"  expires_in: {expires_in}s")
    return token


async def fetch_product_list(client: httpx.AsyncClient, token: str) -> None:
    print("\n===== Step 2: 调用 productList =====")
    path = "/erp/sc/routing/data/local_inventory/productList"
    timestamp = int(time.time())

    body = {"offset": 0, "length": 10}

    sign_params = {
        "app_key": APP_ID,
        "access_token": token,
        "timestamp": timestamp,
        **body,
    }
    sign = generate_sign(sign_params, APP_ID)

    query_params = {
        "app_key": APP_ID,
        "access_token": token,
        "timestamp": timestamp,
        "sign": sign,
    }

    print(f"  请求路径: POST {path}")
    print(f"  query: app_key={APP_ID}, timestamp={timestamp}")
    print(f"  body: {json.dumps(body, ensure_ascii=False)}")
    print(f"  sign: {sign}")

    resp = await client.post(
        path,
        params=query_params,
        json=body,
        headers={"Content-Type": "application/json"},
    )
    print(f"  HTTP 状态码: {resp.status_code}")
    data = resp.json()
    print(f"  业务码: {data.get('code')}")
    print(f"  消息: {data.get('message', '')}")

    total = data.get("total", 0)
    products = data.get("data", [])
    print(f"  total: {total}")
    print(f"  本页条数: {len(products) if isinstance(products, list) else 'N/A'}")

    if isinstance(products, list) and products:
        print("\n  前 3 条产品数据:")
        for i, p in enumerate(products[:3]):
            print(
                f"    [{i}] id={p.get('id')}  sku={p.get('sku')}  "
                f"品名={p.get('product_name')}  状态={p.get('status_text')}  "
                f"采购成本={p.get('cg_price')}"
            )
    elif not isinstance(products, list):
        print(f"  data 类型异常: {type(products)}")
        print(f"  完整响应: {json.dumps(data, ensure_ascii=False, indent=2)[:2000]}")


async def main():
    print("=" * 60)
    print("领星 API 控制台测试")
    print(f"APP_ID: {APP_ID}")
    print(f"API_BASE: {API_BASE}")
    print("=" * 60)

    async with httpx.AsyncClient(base_url=API_BASE, timeout=30.0) as client:
        token = await fetch_token(client)
        await fetch_product_list(client, token)

    print("\n===== 测试完成 =====")


if __name__ == "__main__":
    asyncio.run(main())
