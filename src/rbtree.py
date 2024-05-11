from PrettyPrintTree import PrettyPrintTree
from typing import Generic, TypeVar
from enum import Enum

T = TypeVar("T")


class RedBlackTreeColor(Enum):
    RED = 0
    BLACK = 1


class RedBlackTreeNode(Generic[T]):
    """
    Represents a node in an AVL Tree
    """

    def __init__(
        self,
        val: T,
        left: "RedBlackTreeNode | None" = None,
        right: "RedBlackTreeNode | None" = None,
        parent: "RedBlackTreeNode | None" = None,
        color: RedBlackTreeColor = RedBlackTreeColor.RED,
    ):
        self.left = left
        self.right = right
        self.val = val
        self.parent = parent
        self.color = color

    def children(self) -> list["RedBlackTreeNode"]:
        """
        Returns the children of a node as an iterable
        """
        children = []
        if self.left:
            children.append(self.left)
        if self.right:
            children.append(self.right)
        return children


class RedBlackTree(Generic[T]):
    """
    A Red black Tree is a Binary Search Tree that is approximately height balanced
    """

    def __init__(self, root: "RedBlackTreeNode | None" = None):
        self.root = root
        self.pretty_printer = PrettyPrintTree(
            lambda node: node.children(),
            lambda node: node.val,
            return_instead_of_print=True,
        )

    def __str__(self) -> str:
        if self.root:
            return self.pretty_printer(self.root)
        else:
            return f"Empty-Tree"

    def _left_rotate(self, node: RedBlackTreeNode) -> None:
        r"""
            C                                A
           /  \     left Rotation at C      / \   
          /    A    ---------------->      C   \
         /   /  \                         / \   \
        E    B   D                        E  B   D

        This is a visual description of the transformation. It is a counter-clockwise rotation of the tree
        where the right child of {node} becomes the parent.
        """
        parent_of_node = node.parent
        right_child = node.right
        assert right_child is not None
        right_childs_left_child = right_child.left
        # link node and rights child left child
        node.right = right_childs_left_child
        if right_childs_left_child:
            right_childs_left_child.parent = node
        # link node and right child. right child is new parent
        right_child.left = node
        node.parent = right_child
        # Fix up links with parent_of_node
        right_child.parent = parent_of_node
        if not parent_of_node:
            self.root = right_child
        elif parent_of_node.right == node:
            parent_of_node.right = right_child
        else:
            parent_of_node.left = right_child

    def _right_rotate(self, node: RedBlackTreeNode) -> None:
        r"""
            C                                A
           /  \     right Rotation at C     / \   
          A    \    ---------------->      /   C 
         / \    \                         /   / \
        B   D    E                       B   D    E

        This is a visual description of the transformation. It is a clockwise rotation of the tree
        where the left child of {node} becomes the parent.
        """
        parent_of_node, left_child = node.parent, node.left
        assert left_child is not None
        left_childs_right_child = left_child.right
        # Node and left_childs_right child need to be linked
        node.left = left_childs_right_child
        if left_childs_right_child:
            left_childs_right_child.parent = node
        # left_child becomes new root of subtree
        left_child.right = node
        node.parent = left_child
        # link to subtree above
        left_child.parent = parent_of_node
        if not parent_of_node:
            self.root = node
        elif parent_of_node.left == node:
            parent_of_node.left = left_child
        else:
            parent_of_node.right = left_child

    def is_empty(self) -> bool:
        """
        Returns True if the tree is empty
        """
        return self.root is None

    def search(self, val: T) -> bool:
        """
        Search for a key with {val} in the Tree
        """

        def search_from_node(val: T, node: RedBlackTreeNode | None) -> bool:
            if node is None:
                return False
            elif node.val == val:
                return True
            elif val < node.val:
                return search_from_node(val, node.left)
            else:
                return search_from_node(val, node.right)

        return search_from_node(val, self.root)
