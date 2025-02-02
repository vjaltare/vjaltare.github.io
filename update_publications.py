import os
import yaml
from scholarly import scholarly

# Google Scholar profile ID (Find in your Scholar profile URL)
SCHOLAR_ID = "nrbyKg0AAAAJ"

# Fetch author data from Google Scholar
author = scholarly.search_author_id(SCHOLAR_ID)
scholarly.fill(author, sections=["publications"])

# Ensure _publications directory exists
PUBLICATIONS_DIR = "_publications"
os.makedirs(PUBLICATIONS_DIR, exist_ok=True)

# List to store structured publication data
publication_data = []

for pub in author["publications"]:
    scholarly.fill(pub)  # Fetch publication details

    title = pub["bib"]["title"]
    date = pub["bib"].get("pub_year", "Unknown")
    venue = pub["bib"].get("venue", "Unknown Venue")
    paper_url = pub.get("pub_url", "")

    # Create filename-friendly slug
    slug = "-".join(title.lower().split()[:5])  # First 5 words

    # Generate the Markdown front matter
    md_content = f"""---
title: "{title}"
collection: publications
category: manuscripts
permalink: /publication/{slug}
date: {date}-01-01
venue: "{venue}"
paperurl: "{paper_url}"
---
"""

    # Write to a Markdown file
    md_filename = os.path.join(PUBLICATIONS_DIR, f"{slug}.md")
    with open(md_filename, "w", encoding="utf-8") as md_file:
        md_file.write(md_content)

    # Add entry to YAML data
    publication_data.append({
        "title": title,
        "date": date,
        "venue": venue,
        "url": f"/publication/{slug}"
    })

# Update `_data/publications.yml`
DATA_YAML_PATH = "_data/publications.yml"
with open(DATA_YAML_PATH, "w", encoding="utf-8") as yaml_file:
    yaml.dump(publication_data, yaml_file, default_flow_style=False, allow_unicode=True)

print("✅ Publications updated successfully!")
