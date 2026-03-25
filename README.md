# HW3 Extra Credit Project

--- 

# WikiPlots BST Search Engine

This is a story search and indexing application built using a **Binary Search Tree (BST)**,
applied to the vast [WikiPlots dataset](https://github.com/markriedl/WikiPlots) —
This ia a real-world collection of 112,936 story plot summaries. These plots are
extracted from English-language Wikipedia.

This project was created to demonstrate how a classic data structure can be applied
to a large, noisy, real-world dataset.

---

## Features

- 🔍 **Search Stories** — Search by full title or prefix (e.g. type `star` to find all Star Wars, Stargate, etc.)
- 🔤 **Browse Alphabetically** — In-order BST traversal returns all stories sorted A–Z with pagination
- 📅 **Filter by Year** — Retrieve all stories within a specified year range
- 🗑️ **Delete a Story** — Remove a story from the BST while preserving tree ordering
- 📊 **BST Balance Report** — Visualizes actual vs ideal tree height to demonstrate BST limitations at scale

---

## Data Structure

The core data structure used is a **Binary Search Tree (BST)** where each node stores a `Story` object,
whose key is a normalized i.e. lowercase form of the title.

| Operation | Average Case | Worst Case |
|---        |---           |---         |
| Insert    | O(log n)     | O(n)       |
| Search    | O(log n)     | O(n)       |
| Delete    | O(log n)     | O(n)       |
| Traversal | O(n)         | O(n)       |

> Worst case occurs when input is already sorted (alphabetical),
> causing the tree to degrade into a linked list.
> This limitation is demonstrated in the BST Balance Report feature.

---

## Project Structure
```
WikiPlots-BST/
├── data/                    # Dataset files (not included — steps to setup is below)
├── docs/
│   ├── Project Proposal_MSML606.pdf
│   └── presentation.pdf
├── src/
│   ├── bst.py               # Binary Search Tree implementation (core algorithm)
│   ├── story.py             # Story data class
│   ├── preprocessing.py     # Data loading and cleaning
│   └── app.py               # Streamlit frontend
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Setup Instructions

To use this project for on your private computer, you can follow the instructions given below:

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/WikiPlots-BST.git
cd WikiPlots-BST
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download the dataset
- Go to: https://github.com/markriedl/WikiPlots
- Download **plots.zip** and extract it
- Place the two extracted files (`plots` and `titles`) inside the `data/` folder
```
data/
├── plots       ← place here
└── titles      ← place here
```

### 5. Run the application
```bash
streamlit run src/app.py
```

The app will open automatically in your browser at `http://localhost:8501`

---

## Data Preprocessing

Since the WikiPlots dataset comes from real-world Wikipedia extractions,
the following preprocessing steps are applied before inserting records into the BST:

- Titles are **normalized** (lowercased, whitespace removed) for consistent key comparison
- **Years** are extracted from titles using regex (e.g. `The Thing (1982)` → `1982`)
- **Missing or empty** title entries are skipped
- **Encoding artifacts** are handled using `errors='replace'` during file reading

---

## Known Limitations

- A plain BST on alphabetically clustered input (e.g. many titles starting with "The")
  can become unbalanced, degrading search to O(n)
- Year filtering requires a full O(n) traversal since the BST node key is based on title, not year
- No self-balancing mechanism — an AVL or Red-Black tree would address this

These limitations are documented and demonstrated in the **BST Balance Report** feature.

---

## Academic Integrity & Sources

- **Dataset**: WikiPlots by Mark Riedl — https://github.com/markriedl/WikiPlots
- **External libraries**: `streamlit`, `tqdm`, `colorama` (UI only — no library performs BST logic)

---

## AI usage Statement

- **Google**: Dataset search and easy to implement frontend
- **Claude**: Most of the frontend and sanity check on written code
- **OpenAI**: Recommendation for project structure
- **Youtube**: Implementation of BST, and different strategies for preprocessing

---

## Course

MSML606 — Algorithms and Data Structures for Machine Learning