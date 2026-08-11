"""
Program Name: Lab17_mshyjuphilip-2.py
Author: Mervyn S. Philip
Purpose: Uses the GitHub API to find the most-starred Java repositories
         and visualizes them as an interactive plotly bar chart, with
         hover text showing each project's owner and description.
Starter Code: Adapted from python_repos_visual.py (Python Crash Course,
              Chapter 17), modified to query GitHub for Java repositories
              instead of Python and to customize the chart's appearance.
Date: 2026-08-10
"""

import requests
import plotly.express as ex
from plotly.graph_objects import Bar, Figure


def extract_repo_info(repo_dict):
    """Extract relevant information from a GitHub repo dict."""
    name = repo_dict.get("name", "Unknown")
    stars = repo_dict.get("stargazers_count", 0)
    owner = repo_dict.get("owner", {}).get("login", "Unknown")
    url = repo_dict.get("html_url", "")
    description = repo_dict.get("description") or "No description provided"
    return name, stars, owner, url, description


def build_hover_text(owner, description):
    """Build a single hover-text label combining owner and description."""
    return f"{owner}<br>{description}"


def fetch_top_repos(language, per_page = 10):
    """Fetch the top repositories for a given programming language from GitHub.
    
    Args:
        language (str): The programming language to search for.
        per_page (int): The number of repositories to fetch (max 100).
    """
    url = (
        "https://api.github.com/search/repositories"
        f"?q=language:{language}&sort=stars&order=desc&per_page={per_page}"
    )
    headers = {"Accept": "application/vnd.github.v3+json"}

    try:
        response = requests.get(url, headers = headers, timeout = 10)
        response.raise_for_status()
        response_dict = response.json()
    except (requests.exceptions.RequestException, ValueError) as error:
        print(f"Error fetching data from GitHub API: {error}")
        return []

    print(f"Status code: {response.status_code}")
    return response_dict.get("items", [])


def save_chart(figure, output_path):
    """Save a plotly Figure to an interactive HTML file."""
    figure.write_html(output_path)


def create_repos_chart(names, stars, hover_texts, links, title):
    """Create a plotly bar chart for the given repository data.
    Args:
        names (list of str): Repository names.
        stars (list of int): Star counts for each repository.
        hover_texts (list of str): Hover text for each bar.
        links (list of str): GitHub URLs for each repository.
        title (str): Title for the chart."""
    data = [
        Bar(
            x = names,
            y = stars,
            text = hover_texts,
            hovertext = hover_texts,
            marker = dict(
                color = stars,
                colorscale = ex.colors.sequential.Viridis,
                colorbar = dict(title = "Stars"),
            ),
        )
    ]

    layout = dict(
        title=title,
        xaxis=dict(title = "Repository", tickangle = -40),
        yaxis=dict(title = "Stars"),
    )

    figure = Figure(data = data, layout = layout)

    # Attach each repo's GitHub URL as custom data so it travels with
    # the figure; plotly HTML output keeps this accessible via hover.
    figure.update_traces(customdata = links)

    return figure


def main():
    """Wire together fetching, transforming, and charting Java repos."""
    language = "java"
    repo_count = 10
    output_html_path = "java_repos.html"
    chart_title = "Most-Starred Java Projects on GitHub"

    repo_dicts = fetch_top_repos(language, per_page = repo_count)

    names, stars, hover_texts, links = [], [], [], []
    for repo_dict in repo_dicts:
        name, star_count, owner, url, description = extract_repo_info(repo_dict)
        names.append(name)
        stars.append(star_count)
        hover_texts.append(build_hover_text(owner, description))
        links.append(url)

    chart = create_repos_chart(names, stars, hover_texts, links, chart_title)
    save_chart(chart, output_html_path)


if __name__ == "__main__":
    main()