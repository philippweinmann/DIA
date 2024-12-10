# %%
import collections
import numpy as np

class TrieNode:
    def __init__(self):
        self.children = collections.defaultdict(TrieNode)
        self.is_end = False
        

class Trie:    
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        """
        Inserts a word into the trie.
        """
        current = self.root
        for letter in word:
            current = current.children[letter]
        current.is_end = True    
        
    def exact_search(self, word: str) -> bool:
        """
        Returns if the word is in the trie.
        """
        current = self.root
        for letter in word:
            current = current.children.get(letter)
            if current is None:
                return False
        return current.is_end
    
    def hamming_search(self, word:str, max_dist:int) -> bool:
        """
        Returns if there is any word in the trie that is within the hamming distance of the given word.
        """
        def dfs(node, current_word, current_distance):
            # print(f"Visiting node: {current_word}, current_distance: {current_distance}")
            if current_distance > max_dist:
                return False
            
            if node.is_end:
                if len(current_word) == len(word) and current_distance <= max_dist:
                    # print(f"Found word: {current_word} with distance: {current_distance}")
                    return True

            if len(current_word) >= len(word):
                return False
            
            for char, child in node.children.items():
                next_letter_matches = (char == word[len(current_word)])
                new_distance = current_distance + (1 if not next_letter_matches else 0)

                if dfs(child, current_word + char, new_distance):
                    return True
                
            return False
        
        return dfs(self.root, "", 0)
    
    def levshetin_search(self, word:str, max_dist:int) -> bool:
        """
        Returns if there is any word in the trie that is within the levshetin distance of the given word.
        """
        def dfs(node, current_word, current_distance):
            print(f"Visiting node: {current_word}, current_distance: {current_distance}")
            if current_distance > max_dist:
                return False
            
            if node.is_end:
                length_diff = abs(len(current_word) - len(word))
                end_node_distance = current_distance + length_diff

                if end_node_distance <= max_dist:
                    return True
            
            for char, child in node.children.items():
                print(f"Char: {char}, Current Word: {current_word}, Current Distance: {current_distance}")

                if len(current_word + char) > len(word):
                    next_letter_matches = False
                elif char == word[len(current_word)]:
                    next_letter_matches = True
                else:
                    next_letter_matches = False

                new_distance = current_distance + (1 if not next_letter_matches else 0)

                if dfs(child, current_word + char, new_distance):
                    return True
                
            return False
        
        return dfs(self.root, "", 0)
    
    def startsWith(self, prefix: str) -> bool:
        """
        Returns if there is any word in the trie that starts with the given prefix.
        """
        current = self.root 
        
        for letter in prefix:
            current = current.children.get(letter)
            if not current:
                return False
        
        return True
    
trie = Trie()
strings = ["apple", "app", "ap", "applesauce", "banana", "bananas", "bananarama", "bananaramas"]

for string in strings:
    trie.insert(string)

print(trie)

assert trie.exact_search("apple") == True
assert trie.exact_search("app") == True
assert trie.exact_search("NotExistent") == False
# %%
# alright works for exact match, now let's try hamming distance

assert trie.hamming_search("apple", 0) == True
assert trie.hamming_search("apple", 1) == True

assert trie.hamming_search("applr", 0) == False
assert trie.hamming_search("applr", 1) == True
assert trie.hamming_search("applr", 2) == True
# %%
# okay now levshetin distance
assert trie.levshetin_search("apple", 0) == True
assert trie.levshetin_search("apple", 1) == True
assert trie.levshetin_search("applr", 0) == False
assert trie.levshetin_search("applr", 1) == True
assert trie.levshetin_search("applr", 2) == True

assert trie.levshetin_search("appl", 1) == True

assert trie.levshetin_search("appl", 0) == False
assert trie.levshetin_search("rppl", 2) == True
assert trie.levshetin_search("rppl", 3) == True

# %%
