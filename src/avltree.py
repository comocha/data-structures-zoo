"""Some design choices:
Why did I seperate AvlTreeNode from AvlTree.
I wanted to write functions like insert() and search() to be instance
methods but also work on empty trees.
Realistically insert() and search would not be instance methods if I only AVLTreeNode. 
They would instead take an argument of type Optional[AVLTreeNode]. 
If they were instance methods, I'd have to special casing and check 
everytime I invoke node.left.insert() or node.right.search(). 

In python an empty tree is represented by None. 
With a wrapper class, I can still define insert() and search()
on the AVLTree class and have inner closure methods that operate on Optional[AVLTreeNode]

Some good things to know:
A "rotation" (single or double) happens only once per insert. It is at the lowest node in the ancestor
chain that has it's balance factor violated. After "rotations", the height of the node with the violation
is the same as it was prior to violation. Thus we theoretically can stop fixing up the ancestor chain from this node.
In the algorithm below, we do call _apply_rotation all the way to the top for simplicity. We'd just be nooping after
the node with the first rotation
"""

from PrettyPrint import PrettyPrintTree
from typing import Generic, TypeVar

T = TypeVar("T")


class AvlTreeNode(Generic[T]):
    """
    Represents a node in an AVL Tree
    """

    def __init__(
        self,
        val: T,
        left: "AvlTreeNode | None" = None,
        right: "AvlTreeNode | None" = None,
    ):
        self.left = left
        self.right = right
        self.val = val
        self.height = 1

    def children(self) -> list["AvlTreeNode"]:
        """
        Returns the children of a node as an iterable
        """
        children = []
        if self.left:
            children.append(self.left)
        if self.right:
            children.append(self.right)
        return children

    def balance(self) -> int:
        """
        Returns the balance of the tree.
        For an AVL tree, this value is in the range {0, 1, -1}
        We need to rebalance a node via rotations if the balance ever assumes the values 2 or -2
        """
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        return right_height - left_height


class AvlTree(Generic[T]):
    """
    An AVL Tree is a Binary Search Tree that is height balanced. It performs rotations on insertions and deletions
    """

    def __init__(self, root: "AvlTreeNode | None" = None):
        self.root = root
        self.pretty_printer = PrettyPrintTree(
            lambda node: node.children(),
            lambda node: node.val,
            return_instead_of_print=True,
        )

    def is_empty(self) -> bool:
        """
        Returns True if the tree is empty
        """
        return self.root is None

    def __str__(self) -> str:
        return self.pretty_printer(self.root)

    @staticmethod
    def _left_rotate(node: AvlTreeNode) -> AvlTreeNode:
        r"""
            C                                A
           /  \     left Rotation at C      / \   
          /    A    ---------------->      C   \
         /   /  \                         / \   \
        E    B   D                        E  B   D

        This is a visual description of the transformation. It is a counter-clockwise rotation of the tree
        where the right child of {node} becomes the parent.
        """
        right_child = node.right
        assert right_child is not None
        right_childs_left_child = right_child.left
        node.right = right_childs_left_child
        right_child.left = node
        AvlTree._fix_height(node)
        AvlTree._fix_height(right_child)
        return right_child

    @staticmethod
    def _right_rotate(node: AvlTreeNode) -> AvlTreeNode:
        r"""
            C                                A
           /  \     right Rotation at C      / \   
          A    \    ---------------->      /   C 
         / \    \                         /    / \
        B   D    E                       B   D    E

        This is a visual description of the transformation. It is a clockwise rotation of the tree
        where the left child of {node} becomes the parent.
        """
        left_child = node.left
        assert left_child is not None
        left_childs_right_child = left_child.right
        node.left = left_childs_right_child
        left_child.right = node
        AvlTree._fix_height(node)
        AvlTree._fix_height(left_child)
        return left_child

    @staticmethod
    def _apply_rotation(node: AvlTreeNode) -> AvlTreeNode:
        balance = node.balance()
        if balance > 1:  # right heavy
            if node.right and node.right.balance() < 0:
                node.right = AvlTree._right_rotate(node.right)
            return AvlTree._left_rotate(node)
        elif balance < 1:  # left heavy:
            if node.left and node.left.balance() > 0:
                node.left = AvlTree._left_rotate(node.left)
            return AvlTree._right_rotate(node)
        return node

    @staticmethod
    def _fix_height(node: AvlTreeNode) -> None:
        height = 1 + max(
            node.left.height if node.left else 0, node.right.height if node.right else 0
        )
        node.height = height

    def search(self, val: T) -> bool:
        """
        Search for a key with {val} in the Tree
        """

        def search_from_node(val: T, node: AvlTreeNode | None) -> bool:
            if node is None:
                return False
            elif node.val == val:
                return True
            elif val < node.val:
                return search_from_node(val, node.left)
            else:
                return search_from_node(val, node.right)

        return search_from_node(val, self.root)

    def insert(self, val: T) -> bool:
        """
        Inserts a value {val} into the tree. If the value already exists, we return False.
        On success of the operation, we return True.
        Failure is due to the key existing in the tree.
        A boolean is sufficient for the return type as we can only fail under one circumstance:
        The value is already present in the tree
        """

        def insert_from_node(node: AvlTreeNode | None) -> AvlTreeNode | None:
            if node is None:
                return AvlTreeNode(val, None, None)
            elif node.val == val:
                return None
            elif node.val > val:
                left_tree = insert_from_node(node.left)
                if not left_tree:
                    return None
                else:
                    node.left = left_tree
            else:
                right_tree = insert_from_node(node.right)
                if not right_tree:
                    return None
                else:
                    node.right = right_tree
            AvlTree._fix_height(node)
            return AvlTree._apply_rotation(node)

        tree_after_insertion = insert_from_node(self.root)
        if tree_after_insertion:
            self.root = tree_after_insertion
            return True  # Insertion succeeded
        else:
            return False  # Insertion failed
