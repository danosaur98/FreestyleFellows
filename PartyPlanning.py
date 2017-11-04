# dynamic programming method to optimize popularity and cost
def optimize(item_type, index, budget_remaining):
    if item_type == "food":
        memo = food_memo
        popularity = food_popularity
        cost = food_cost
        booleans = food_booleans
        l = food_list
    else:
        memo = drinks_memo
        popularity = drinks_popularity
        cost = drinks_cost
        l = drinks_list
        booleans = drinks_booleans

    if index == len(
            l) or budget_remaining == 0:  # if all the items have been examined or all the money has been spent, return an empty list
        return 0
    elif memo[index][budget_remaining]:  # if we have previously visited this case, return the answer
        return memo[index][budget_remaining]
    elif cost[l[index]] > budget_remaining:  # if this item costs too much, skip it
        memo[index][budget_remaining] = optimize(item_type, index + 1, budget_remaining)
        return memo[index][budget_remaining]
    else:  # if this item fits in our budget, see whether it's better to buy the item or not depending on which option yields a higher popularity
        ignore = optimize(item_type, index + 1, budget_remaining)
        buy = popularity[l[index]] + optimize(item_type, index + 1, budget_remaining - cost[l[index]])
        if buy > ignore:
            booleans[index][budget_remaining] = True
            memo[index][budget_remaining] = buy
        else:
            memo[index][budget_remaining] = ignore

        return memo[index][budget_remaining]


def get_items(item_type):
    if item_type == "food":
        memo = food_memo
        popularity = food_popularity
        cost = food_cost
        l = food_list
        booleans = food_booleans
        budget = food_budget
    else:
        memo = drinks_memo
        popularity = drinks_popularity
        cost = drinks_cost
        l = drinks_list
        booleans = drinks_booleans
        budget = drinks_budget
    ret = []
    total_cost = 0
    for i in range(0, len(l)):
        if booleans[i][budget] == True:
            ret.append(l[i])
            budget -= cost[l[i]]
            total_cost += cost[l[i]]
    return [ret, total_cost]

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
budget = 16
# splits budget into money spent on food and drink
budget_food_proportion = .75

food_budget = int(budget_food_proportion * budget)
food_memo = [[[] for fcol in range(food_budget + 1)] for frow in range(len(food_popularity) + 1)]
food_list = list(food_popularity.keys())
food_booleans = [[False for x in range(food_budget + 1)] for y in range(len(food_popularity) + 1)]

print("Food Popularity: " + str(food_popularity))
print("Food Cost: " + str(food_cost))
print("Food Budget: " + str(food_budget))

food_result = optimize("food", 0, food_budget)
print("Food Popularity: " + str(food_result))
food_bought, food_cost = get_items("food")
print("Food Bought: " + str(food_bought))
print("Food Cost: " + str(food_cost))

drinks_budget = budget - food_cost # if there is extra budget left from food, add it to the drink budget
drinks_memo = [[[] for dcol in range(drinks_budget + 1)] for drow in range(len(drinks_popularity) + 1)]
drinks_list = list(drinks_popularity.keys())
drinks_booleans = [[False for i in range(drinks_budget + 1)] for j in range(len(drinks_popularity) + 1)]

print("Drinks Popularity: " + str(drinks_popularity))
print("Drinks Cost: " + str(drinks_cost))
print("Drinks Budget: " + str(drinks_budget))

drinks_result = optimize("drinks", 0, drinks_budget)
print("Drinks Popularity: " + str(food_result))
drinks_bought, drinks_cost = get_items("drinks")
print("Drinks Bought: " + str(drinks_bought))
print("Drinks Cost: " + str(drinks_cost))
