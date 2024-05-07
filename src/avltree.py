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

References:
https://www.cs.cmu.edu/~rjsimmon/15122-m15/lec/16-avl.pdf
https://www.youtube.com/watch?v=Jj9Mit24CWk&list=PLlsmxlJgn1HJRYU7YIf8DSEg8_DGwSV29&index=3

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

    def __str__(self) -> str:
        if self.root:
            return self.pretty_printer(self.root)
        else:
            return f"Empty-Tree"

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
        elif balance < -1:  # left heavy:
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

    @staticmethod
    def _find_max(node: AvlTreeNode):
        cur = node
        while cur.right:
            cur = cur.right
        return cur.val

    def is_empty(self) -> bool:
        """
        Returns True if the tree is empty
        """
        return self.root is None

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

    def insert(self, val: T) -> None:
        """
        Inserts a value {val} into the tree. If the value already exists, this is a noop
        """

        def insert_from_node(node: AvlTreeNode | None) -> AvlTreeNode:
            if node is None:
                return AvlTreeNode(val, None, None)
            elif node.val == val:
                return node
            elif node.val > val:
                node.left = insert_from_node(node.left)
            else:
                node.right = insert_from_node(node.right)
            AvlTree._fix_height(node)
            return AvlTree._apply_rotation(node)

        tree_after_insertion = insert_from_node(self.root)
        self.root = tree_after_insertion

    def delete(self, val: T) -> None:
        """
        Delete a value {val} from the Tree
        """

        def delete_node(node: AvlTreeNode | None, key: T) -> AvlTreeNode | None:
            if not node:
                return None
            new_root = node
            print(f"node {node.val} deleting key {key}")
            if node.val > key:
                node.left = delete_node(node.left, key)
            elif node.val < key:
                node.right = delete_node(node.right, key)
            else:
                # remove root
                if node.left is None:
                    new_root = node.right
                    node.right = None
                elif node.right is None:
                    new_root = node.left
                    node.left = None
                else:
                    node.val = AvlTree._find_max(node.left)
                    node.left = delete_node(node.left, node.val)
                    new_root = node
            if new_root:
                self._fix_height(new_root)
                new_root = self._apply_rotation(new_root)
            return new_root

        self.root = delete_node(self.root, val)
