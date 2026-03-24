# Core data structure: Binary Search Tree (BST)
# Each node stores a Story object, keyed by normalized title.
# Supports: insert, search, delete, in-order traversal, prefix search, balance report.

class BSTNode:
    # A single node in the Binary Search Tree.
    def __init__(self, key, story):
        self.key = key        # Normalized title string (ordering key)
        self.story = story    # Story object with all data
        self.left = None      # Left child (alphabetically smaller)
        self.right = None     # Right child (alphabetically larger)


class BinarySearchTree:
   
    def __init__(self):
        self.root = None
        self.size = 0

    
    # --INSERT--
    def insert(self, key, story):

        # Inserting a Story into the BST using normalized title as key
        self.root = self._insert(self.root, key, story)
        self.size += 1

    def _insert(self, node, key, story):

        if node is None:
            return BSTNode(key, story)
        if key < node.key:
            node.left = self._insert(node.left, key, story)
        elif key > node.key:
            node.right = self._insert(node.right, key, story)

        # Duplicate keys are ignored
        return node

    # --SEARCH--
    def search(self, key):
        
        # Searchs for a story by title, returns story or none if not found.
        return self._search(self.root, key.strip().lower())

    def _search(self, node, key):

        if node is None:
            return None
        if key == node.key:
            return node.story
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    # --DELETE--
    def delete(self, key):

        # Remove a node by key while maintaing BST order
        self.root, deleted = self._delete(self.root, key.strip().lower())
        if deleted:
            self.size -= 1
        return deleted

    def _delete(self, node, key):
        if node is None:
            return node, False

        deleted = False
        if key < node.key:
            node.left, deleted = self._delete(node.left, key)
        elif key > node.key:
            node.right, deleted = self._delete(node.right, key)
        else:
            # If node found we handle the 3 cases 
            deleted = True
            if node.left is None:
                return node.right, deleted
            elif node.right is None:
                return node.left, deleted
            else:
                # If node has two children, we replace it with in-order successor
                successor = self._min_node(node.right)
                node.key = successor.key
                node.story = successor.story
                node.right, _ = self._delete(node.right, successor.key)

        return node, deleted

    def _min_node(self, node):

        # Find the leftmost i.e. minimum node in a subtree
        while node.left is not None:
            node = node.left
        return node

    # --IN-ORDER TRAVERSAL--

    # Returns all stories in alphabetical order
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.story)
        self._inorder(node.right, result)

    # --PREFIX SEARCH--

    def prefix_search(self, prefix):
      
        # Return all stories whose title starts with the given prefix i.e. given starting of the title
        prefix = prefix.strip().lower()
        results = []
        self._prefix_search(self.root, prefix, results)
        return results

    def _prefix_search(self, node, prefix, results):
        if node is None:
            return
        if node.key >= prefix:
            self._prefix_search(node.left, prefix, results)
        if node.key.startswith(prefix):
            results.append(node.story)
        if node.key <= prefix + '\xff':
            self._prefix_search(node.right, prefix, results)

    # --YEAR RANGE FILTER--

    # Returns all stories with year in [start_year, end_year]
    def filter_by_year(self, start_year, end_year):
        all_stories = self.inorder()
        return [s for s in all_stories if s.year and start_year <= s.year <= end_year]

   
    # --BALANCE REPORT--
    
    # Calculates the height of the BST
    def tree_height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))


    # Comparing actual tree height vs ideal balanced height.
    def balance_report(self):
        
        import math
        height = self.tree_height()
        ideal = math.log2(self.size + 1) if self.size > 0 else 0
        ratio = (ideal / height * 100) if height > 0 else 0

        print(f"\n--- BST Balance Report ---")
        print(f"Total nodes   : {self.size}")
        print(f"Actual height : {height}")
        print(f"Ideal height  : {ideal:.1f}  (log2 of node count)")

        # Demonstrates the known limitation of a plain BST on real-world data.
        print(f"Balance ratio : {ratio:.1f}% of optimal")

        if ratio < 50:
            print("Status        : Tree is significantly unbalanced.")
            print("Note          : An AVL or Red-Black tree would fix this.")
        else:
            print("Status        : Tree is reasonably balanced for this dataset.")
        print("--------------------------")