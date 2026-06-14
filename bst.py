class BSTNode:
    def __init__(self, task):
        self.task = task
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, task):
        self.root = self._insert(self.root, task)

    def _insert(self, node, task):
        if node is None:
            return BSTNode(task)
        if task.deadline < node.task.deadline:
            node.left = self._insert(node.left, task)
        else:
            node.right = self._insert(node.right, task)
        return node

    def rebuild(self, tasks):
        """пересобирает дерево из списка задач"""
        self.root = None
        for task in tasks:
            self.insert(task)

    def inorder(self, node, result):
        """рекурсивный обход в порядке возрастания дедлайна"""
        if node is None:
            return
        self.inorder(node.left, result)
        result.append(node.task)
        self.inorder(node.right, result)

    def find_min(self):
        """возвращает задачу с самым ранним дедлайном"""
        if self.root is None:
            return None
        return self._find_min(self.root).task

    def _find_min(self, node):
        if node.left is None:
            return node
        return self._find_min(node.left)

    def find_max(self):
        """возвращает задачу с самым поздним дедлайном"""
        if self.root is None:
            return None
        return self._find_max(self.root).task

    def _find_max(self, node):
        if node.right is None:
            return node
        return self._find_max(node.right)