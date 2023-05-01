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

# # Création de l'arbre binaire
# root = BinaryTreeNode("Quel langage de programmation souhaitez-vous apprendre (Python ou Java) ?")
# left_child = BinaryTreeNode("Voulez-vous apprendre les bases de Python ou les concepts avancés ?")
# right_child = BinaryTreeNode("Voulez-vous apprendre les bases de Java ou les concepts avancés ?")
# python_basic = BinaryTreeNode("Vous pouvez commencer par le cours Python pour les débutants. Voulez-vous que je vous propose des liens ?")
# python_advanced = BinaryTreeNode("Vous pouvez consulter le cours Python avancé. Voulez-vous que je vous propose des liens ?")
# java_basic = BinaryTreeNode("Vous pouvez commencer par le cours Java pour les débutants. Voulez-vous que je vous propose des liens ?")
# java_advanced = BinaryTreeNode("Vous pouvez consulter le cours Java avancé. Voulez-vous que je vous propose des liens ?")

# root.left = left_child
# root.right = right_child
# left_child.left = python_basic
# left_child.right = python_advanced
# right_child.left = java_basic
# right_child.right = java_advanced