#!/usr/bin/env python3
"""
GitHub Repository Search Tool
Search GitHub repositories using the GitHub API.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import ssl


def search_repositories(query: str, language: str = None, sort: str = "stars", 
                       order: str = "desc", per_page: int = 10) -> dict:
    """
    Search GitHub repositories.
    
    Args:
        query: Search query (e.g., "whatsapp bot automation")
        language: Filter by programming language (optional)
        sort: Sort by (stars, forks, updated)
        order: Order (asc, desc)
        per_page: Number of results (max 100)
    
    Returns:
        dict: Search results
    """
    base_url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": sort,
        "order": order,
        "per_page": min(per_page, 100)
    }
    
    if language:
        params["q"] += f"+language:{language}"
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/vnd.github.v3+json")
        
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {
                "success": True,
                "total_count": data.get("total_count", 0),
                "items": [
                    {
                        "full_name": repo.get("full_name"),
                        "description": repo.get("description"),
                        "stars": repo.get("stargazers_count"),
                        "forks": repo.get("forks_count"),
                        "language": repo.get("language"),
                        "updated_at": repo.get("updated_at"),
                        "html_url": repo.get("html_url"),
                        "open_issues": repo.get("open_issues_count"),
                        "license": repo.get("license", {}).get("name") if repo.get("license") else None,
                        "owner": {
                            "login": repo.get("owner", {}).get("login"),
                            "avatar_url": repo.get("owner", {}).get("avatar_url"),
                        }
                    }
                    for repo in data.get("items", [])
                ]
            }
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        return {
            "success": False,
            "error": f"HTTP {e.code}: {e.reason}",
            "details": error_body
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def get_repository_details(owner: str, repo: str) -> dict:
    """
    Get detailed information about a specific repository.
    
    Args:
        owner: Repository owner
        repo: Repository name
    
    Returns:
        dict: Repository details
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"
    
    try:
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/vnd.github.v3+json")
        
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {
                "success": True,
                "data": {
                    "full_name": data.get("full_name"),
                    "description": data.get("description"),
                    "html_url": data.get("html_url"),
                    "stars": data.get("stargazers_count"),
                    "forks": data.get("forks_count"),
                    "watchers": data.get("watchers_count"),
                    "language": data.get("language"),
                    "license": data.get("license", {}).get("name") if data.get("license") else None,
                    "created_at": data.get("created_at"),
                    "updated_at": data.get("updated_at"),
                    "pushed_at": data.get("pushed_at"),
                    "size": data.get("size"),
                    "open_issues": data.get("open_issues_count"),
                    "topics": data.get("topics", []),
                    "owner": {
                        "login": data.get("owner", {}).get("login"),
                        "avatar_url": data.get("owner", {}).get("avatar_url"),
                        "type": data.get("owner", {}).get("type"),
                    },
                    "permissions": data.get("permissions"),
                }
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def list_topics(owner: str, repo: str) -> dict:
    """
    List topics for a repository.
    
    Args:
        owner: Repository owner
        repo: Repository name
    
    Returns:
        dict: Topics list
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/topics"
    
    try:
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/vnd.github.v3+json")
        
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {
                "success": True,
                "names": data.get("names", [])
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description="GitHub Repository Search Tool")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search repositories")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--language", "-l", help="Programming language")
    search_parser.add_argument("--sort", "-s", default="stars", choices=["stars", "forks", "updated"])
    search_parser.add_argument("--order", "-o", default="desc", choices=["asc", "desc"])
    search_parser.add_argument("--per-page", "-p", type=int, default=10)
    
    # Details command
    details_parser = subparsers.add_parser("details", help="Get repository details")
    details_parser.add_argument("owner", help="Repository owner")
    details_parser.add_argument("repo", help="Repository name")
    
    # Topics command
    topics_parser = subparsers.add_parser("topics", help="List repository topics")
    topics_parser.add_argument("owner", help="Repository owner")
    topics_parser.add_argument("repo", help="Repository name")
    
    args = parser.parse_args()
    
    if args.command == "search":
        result = search_repositories(
            query=args.query,
            language=args.language,
            sort=args.sort,
            order=args.order,
            per_page=args.per_page
        )
    elif args.command == "details":
        result = get_repository_details(args.owner, args.repo)
    elif args.command == "topics":
        result = list_topics(args.owner, args.repo)
    else:
        parser.print_help()
        sys.exit(1)
    
    # Output as JSON
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
