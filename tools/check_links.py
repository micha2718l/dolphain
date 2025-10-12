#!/usr/bin/env python3
"""
Simple link checker for the Dolphain site.
Tests local file links to ensure they exist.
"""

import os
import re
from pathlib import Path

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def check_local_links(html_file):
    """Check all local file links in an HTML file."""

    print(f"\n{BLUE}Checking links in: {html_file}{RESET}\n")

    site_dir = Path(html_file).parent

    with open(html_file, "r") as f:
        content = f.read()

    # Find all href attributes (excluding # anchors and external URLs)
    href_pattern = r'href=["\']((?!http|#|mailto)[^"\']+)["\']'
    links = re.findall(href_pattern, content)

    # Also check script and link tags
    src_pattern = r'(?:src|href)=["\']((?!http)[^"\']+\.(?:js|css))["\']'
    resource_links = re.findall(src_pattern, content)

    all_links = set(links + resource_links)

    issues = []
    successes = []

    for link in sorted(all_links):
        # Skip anchor links and external links
        if link.startswith("#") or link.startswith("http"):
            continue

        # Resolve the path relative to the HTML file's directory
        link_path = site_dir / link

        if link_path.exists():
            successes.append(link)
            print(f"{GREEN}✓{RESET} {link}")
        else:
            issues.append(link)
            print(f"{RED}✗{RESET} {link} {RED}(NOT FOUND){RESET}")

            # Try to suggest corrections
            filename = Path(link).name
            potential_files = list(site_dir.rglob(f"{filename.split('.')[0]}.*"))
            if potential_files:
                print(
                    f"  {YELLOW}  Found similar: {[str(f.relative_to(site_dir)) for f in potential_files]}{RESET}"
                )

    # Summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{GREEN}✓ {len(successes)} links OK{RESET}")
    if issues:
        print(f"{RED}✗ {len(issues)} links broken{RESET}")
        print(f"\n{RED}Broken links:{RESET}")
        for link in issues:
            print(f"  - {link}")
    else:
        print(f"{GREEN}All local links are valid!{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

    return len(issues) == 0


def check_all_html_files(directory):
    """Check all HTML files in a directory."""
    site_path = Path(directory)
    html_files = list(site_path.glob("*.html"))

    print(f"{BLUE}Found {len(html_files)} HTML files to check{RESET}")

    all_good = True
    for html_file in html_files:
        if not check_local_links(html_file):
            all_good = False

    return all_good


if __name__ == "__main__":
    import sys

    # Check if a specific file or directory is provided
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        # Default to site directory
        target = "site"

    target_path = Path(target)

    if target_path.is_file():
        success = check_local_links(target_path)
    elif target_path.is_dir():
        success = check_all_html_files(target_path)
    else:
        print(f"{RED}Error: {target} not found{RESET}")
        sys.exit(1)

    sys.exit(0 if success else 1)
