# %%
from rapidfuzz.distance import Hamming, Levenshtein
from lorem_text import lorem

s1 = "world"
s2 = 'workd'

print(f"Levenshtein distance: {Levenshtein.distance(s1, s2)}")
print(f"Hamming distance: {Hamming.distance(s1, s2)}")

# %%
Hamming.distance("a", "ab", pad=False)
# %%
Levenshtein.distance("", "ab")
# %%
long_string = lorem.words(20).split(" ")
print(long_string)

# %%
import pygtrie

t = pygtrie.CharTrie()

for word in long_string:
    t[word] = True

print(t)

# exact match:
t["reallylongWord"] = True

assert t.has_key("reallylongWord") == True
assert t.has_key("reallylongWork") == False

def exact_match_trie(t, search_str):
    return t.has_key(search_str)

# %%
def hamming_distance_trie(trie, search_str, max_dist):
    def dfs(node, current_word, current_distance):
        if current_distance > max_dist:
            return
        
        if trie.has_key(current_word) and current_word != "":
            print(f"Word: {current_word}, Distance: {current_distance}")
        
        if not node.children:
            if len(current_word) == len(search_str) and current_distance <= max_dist:
                return True

            return False
        
        for char, child in node.children.items():
            print(char)
            new_distance = current_distance + (1 if len(current_word) < len(search_str) and char != search_str[len(current_word)] else 0)
            dfs(child, current_word + char, new_distance)
    
    dfs(trie._root, "", 0)

hamming_distance_trie(t, "undr", 1)

# %%
str_3 = "undr"
str_4 = "unsr"

t["a"] = True

assert hamming_distance_trie(t, "a", 0) == True
assert hamming_distance_trie(t, "b", 0) == False
assert hamming_distance_trie(t, "b", 1) == True

assert hamming_distance_trie(t, "ab", 1) == False
assert hamming_distance_trie(t, "ab", 2) == False

t["aba"] = True
assert hamming_distance_trie(t, "aaa", 2) == True

# %%
def levenshtein_distance_trie(trie, search_str, max_dist):
    pass

assert levenshtein_distance_trie(t, "earum", 0) == True
assert levenshtein_distance_trie(t, "earum", 1) == True
assert levenshtein_distance_trie(t, "earu", 1) == True
assert levenshtein_distance_trie(t, "earu", 0) == False

assert levenshtein_distance_trie(t, "earsk", 2) == True
assert levenshtein_distance_trie(t, "Aarsk", 3) == False
# %%
for char, child in node.children.items():