# Streamlit frontend for the WikiPlots BST Search Engine.
# Creating an interactive web UI for searching, browsing, and exploring stories.

import os
import sys
import time
import streamlit as st

# Ensuring imports work from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.bst import BinarySearchTree
from src.story import Story
from src.preprocessing import load_dataset

# --- Dataset paths ---
DATA_DIR    = os.path.join(os.path.dirname(__file__), '..', 'data')
TITLES_PATH = os.path.join(DATA_DIR, 'titles')
PLOTS_PATH  = os.path.join(DATA_DIR, 'plots')

# Load BST 

@st.cache_resource(show_spinner=False)
def build_tree(limit=None):

    # Creating a BST with all plots and titles, and caching it so it only builds once per session
    stories_data = load_dataset(TITLES_PATH, PLOTS_PATH, limit=limit)
    bst = BinarySearchTree()
    for entry in stories_data:
        story = Story(
            title=entry['title'],
            plot=entry['plot'],
            year=entry['year']
        )
        bst.insert(entry['normalized_title'], story)
    return bst


# Page Config
st.set_page_config(
    page_title="WikiPlots BST Search",
    page_icon="📖",
    layout="wide"
)


# Header
st.title("📖 WikiPlots Story Search Engine")
st.markdown("Search and explore **112,000+ story plots** from Wikipedia using a **Binary Search Tree**.")
st.divider()

# Loading data with progress bar
with st.spinner("Building BST from dataset... (this takes ~10 seconds on first load)"):
    bst = build_tree(limit=None)  # Change to limit=5000 for faster testing

st.success(f"✅ BST ready — {bst.size:,} stories loaded.")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a feature:",
    ["🔍 Search by Title",
     "🔤 Browse Alphabetically",
     "🔎 Search by Prefix",
     "📅 Filter by Year",
     "🗑️ Delete a Story",
     "📊 BST Balance Report"]
)

# =========================================================
# PAGE 1: Search by Title
# =========================================================
if page == "🔍 Search by Title":
    st.header("🔍 Search by Exact Title")
    st.markdown("Enter a story title to retrieve its full plot summary.")

    query = st.text_input("Enter title (case-insensitive):", placeholder="e.g. titanic")

    if query:
        start = time.time()
        result = bst.search(query)
        elapsed = time.time() - start

        if result:
            st.success(f"Found in **{elapsed:.6f}s**")
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader(result.title)
            with col2:
                st.metric("Year", result.year if result.year else "Unknown")

            with st.expander("📄 View Full Plot Summary", expanded=True):
                st.write(result.plot if result.plot else "No plot available.")
        else:
            st.error("Story not found. Try lowercase, e.g. `the godfather`")

# =========================================================
# PAGE 2: Browse Alphabetically
# =========================================================
elif page == "🔤 Browse Alphabetically":
    st.header("🔤 Browse All Stories (A–Z)")
    st.markdown("In-order traversal of the BST returns all stories in alphabetical order.")

    all_stories = bst.inorder()
    total = len(all_stories)

    # Pagination
    per_page = 50
    total_pages = (total // per_page) + 1
    page_num = st.number_input("Page", min_value=1, max_value=total_pages, value=1, step=1)
    start_idx = (page_num - 1) * per_page
    end_idx = min(start_idx + per_page, total)

    st.markdown(f"Showing **{start_idx + 1}–{end_idx}** of **{total:,}** stories")
    st.divider()

    for story in all_stories[start_idx:end_idx]:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"📘 {story.title}")
        with col2:
            st.write(story.year if story.year else "—")

