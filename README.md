# STAR-CUBING

The Star- Cubing Algorithm explores both the top- down and bottom-up models.
The entire program is computed, and the algorithms are implemented in Python 3. 
I have implemented the star cubing algorithms in both small data sets and larger data sets that are present in “UCI Machine Learning repository” in order to test the memory efficiency and the time taken to execute the entire algorithm.
Star cubing algorithm in python requires four different components: data preprocessing, star table generation, star tree generation, and star cubing

Pseudocode:
starcubing(T, cnode)
If cnode.count >= threshold
   If cnode != root
     Print path to file
   If cnode not a leaf 
Cc = new copy of cnode
   Tc = new tree
   Append Tc to tree T’s neighbors 
If cnode is not a leaf
  Starcubing(T, cnode.child)
If Cc exists
   If cnode sibling exists
     Starcubing(T, cnode.sibling)
     
Remove reference to Tc from Tc’s parent tree
