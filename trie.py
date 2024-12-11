# %%
import collections
import numpy as np

import logging
logging.basicConfig(level=logging.DEBUG)


class TrieNode:
    def __init__(self):
        self.children = collections.defaultdict(TrieNode)
        self.is_end = False
        self.doc_ids = set()
        

class Trie:    
    def __init__(self):
        self.root = TrieNode()
        self.empty_set = set() # so that it only gets instantiated once.
    
    def insert(self, word: str, doc_id) -> None:
        current = self.root
        for letter in word:
            current = current.children[letter]
        current.is_end = True
        current.doc_ids.add(doc_id)
        
    def exact_search(self, word: str) -> bool:
        current = self.root
        for letter in word:
            current = current.children.get(letter)
            if current is None:
                return self.empty_set
        return current.doc_ids
    
    # todo maybe switch back to exact search if max_dist is 0?
    def hamming_search(self, word:str, max_dist:int = 0) -> bool:
        doc_matches = set()
        def dfs(node, current_word, current_distance):
            logging.debug(f"Visiting node: {current_word}, current_distance: {current_distance}")
            if current_distance > max_dist:
                return self.empty_set
            
            if node.is_end:
                if len(current_word) == len(word) and current_distance <= max_dist:
                    logging.debug(f"Found word: {current_word} with distance: {current_distance}")
                    return node.doc_ids

            if len(current_word) >= len(word):
                return self.empty_set
            
            for char, child in node.children.items():
                next_letter_matches = (char == word[len(current_word)])
                new_distance = current_distance + (1 if not next_letter_matches else 0)

                current_results = dfs(child, current_word + char, new_distance)
                if current_results:
                    doc_matches.update(current_results)
                
            return doc_matches
        
        return dfs(self.root, "", 0)
    
    # todo maybe switch back to exact search if max_dist is 0?
    def levshetin_search(self, word:str, max_dist:int = 0) -> bool:
        def dfs(node, current_word, current_distance):
            logging.debug(f"Visiting node: {current_word}, current_distance: {current_distance}")
            if current_distance > max_dist:
                return False
            
            if node.is_end:
                length_diff = abs(len(current_word) - len(word))
                end_node_distance = current_distance + length_diff

                if end_node_distance <= max_dist:
                    return True
            
            for char, child in node.children.items():
                logging.debug(f"Char: {char}, Current Word: {current_word}, Current Distance: {current_distance}")

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
        current = self.root 
        
        for letter in prefix:
            current = current.children.get(letter)
            if not current:
                return False
        
        return True