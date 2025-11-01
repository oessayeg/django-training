#!/usr/bin/env python3

import sys
import requests
import dewiki


def fetch_wikitext(title: str, lang: str):
    endpoint = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": title,
        "prop": "wikitext",
        "redirects": 1,
        "format": "json",
    }
    headers = {"User-Agent": "WikipediaSearch/1.0"}

    try:
        request = requests.get(endpoint, params=params, headers=headers, timeout=10)
        if request.status_code != 200:
            return None
        data = request.json()
        wikitext = data.get("parse", {}).get("wikitext", {}).get("*")
        return wikitext
    except Exception:
        return None


def write_to_file(file_name, result):
    with open(file_name, "w") as f:
        f.write(result)


def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError(
                "Parameter error: exactly one quoted search string is required."
            )
        search_query = sys.argv[1]
        wiki_text = fetch_wikitext(search_query, "en")
        if not wiki_text:
            raise ValueError("No result found on Wikipedia (EN) for the given request.")
        result = dewiki.from_string(wiki_text)
        write_to_file(search_query + ".wiki", result)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()