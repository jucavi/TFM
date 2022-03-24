class FolderNode():
    def __init__(self, folder):
        self.folder = folder

    @property
    def name(self):
        return self.folder.foldername

    @property
    def children(self):
        return self.folder.children

    @property
    def get_id(self):
        return self.folder.id

    def __repr__(self):
        return str(self.name)

    def __str__(self):
        return self.name

class Tree(object):
    def __init__(self):
        self.folders = {}

    def add_node(self, node):
        if node in self.folders:
            # pass
            raise ValueError('Duplicate folder')
        self.folders[node] = node.children

    def get_node(self, name):
        for node in self.folders:
            if node.name == name:
                return node
        return None

    def get_node(self, name):
        for node in self.folders:
            if node.name == name:
                return node
        return None

    def has_node(self, node):
        return node in self.folders

    def children_of(self, node):
        return self.folders.get(node)

    def __str__(self):
        return str(self.folders)


class BuildTree():
    def __init__(self, root_folder):
        self.tree = Tree()
        self.build_tree(root_folder)

    def build_tree(self, node):
        stack = [node]

        while stack:
            current = stack[0]
            stack.pop(0)
            stack += current.children
            self.tree.add_node(FolderNode(current))


    def __str__(self):
        return str(self.tree)
