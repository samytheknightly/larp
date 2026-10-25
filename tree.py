class Tree:
    def __init__(self):
        self.root = Node(1)
    def print(self):
        self.root.print()
    def get_deepest_node(self):
        return self.root.get_deepest_node(0)

class Node:
    def __init__(self, val):
        self.val = val
        self.children: list[Node] = []
    def append(self, node):
        self.children.append(node)
    def print(self):
        print(self.val)
        for child in self.children:
            child.print()
    def get_deepest_node(self, depth):
        front = []
        visited = []

        for child in self.children:
            front.append(child)
            visited.append(child.get_deepest_node(depth+1))
        if len(visited):
            return max(visited, key=lambda x: x[1])

        return (self, depth)

        

tree = Tree()
tree.root.append(Node(2))
tree.root.append(Node(3))
tree.root.children[0].append(Node(4))
tree.root.children[1].append(Node(5))
tree.root.children[0].children[0].append(Node(6))
tree.print()
print(tree.get_deepest_node()[0].val, tree.get_deepest_node()[1])