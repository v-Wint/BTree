import bisect


class Node:
    def __init__(self):
        self.keys = []
        self.child = []

    @property
    def n(self):
        return len(self.keys)

    @property
    def leaf(self):
        return not self.child

    def __str__(self):
        return " ".join(map(str, self.keys))


class BTree:
    def __init__(self, t):
        if t <= 1:
            raise ValueError("t must be greater than or equal to 2")

        self.t = t
        self.min_keys = t - 1
        self.max_keys = 2 * t - 1

        self.root = Node()

    @staticmethod
    def key_in_node(node, key, i):
        return i < node.n and key == node.keys[i]

    def search(self, key):
        return self._search_in_node(self.root, key)

    def _search_in_node(self, node, key):
        i = bisect.bisect_left(node.keys, key)
        if self.key_in_node(node, key, i):
            return node, i
        if node.leaf:
            return None
        return self._search_in_node(node.child[i], key)

    def insert(self, key):
        if self.root.n == self.max_keys:
            self._split_root()
        self._insert_non_full(self.root, key)

    def _split_root(self):
        new_root = Node()
        new_root.child = [self.root]
        self.root = new_root
        self._split_child(new_root, 0)

    def _split_child(self, parent, i):
        t = self.t

        right = Node()
        left = parent.child[i]

        right.keys = left.keys[t:]
        middle = left.keys[t-1]
        left.keys = left.keys[:t-1]

        if not left.leaf:
            right.child = left.child[t:]
            left.child = left.child[:t]

        parent.keys.insert(i, middle)
        parent.child.insert(i+1, right)

    def _insert_non_full(self, node, key):
        i = bisect.bisect_left(node.keys, key)

        if node.leaf:
            node.keys.insert(i, key)
            return

        if node.child[i].n == self.max_keys:
            self._split_child(node, i)
            if node.keys[i] < key:
                i += 1

        self._insert_non_full(node.child[i], key)

    def delete(self, key):
        self._delete_in_node(self.root, key)

    def _delete_in_node(self, node, key, find_delete_predecessor=False):
        def check_root(i):
            if self.root.n == 0:
                self.root = self.root.child[i]

        i = bisect.bisect_left(node.keys, key)

        # case 1
        if node.leaf:
            if find_delete_predecessor:
                i = i if i < node.n else node.n - 1
                tmp = node.keys[i]
                del node.keys[i]
                return tmp

            if self.key_in_node(node, key, i):
                del node.keys[i]
            return

        # case 2
        if self.key_in_node(node, key, i):
            # case 2a-b
            # continue descent until the predecessor is put in the place of current key,
            # ensuring the properties after its deletion
            if (curr := node.child[i]).n > self.min_keys or (curr := node.child[i+1]).n > self.min_keys:
                node.keys[i] = self._delete_in_node(curr, key, True)
            # case 2c
            # merge children
            else:
                del node.keys[i]
                node.child[i].keys += node.child[i + 1].keys
                node.child[i].child += node.child[i + 1].child
                del node.child[i + 1]
                check_root(i)
            return

        # case 3
        # continue descent guaranteeing the child to have t keys
        if (curr := node.child[i]).n == self.min_keys:
            # case 3a
            # steal a key from a sibling
            if i > 0 and (sibling := node.child[i-1]).n > self.min_keys:
                i -= 1
                curr.keys.insert(0, node.keys[i])
                node.keys[i] = sibling.keys.pop()
                if sibling.child:
                    curr.child.insert(0, sibling.child.pop())
            elif i < node.n and (sibling := node.child[i+1]).n > self.min_keys:
                curr.keys.append(node.keys[i])
                node.keys[i] = sibling.keys.pop(0)
                if sibling.child:
                    curr.child.append(sibling.child.pop(0))

            # case 3b
            # merge child with sibling
            else:
                if i > 0:
                    i -= 1
                    sibling = node.child[i]
                    curr.keys = sibling.keys + [node.keys[i]] + curr.keys
                    curr.child = sibling.child + curr.child
                    del node.child[i]
                    del node.keys[i]
                else:
                    sibling = node.child[i+1]
                    curr.keys += [node.keys[i]] + sibling.keys
                    curr.child += sibling.child
                    del node.child[i+1]
                    del node.keys[i]

                check_root(i)

        return self._delete_in_node(curr, key, find_delete_predecessor)

    def __repr__(self):
        def print_node(node, level):
            return '\n'.join(
                ['\t' * level + str(node)] +
                [print_node(child, level + 1) for child in node.child]
            )
        return print_node(self.root, 0)

    def __len__(self):
        def calc_length(node):
            return node.n + sum(calc_length(child) for child in node.child)
        return calc_length(self.root)
