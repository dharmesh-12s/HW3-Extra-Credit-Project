# Handles loading and cleaning of the WikiPlots dataset.
# Addresses: missing values, encoding artifacts, title normalization, year extraction.

import re
import os

# Turning title to lowercase and remove whitespace for better BST key comparison
def normalize_title(title):
    return title.strip().lower()

# Extract a 4-digit year from the title string.
def extract_year(title):

    #Returns None if no year found or year is out of reasonable range.

    match = re.search(r'\((\d{4})\)', title)
    if match:
        year = int(match.group(1))
        if 1800 <= year <= 2030:
            return year
    return None

# Loading and pairing titles with their plot summaries from the WikiPlots dataset.
def load_dataset(titles_path, plots_path, limit=None):
   
    # Each story in the plots file is terminated by <EOS>.
    # This function returns a list of dicts with keys: title, normalized_title, plot, year
    
    stories = []

    # Load titles
    with open(titles_path, 'r', encoding='utf-8', errors='replace') as f:
        titles = [line.strip() for line in f.readlines()]

    # Load plots split by <EOS> marker
    with open(plots_path, 'r', encoding='utf-8', errors='replace') as f:
        raw = f.read()

    raw_plots = raw.split('<EOS>')

    # Pairing each title with its plot
    for i, title in enumerate(titles):
        if limit and i >= limit:
            break

        # Skiping entries with empty titles
        if not title:
            continue

        # Get matching plot, default to empty string if missing
        plot = raw_plots[i].strip() if i < len(raw_plots) else ""

        year = extract_year(title)

        stories.append({
            'title': title,
            'normalized_title': normalize_title(title),
            'plot': plot,
            'year': year
        })

    print(f"[Preprocessing] Loaded {len(stories)} stories.")
    return stories