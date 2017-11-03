# ASSUMPTIONS:
# foods are not distinct by capital and lower case values
# every drink/food requested in people.txt is found in drinks.txt/food.txt


class ItemList(object):
    def __init__(self, item_list, popularity, cost):
        self.item_list = item_list
        self.popularity = popularity
        self.cost = cost

    def __str__(self):
        return str(self.item_list) + "\nTotal Popularity: " + str(self.popularity) + "\nCost: " + str(self.cost)


def compute_popularity(item_list, popularity):
    total = 0
    for item in item_list:
        total += popularity[item]
    return total


def compute_cost(item_list, cost):
    total = 0
    for item in item_list:
        total += cost[item]
    return total


# load all the data
with open('people.txt') as p:
    people_raw = p.readlines()
people_raw = [x.strip() for x in people_raw]

with open('drinks.txt') as d:
    drinks_raw = d.readlines()
drinks_raw = [x.strip() for x in drinks_raw]

with open('food.txt') as f:
    food_raw = f.readlines()
food_raw = [x.strip() for x in food_raw]

# extracts information for list of people, and the popularity of each drink and foods
people = []
drinks_popularity = {}
food_popularity = {}
count = 0
for line in people_raw:
    if count % 3 == 0:
        people.append(line)
    elif count % 3 == 1:
        drinks = [x.lower() for x in line.split(",")]
        for drink_entry in drinks:
            if drink_entry not in drinks_popularity:
                drinks_popularity[drink_entry] = 0
            drinks_popularity[drink_entry] = drinks_popularity[drink_entry] + 1
    else:
        food = [x.lower() for x in line.split(",")]
        for food_entry in food:
            if food_entry not in food_popularity:
                food_popularity[food_entry] = 0
            food_popularity[food_entry] = food_popularity[food_entry] + 1
    count += 1

# extracts cost for drinks
drinks_cost = {}
for line in drinks_raw:
    drinks_cost[line.split(":")[0].lower()] = int(line.split(":")[1])

# extracts cost for foods
food_cost = {}
for line in food_raw:
    food_cost[line.split(":")[0].lower()] = int(line.split(":")[1])

# budget given
budget = 12

# splits budget into money spent on food and drink
budget_food_proportion = 0.75
food_budget = int(budget_food_proportion * budget)
drinks_budget = budget - food_budget

food_memo = [[[] for fcol in range(food_budget + 1)] for frow in range(len(food_popularity) + 1)]
drinks_memo = [[[] for dcol in range(drinks_budget + 1)] for drow in range(len(drinks_popularity) + 1)]
food_list = list(food_popularity.keys())
drinks_list = list(drinks_popularity.keys())


# dynamic programming method to optimize popularity and cost
def optimize(item_type, index, budget_remaining):
    if item_type == "food":
        memo = food_memo
        popularity = food_popularity
        cost = food_cost
        l = food_list
    else:
        memo = drinks_memo
        popularity = drinks_popularity
        cost = drinks_cost
        l = drinks_list

    if index == len(
            popularity) or budget_remaining == 0:  # if all the items have been examined or all the money has been spent, return an empty list
        return ItemList([], 0, 0)
    elif memo[index][budget_remaining]:  # if we have previously visited this case, return the answer
        return memo[index][budget_remaining]
    elif cost[l[index]] > budget_remaining:  # if this item costs too much, skip it
        memo[index][budget_remaining] = optimize(item_type, index + 1, budget_remaining)
        return memo[index][budget_remaining]
    else:  # if this item fits in our budget, see whether it's better to buy the item or not depending on which option yields a higher popularity
        ignore = optimize(item_type, index + 1, budget_remaining).popularity
        bought = optimize(item_type, index + 1, budget_remaining - cost[l[index]])
        if cost[l[index]] < budget_remaining - bought.cost:
            bought.item_list.append(l[index])
            bought.popularity = compute_popularity(bought.item_list, popularity)
            bought.cost = compute_cost(bought.item_list, cost)
        buy = bought.popularity

        if ignore >= buy:
            memo[index][budget_remaining] = optimize(item_type, index + 1, budget_remaining)
        else:
            memo[index][budget_remaining] = bought

        return memo[index][budget_remaining]


print(optimize("food", 0, food_budget))
