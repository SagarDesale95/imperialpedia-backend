#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request


BASE_URL = os.getenv("BASE_API_URL", "http://127.0.0.1:8000").rstrip("/")


def req(method: str, path: str, body: dict | None = None) -> tuple[int, dict]:
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    data = None if body is None else json.dumps(body).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30) as resp:
            payload = resp.read().decode("utf-8")
            return resp.status, json.loads(payload) if payload else {}
    except urllib.error.HTTPError as e:
        payload = e.read().decode("utf-8")
        try:
            body_json = json.loads(payload) if payload else {}
        except Exception:
            body_json = {"raw": payload}
        return e.code, body_json


def assert_200(step: str, status: int, payload: dict) -> None:
    if status != 200:
        raise RuntimeError(f"{step} failed: {status} -> {payload}")
    print(f"{step}: 200")


def main() -> None:
    suffix = str(int(time.time()))
    cat_slug = f"deploy-cat-{suffix}"
    tag_slug = f"deploy-tag-{suffix}"
    article_slug = f"deploy-article-{suffix}"
    glossary_slug = f"deploy-glossary-{suffix}"

    status, payload = req("GET", "/api/categories")
    assert_200("GET /api/categories", status, payload)

    status, payload = req(
        "POST",
        "/api/categories",
        {"name": "Deploy Category", "slug": cat_slug, "parent_id": None},
    )
    assert_200("POST /api/categories", status, payload)
    cat_id = payload["data"]["id"]

    status, payload = req("PUT", f"/api/categories/{cat_id}", {"name": "Deploy Category Updated", "slug": cat_slug})
    assert_200("PUT /api/categories/{id}", status, payload)

    status, payload = req("GET", "/api/tags")
    assert_200("GET /api/tags", status, payload)

    status, payload = req("POST", "/api/tags", {"name": "Deploy Tag", "slug": tag_slug})
    assert_200("POST /api/tags", status, payload)

    status, payload = req("GET", "/api/articles")
    assert_200("GET /api/articles", status, payload)

    article_body = {
        "title": "Deploy Article",
        "slug": article_slug,
        "content": "<p>Deploy test content.</p>",
        "category_id": cat_id,
        "tags": [tag_slug, "deploy"],
        "status": "published",
        "seo_title": "Deploy Article",
        "seo_description": "Deploy API test",
        "featured_image": None,
        "author_id": 1,
    }
    status, payload = req("POST", "/api/articles", article_body)
    assert_200("POST /api/articles", status, payload)
    article_id = payload["data"]["id"]

    status, payload = req("GET", f"/api/articles/{article_id}")
    assert_200("GET /api/articles/{id}", status, payload)

    status, payload = req(
        "PUT",
        f"/api/articles/{article_id}",
        {"title": "Deploy Article Updated", "slug": article_slug, "status": "review"},
    )
    assert_200("PUT /api/articles/{id}", status, payload)

    status, payload = req("GET", "/api/glossary")
    assert_200("GET /api/glossary", status, payload)

    status, payload = req(
        "POST",
        "/api/glossary",
        {
            "term": "Deploy Term",
            "definition": "Deploy definition.",
            "slug": glossary_slug,
            "related_terms": ["deploy-a", "deploy-b"],
        },
    )
    assert_200("POST /api/glossary", status, payload)
    glossary_id = payload["data"]["id"]

    status, payload = req("PUT", f"/api/glossary/{glossary_id}", {"definition": "Deploy definition updated."})
    assert_200("PUT /api/glossary/{id}", status, payload)

    status, payload = req("GET", "/api/seo/index-status")
    assert_200("GET /api/seo/index-status", status, payload)

    status, payload = req("GET", "/api/seo/sitemap")
    assert_200("GET /api/seo/sitemap", status, payload)

    status, payload = req("POST", "/api/ai/generate", {"prompt": "What is a stock in one sentence?"})
    assert_200("POST /api/ai/generate", status, payload)

    status, payload = req("DELETE", f"/api/articles/{article_id}")
    assert_200("DELETE /api/articles/{id}", status, payload)

    status, payload = req("DELETE", f"/api/glossary/{glossary_id}")
    assert_200("DELETE /api/glossary/{id}", status, payload)

    status, payload = req("DELETE", f"/api/categories/{cat_id}")
    assert_200("DELETE /api/categories/{id}", status, payload)

    # Post-delete verification
    status, payload = req("GET", f"/api/articles/{article_id}")
    if status != 404:
        raise RuntimeError(f"POST-DELETE verification failed for article: expected 404 got {status} -> {payload}")
    print("POST-DELETE verification: GET /api/articles/{id} => 404 OK")

    status, payload = req("GET", "/api/glossary")
    assert_200("GET /api/glossary (after delete)", status, payload)
    found_glossary = any(row.get("slug") == glossary_slug for row in payload.get("data", []))
    if found_glossary:
        raise RuntimeError("POST-DELETE verification failed: glossary slug still exists in list")
    print("POST-DELETE verification: glossary slug absent OK")

    status, payload = req("GET", "/api/categories")
    assert_200("GET /api/categories (after delete)", status, payload)
    found_category = any(row.get("slug") == cat_slug for row in payload.get("data", []))
    if found_category:
        raise RuntimeError("POST-DELETE verification failed: category slug still exists in list")
    print("POST-DELETE verification: category slug absent OK")

    print(f"All required endpoints returned 200 at {BASE_URL}")


if __name__ == "__main__":
    main()
