# Defines the Story data class that holds each record stored in the BST.

class Story:
    def __init__(self, title, plot, year=None):
        self.title = title        # Original title for display
        self.plot = plot          # Full plot summary text
        self.year = year          # Extracted year as int, or None

    def __repr__(self):
        return f"Story(title={self.title!r}, year={self.year})"