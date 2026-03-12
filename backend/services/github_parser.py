import requests
from typing import Dict, List
from collections import Counter
from config import settings


class GithubParser:
    """
    GitHub portfolio analyzer.

    Extracts:
    - repository metadata
    - languages used
    - project quality indicators
    - portfolio score
    """

    def __init__(self):

        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        
        if settings.GITHUB_TOKEN:
            # Use Bearer schema as it works for both Classic and Fine-Grained PATs
            token_prefix = "Bearer" if settings.GITHUB_TOKEN.startswith("github_pat_") else "token"
            self.headers["Authorization"] = f"{token_prefix} {settings.GITHUB_TOKEN}"

    # ---------------------------------------------------
    # Extract username from GitHub URL
    # ---------------------------------------------------

    def extract_username(self, github_url: str) -> str:

        return github_url.rstrip("/").split("/")[-1]

    # ---------------------------------------------------
    # Fetch repositories
    # ---------------------------------------------------

    def fetch_repositories(self, username: str) -> List[Dict]:

        url = f"https://api.github.com/users/{username}/repos"

        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print(f"GitHub API Error for {username}: {response.status_code} {response.text}")
            return []

        repos = response.json()

        repo_data = []

        for repo in repos:

            repo_data.append({
                "name": repo["name"],
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "language": repo["language"],
                "description": repo["description"],
                "url": repo["html_url"],
                "updated_at": repo["updated_at"]
            })

        return repo_data

    # ---------------------------------------------------
    # Language analysis
    # ---------------------------------------------------

    def analyze_languages(self, repos: List[Dict]) -> List[str]:

        languages = []

        for repo in repos:

            if repo["language"]:
                languages.append(repo["language"])

        language_counts = Counter(languages)

        return [lang for lang, _ in language_counts.most_common(5)]

    # ---------------------------------------------------
    # Documentation quality
    # ---------------------------------------------------

    def estimate_documentation_score(self, repos: List[Dict]) -> float:

        documented = 0

        for repo in repos:

            description = repo["description"]

            if description and len(description) > 20:
                documented += 1

        if len(repos) == 0:
            return 0

        return documented / len(repos)

    # ---------------------------------------------------
    # Portfolio scoring
    # ---------------------------------------------------

    def compute_portfolio_score(self, repos: List[Dict]) -> float:

        if len(repos) == 0:
            return 0

        total_stars = sum(repo["stars"] for repo in repos)
        total_forks = sum(repo["forks"] for repo in repos)

        repo_count_score = min(len(repos) / 10, 1)

        star_score = min(total_stars / 50, 1)

        fork_score = min(total_forks / 20, 1)

        documentation_score = self.estimate_documentation_score(repos)

        final_score = (
            0.35 * repo_count_score +
            0.35 * star_score +
            0.15 * fork_score +
            0.15 * documentation_score
        )

        return round(final_score * 100, 2)

    # ---------------------------------------------------
    # Main analysis pipeline
    # ---------------------------------------------------

    def analyze(self, github_url: str) -> Dict:

        username = self.extract_username(github_url)

        repos = self.fetch_repositories(username)

        languages = self.analyze_languages(repos)

        total_stars = sum(repo["stars"] for repo in repos)

        total_forks = sum(repo["forks"] for repo in repos)

        documentation_score = self.estimate_documentation_score(repos)

        portfolio_score = self.compute_portfolio_score(repos)

        return {
            "username": username,
            "repo_count": len(repos),
            "total_stars": total_stars,
            "total_forks": total_forks,
            "top_languages": languages,
            "documentation_quality": documentation_score,
            "portfolio_score": portfolio_score,
            "repositories": repos[:5]   # top 5 repos
        }