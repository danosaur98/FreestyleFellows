# FreeStyle Fellows Application 2018

Solution to the problem statement:

You are planning a party for an arbitrary number of people and you need to buy drinks and food. Assume you’re given a budget (integer) and 3 files: 'people.txt', 'drinks.txt', 'food.txt'.

'people.txt' contains an arbitrary number of people with their preferred drinks and food; each entry will be 3 lines long (1st line: name (not unique), 2nd line: drinks (comma delimited, not sorted), 3rd line: food (comma delimited, not sorted).

'drinks.txt' and 'food.txt' are arbitrarily large and each entry will be 1 line long in the following format: <drink or food name>:unit cost

Design and implement an algorithm that reads in the files and selects what drinks and foods you should purchase within your budget based on the information in the files. Be creative in how you optimize for food and drinks based on the known preferences.

Your answer should include an explanation of your algorithm, test cases, and a statement of all the assumptions you've made.

Feel free to use any data structures and packages or create your own. Submit all your files in a zipped directory (which can include a link to your GitHub repository of this challenge).

## Algorithmic Design
#Loading the Data
First, all the appropriate data is loaded. ```people``` is a list of all the guests (not used to solve the problem).
```drinks_popularity``` is a dictionary with each drink as a key and the total number of times its been requested as the respective value.
```drinks_cost``` is a dictionary with each drink as a key and its cost as the respective value.
```food_popularity``` and ```food_cost``` is the same as ```drinks_popularity``` and ```drinks_cost``` respectively, but for foods.

#Dynamic Programming
Since the question is recursive in nature with several repeated states, dynamic programming is used to optimize the solution.
Each entry in the memo table contains a data structure called ItemList, which contains the list of items, its total popularity, and total cost. This is to reduce the
time spent recomputing the total popularity and total cost every time an entry is revisited.

The budget is split into money spent on food and money spent on drinks. The current proportion of the budget spent on food is 75%, but this can be easily changed in the code.
An algorithm is performed separately on each budget.

A memo table is constructed for both drinks and foods. It is organized by item index for columns and the amount of money remaining for columns. For example,
```food_memo[2][4]``` would return the best case scenario for when you're examining the 2nd food item with $4 left.

## Assumptions

* Every item requested in people.txt is given a cost in either food.txt or drinks.txt
* Items are indistinguishable by upper/lowercase