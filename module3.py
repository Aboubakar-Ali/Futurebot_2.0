class BinaryTreeNode:
    def __init__(self, question, left=None, right=None):
        self.question = question
        self.left = left
        self.right = right

class BinaryTree:
    def __init__(self, root):
        self.root = root
        self.current_node = root

    def reset(self):
        self.current_node = self.root

    def traverse_left(self):
        if self.current_node.left:
            self.current_node = self.current_node.left

    def traverse_right(self):
        if self.current_node.right:
            self.current_node = self.current_node.right

    def get_current_question(self):
        return self.current_node.question

