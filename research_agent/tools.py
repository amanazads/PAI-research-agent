import os

import requests


def _tavily_results(endpoint: str, payload: dict) -> list:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError("Set TAVILY_API_KEY before running research.")

    try:
        response = requests.post(
            f"https://api.tavily.com/{endpoint}",
            headers={"Authorization": f"Bearer {api_key}"},
            json=payload,
            timeout=(5, 25),
        )
        response.raise_for_status()
        data = response.json()
    except requests.Timeout as error:
        raise RuntimeError("Tavily request timed out.") from error
    except requests.HTTPError as error:
        raise RuntimeError(f"Tavily returned HTTP {response.status_code}.") from error
    except requests.RequestException as error:
        raise RuntimeError("Tavily request failed or returned invalid JSON.") from error

    results = data.get("results") if isinstance(data, dict) else None
    if not isinstance(results, list):
        raise RuntimeError("Tavily returned a malformed results list.")

    return results


def search_web(query: str) -> list[dict[str, str]]:
    results = _tavily_results(
        "search",
        {"query": query, "search_depth": "basic", "max_results": 4},
    )

    hits = []
    for result in results:
        if not isinstance(result, dict):
            continue

        url = result.get("url")
        if not isinstance(url, str) or not url.startswith(("https://", "http://")):
            continue

        title = result.get("title")
        snippet = result.get("content")
        hits.append({
            "title": title if isinstance(title, str) and title.strip() else url,
            "url": url,
            "snippet": snippet[:600] if isinstance(snippet, str) else "",
        })

    return hits


def read_page(url: str) -> str:
    results = _tavily_results("extract", {"urls": [url]})

    for result in results:
        if isinstance(result, dict):
            text = result.get("raw_content")
            if isinstance(text, str) and text.strip():
                return text.strip()[:8_000]

    raise RuntimeError("No usable page text was returned.")