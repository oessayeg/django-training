#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup


def get_wikipedia_response(search_query):
    wikipedia_url = f"https://en.wikipedia.org/wiki/{search_query}"
    headers = {"User-Agent": "TestScript"}
    response = requests.get(wikipedia_url, headers=headers)
    if response.status_code != 200:
        raise Exception("It's a dead end!")
    return response


def parse_html_response(response):
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def get_next_article_search_query_from_html(html):
    content_div = html.find("div", {"id": "mw-content-text"})

    if not content_div:
        return None

    paragraphs = []
    for element in content_div.find_all(["p", "h2"], recursive=True):
        if element.name == "h2":
            break
        if element.name == "p":
            paragraphs.append(element)

    for p in paragraphs:
        for a_tag in p.find_all("a", href=True):
            href = a_tag.get("href")
            if href.startswith("/wiki/") and ":" not in href:
                return href.replace("/wiki/", "")

    return None


def get_next_search_query(search_query):
    response = get_wikipedia_response(search_query)
    parsed_html = parse_html_response(response)
    next_article_link = get_next_article_search_query_from_html(parsed_html)
    return next_article_link


def is_already_visited(search_query, already_visited_queries_set):
    return search_query in already_visited_queries_set


def print_road_to_philosophy(all_queries_list):
    for query in all_queries_list:
        print(query)
    print(
        f"{len(all_queries_list)} roads from {all_queries_list[0]} to {all_queries_list[len(all_queries_list) - 1]}"
    )


def roads_to_philosophy(search_query):
    visited_articles_set = {search_query}
    visited_articles_list = [search_query]
    next_search_query = get_next_search_query(search_query)

    while True:
        if next_search_query is None:
            print("It's a dead end!")
            break
        if next_search_query in visited_articles_set:
            print("It leads to an infinite loop!")
            break
        visited_articles_set.add(next_search_query)
        visited_articles_list.append(next_search_query)
        if next_search_query == "Philosophy":
            print_road_to_philosophy(visited_articles_list)
            break
        next_search_query = get_next_search_query(next_search_query)


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise Exception("Program takes one string for the wikipedia search")
        roads_to_philosophy(sys.argv[1])
    except Exception as e:
        print(e)
