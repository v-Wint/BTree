# B-tree implementation in Python

Searching inside each node is implemented using binary search

All the nodes are in memory using lists, readability is prioritized 
making this implementation a good demonstration of the algorithms involved

Deletion works by using one downward pass through the tree ensuring its properties, 
either just after the deletion, or before during the descent guaranteeing the child to have at least t keys

### Bibliography
Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). 
Introduction to Algorithms, fourth edition. MIT Press.