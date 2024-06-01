"""
6.101 Lab:
Autocomplete
"""

# NO ADDITIONAL IMPORTS!
import doctest
from text_tokenize import tokenize_sentences


class PrefixTree:
    """Autocomplete lab prefix tree data structure attributes and methods"""

    def __init__(self):
        self.value = None
        self.children = {}

    def type_check(self, key):
        """Checks if key is a string"""
        if not isinstance(key, str):
            raise TypeError

    def __setitem__(self, key, value):
        """
        Add a key with the given value to the prefix tree,
        or reassign the associated value if it is already present.
        Raise a TypeError if the given key is not a string.
        """
        self.type_check(key)
        if len(key) == 0:
            self.value = value
        else:
            let = key[0]
            if let not in self.children:
                self.children[let] = PrefixTree()
            self.children[let].__setitem__(key[1:], value)

    def __getitem__(self, key):
        """
        Return the value for the specified prefix.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        self.type_check(key)
        if len(key) == 0:
            if self.value is None:
                raise KeyError
            return self.value
        else:
            let = key[0]
            if let not in self.children:
                raise KeyError
            return self.children[let][key[1:]]

    def __delitem__(self, key):
        """
        Delete the given key from the prefix tree if it exists.
        Raise a KeyError if the given key is not in the prefix tree.
        Raise a TypeError if the given key is not a string.
        """
        self.type_check(key)
        if len(key) == 0:
            if self.value is None:
                raise KeyError
            self.value = None
        else:
            let = key[0]
            if let not in self.children:
                raise KeyError
            del self.children[let][key[1:]]

    def __contains__(self, key):
        """
        Is key a key in the prefix tree?  Return True or False.
        Raise a TypeError if the given key is not a string.
        """
        self.type_check(key)
        if len(key) == 0:
            return self.value is not None

        let = key[0]
        if let in self.children:
            return key[1:] in self.children[let]

        return False

    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this prefix tree
        and its children.  Must be a generator!
        """

        def search(node, direct=""):
            if node.value is not None:
                yield (direct, node.value)

            for key, child in node.children.items():
                yield from search(child, direct + key)

        yield from search(self)


def word_frequencies(text):
    """
    Given a piece of text as a single string, create a prefix tree whose keys
    are the words in the text, and whose values are the number of times the
    associated word appears in the text.
    """
    tree, sentences = PrefixTree(), tokenize_sentences(text)
    words = [word for sent in sentences for word in sent.split()]
    for each in words:
        if each in tree:
            tree[each] += 1
        else:
            tree[each] = 1
    return tree


def autocomplete(tree, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is not a string.
    """
    if not isinstance(prefix, str):
        raise TypeError

    def key_collect(node, pref):
        if node.value is not None:
            result.append(pref)
        for char, child_node in node.children.items():
            key_collect(child_node, pref + char)

    node, result = tree, []
    for note in prefix:
        if note in node.children:
            node = node.children[note]
        else:
            return result

    key_collect(node, prefix)
    result.sort(key=lambda x: -tree[x])

    return result[:max_count] if max_count is not None else result


def autocorrect(tree, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    comp = autocomplete(tree, prefix, max_count)
    lowercase_letters = "abcdefghijklmnopqrstuvwxyz"

    if max_count and max_count <= len(comp):
        return comp

    changes = set()
    for i, _ in enumerate(prefix):
        for c in lowercase_letters:
            delete = prefix[:i] + prefix[i + 1 :]
            insert = prefix[:i] + c + prefix[i:]
            replace = prefix[:i] + c + prefix[i + 1 :]
            for delta in (delete, insert, replace):
                if delta in tree:
                    changes.add((delta, tree[delta]))

            if i < len(prefix) - 1:
                flip = prefix[:i] + prefix[i + 1] + _ + prefix[i + 2 :]
                if flip in tree:
                    changes.add((flip, tree[flip]))

    changes = sorted(changes, key=lambda x: -x[1])

    change_count = max_count - len(comp) if max_count else None
    if change_count:
        result = [edit[0] for edit in changes[:change_count]]
    else:
        result = [edit[0] for edit in changes]

    return list(set(result + comp))[:max_count]


def word_filter(tree, pattern):
    """
    Return list of (word, freq) for all words in the given prefix tree that
    match pattern.  pattern is a string, interpreted as explained below:
          * matches any sequence of zero or more characters,
          ? matches any single character,
          otherwise char in pattern char must equal char in word.
    """
    stak = [(tree, "", pattern)]
    result = set()

    while stak:
        node, word, pat = stak.pop()
        if not pat:
            if node.value is not None:
                result.add((word, node.value))
            continue
        if pat[0] == "?":
            stak.extend(
                (child_node, word + char, pat[1:])
                for char, child_node in node.children.items()
            )
        elif pat[0] == "*":
            stak.append((node, word, pat[1:]))
            stak.extend(
                (child_node, word + char, pat)
                for char, child_node in node.children.items()
            )
        elif pat[0] in node.children:
            next_node = node.children[pat[0]]
            stak.append((next_node, word + pat[0], pat[1:]))
    return list(result)


# you can include test cases of your own in the block below.
if __name__ == "__main__":
    # with open("/Dracula.txt", encoding="utf-8") as f:
    #     text = f.read()
    # tre = word_frequencies(text)
    # print(sum(dict(tre).values()))
    # print(autocorrect(tre,'hear'))
    # print(autocomplete(tre,'gre', 6))
    doctest.testmod()