# =========================================================
# PAGE 3: Search by Prefix
# =========================================================
elif page == "🔎 Search by Prefix":
    st.header("🔎 Search by Title Prefix")
    st.markdown("Type the first few letters of a title to find all matching stories.")

    prefix = st.text_input("Enter prefix:", placeholder="e.g. star")

    if prefix:
        results = bst.prefix_search(prefix)
        st.info(f"Found **{len(results)}** stories starting with **'{prefix}'**")

        if results:
            for story in results[:50]:
                with st.expander(f"📘 {story.title}  ({story.year or 'N/A'})"):
                    st.write(story.plot[:500] + "..." if len(story.plot) > 500 else story.plot)

            if len(results) > 50:
                st.warning(f"Showing first 50 of {len(results)} results.")

# =========================================================
# PAGE 4: Filter by Year
# =========================================================
elif page == "📅 Filter by Year":
    st.header("📅 Filter Stories by Year")
    st.markdown("Find all stories with a known release year in a given range.")

    col1, col2 = st.columns(2)
    with col1:
        start_year = st.number_input("Start Year", min_value=1800, max_value=2030, value=2000)
    with col2:
        end_year = st.number_input("End Year", min_value=1800, max_value=2030, value=2010)

    if st.button("Search"):
        if start_year > end_year:
            st.error("Start year must be before end year.")
        else:
            results = bst.filter_by_year(int(start_year), int(end_year))
            st.success(f"Found **{len(results)}** stories from {start_year} to {end_year}")

            for story in results[:50]:
                with st.expander(f"📘 {story.title}  ({story.year})"):
                    st.write(story.plot[:500] + "..." if len(story.plot) > 500 else story.plot)

            if len(results) > 50:
                st.warning(f"Showing first 50 of {len(results)} results.")

# =========================================================
# PAGE 5: Delete a Story
# =========================================================
elif page == "🗑️ Delete a Story":
    st.header("🗑️ Delete a Story")
    st.markdown("Remove a story from the BST by its title. The tree rebalances its ordering automatically.")

    del_query = st.text_input("Enter title to delete (case-insensitive):", placeholder="e.g. titanic")

    if del_query:
        # Preview before deleting
        preview = bst.search(del_query)
        if preview:
            st.warning(f"Found: **{preview.title}** ({preview.year or 'Unknown'})")
            if st.button("Confirm Delete"):
                success = bst.delete(del_query)
                if success:
                    st.success(f"Deleted '{preview.title}'. Tree now has {bst.size:,} stories.")
                else:
                    st.error("Deletion failed.")
        else:
            st.error("Story not found.")

# =========================================================
# PAGE 6: BST Balance Report
# =========================================================
elif page == "📊 BST Balance Report":
    st.header("📊 BST Balance Report")
    st.markdown("""
    A plain BST's efficiency depends on how **balanced** the tree is.
    If titles are inserted in alphabetical order, the tree degrades to a linked list with **O(n)** search.
    This report shows how balanced our tree actually is.
    """)

    if st.button("Run Balance Report"):
        import math
        with st.spinner("Calculating tree height..."):
            height = bst.tree_height()
            ideal  = math.log2(bst.size + 1) if bst.size > 0 else 0
            ratio  = (ideal / height * 100) if height > 0 else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Nodes", f"{bst.size:,}")
        col2.metric("Actual Height", height)
        col3.metric("Ideal Height", f"{ideal:.1f}")

        st.divider()
        st.progress(min(int(ratio), 100), text=f"Balance Ratio: {ratio:.1f}% of optimal")

        if ratio < 50:
            st.error("⚠️ Tree is significantly unbalanced. An AVL or Red-Black tree would fix this.")
        elif ratio < 75:
            st.warning("🔶 Tree is moderately balanced.")
        else:
            st.success("✅ Tree is well balanced for this dataset.")

        st.info("""
        **Why does this happen?**
        Wikipedia titles aren't randomly distributed — many start with 'The', 'A', etc.
        This clustering causes some branches to grow much deeper than others.
        A self-balancing BST (AVL or Red-Black) would automatically fix this after every insert.
        """)

# -------------------------
# Footer
# -------------------------
st.divider()
st.caption("WikiPlots BST Search Engine | Data Structure: Binary Search Tree | Dataset: WikiPlots by Mark Riedl")