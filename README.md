# FreeStyle Fellows Application 2018
##Github Link:
https://github.com/danosaur98/FreestyleFellows

### Problem statement:

You are planning a party for an arbitrary number of people and you need to buy drinks and food. Assume you’re given a budget (integer) and 3 files: 'people.txt', 'drinks.txt', 'food.txt'.

'people.txt' contains an arbitrary number of people with their preferred drinks and food; each entry will be 3 lines long (1st line: name (not unique), 2nd line: drinks (comma delimited, not sorted), 3rd line: food (comma delimited, not sorted).

'drinks.txt' and 'food.txt' are arbitrarily large and each entry will be 1 line long in the following format: drink or food name:unit cost

Design and implement an algorithm that reads in the files and selects what drinks and foods you should purchase within your budget based on the information in the files. Be creative in how you optimize for food and drinks based on the known preferences.

Your answer should include an explanation of your algorithm, test cases, and a statement of all the assumptions you've made.

Feel free to use any data structures and packages or create your own. Submit all your files in a zipped directory (which can include a link to your GitHub repository of this challenge).

# Algorithmic Design
##Loading the Data
First, all the appropriate data is loaded. ```people``` is a list of all the guests (not used to solve the problem).
```drinks_popularity``` is a dictionary with each drink as a key and the total number of times it has been requested as the respective value.
```drinks_cost``` is a dictionary with each drink as a key and its cost as the respective value.
```food_popularity``` and ```food_cost``` is the same as ```drinks_popularity``` and ```drinks_cost``` respectively, but for foods.
```drinks_list``` and ```foods_list``` are the keys of their respective popularity dictionaries formatted as a list. This is to index each item, since you can't access dictionary keys by index. 

##Dynamic Programming
Since the question is recursive in nature with several repeated states, dynamic programming is used to optimize the solution.

The budget is split into money spent on food and money spent on drinks. The current proportion of the budget spent on food is 75%, but this can be easily changed in the code.
The algorithm is performed separately on each budget. It is optimized so that if there is leftover money from buying all the food items,
it is added to the drinks budget.

A memo table is constructed for both drinks and foods. It is organized by item index for columns and the amount of money remaining for columns. For example,
```food_memo[2][4]``` would return the best case scenario for examining the 2nd food item in the list with $4 left.

The method ```optimize``` takes in 3 parameters: ```item_type```, which is either drinks or foods,```index```,
which is the index of the item list we are currently examining, and ```budget_remaining```, which is the amount of money we have left to spend.
There are four possible outcomes:
1. If all the items have been examined or all the money has been spent (```index=len(l)```, or 
```budget_remaining==0```), return an empty list with cost and popularity 0.
2. If the best situation for this item index and budget remaining has already been calculated 
(```memo[index, budget_remaining]!= 0```), return it.
3. If the cost of the item exceeds the budget remaining (```cost[l[index]] > budget_remaining```), skip this item and check the next item. 
4. If the cost of the item doesn't exceed the budget remaining, choose the more favorable outcome of ignoring or buying it.


Each entry in the memo table takes O(1) time to calculate. There are n*B possible states, where n is the total number of items in the list and 
B is the budget given. Thus, the worst case time complexity of the algorithm is O(Bn).

## Assumptions
* Every item requested in people.txt is given a cost in either food.txt or drinks.txt.
* Items are indistinguishable by upper/lowercase.
* Costs are integers.

## Test Cases
### Input
Budget = 16.


people.txt:
```
P1
water,milk,soda
pizza,chips,cake
P2
water,orange juice
chips,cake,pizza
P3
water,beer
cookies,cupcakes,pizza
```
food.txt:
```
pizza:10
chips:4
cake:5
cookies:1
cupcakes:1
```
drinks.txt:
```
water:1
milk:2
soda:3
beer:5
orange juice:2
```
### Output
```
Food Bought: ['chips', 'cake', 'cookies', 'cupcakes']
Drinks Bought: ['water', 'milk', 'orange juice']
```
### Explanation
```
Food Popularity: {'pizza': 3, 'chips': 2, 'cake': 2, 'cookies': 1, 'cupcakes': 1}
Food Cost: {'pizza': 10, 'chips': 4, 'cake': 5, 'cookies': 1, 'cupcakes': 1}
Food Budget: 12
```
Although pizza is the most popular of all the food items, the maximum total popularity including pizza would be 5 after buying
pizza, cookies, and cupcakes. However, the highest total popularity of all possible sets is 6 after buying chips, cake, cookies, and cupcakes.
Since the total cost was only 11 and the food budget was 12, the extra dollar is added to the drinks budget.

```
Drinks Popularity: {'water': 3, 'milk': 1, 'soda': 1, 'orange juice': 1, 'beer': 1}
Drinks Cost: {'water': 1, 'milk': 2, 'soda': 3, 'beer': 5, 'orange juice': 2}
Drinks Budget:5
```
The highest total popularity is 6 after buying water, milk, and orange juice. 