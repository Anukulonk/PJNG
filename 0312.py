import random

category = ["Drink", "Food", "General", "Cloth"]

n = random.randint(10, 15)

print(n)

products = []
for i in range(1, n+1):
    product = {
        "id" : i,
        "name" : f"PRODUCT{i}",
        "category" : random.choice(category),
        "price" : random.randint(10, 30)
    }
    products.append(product)

for p in products:
    print(f"{p['id']}\t\t{p['name']}\t\t{p['category']}\t\t{p['price']}")

max_price = max({p['price'] for p in products})

highest = []
for p in products:
    if p['price'] == max_price:
        highest.append(p)

highest.sort(key=lambda x : x['id'])

print("MAX Price")
for p in highest:
    print(f"{p['id']}\t\t{p['name']}\t\t{p['category']}\t\t{p['price']}")

min_price = min({p['price'] for p in products})

lowest = []
for p in products:
    if p['price'] == min_price:
        lowest.append(p)

lowest.sort(key=lambda x : x['id'])

print("Min Price")
for p in lowest:
    print(f"{p['id']}\t\t{p['name']}\t\t{p['category']}\t\t{p['price']}")

for cat in category:
    g = []
    for p in products:
        if p['category'] == cat:
            g.append(p)
        if len(g) == 0:
            continue
    g.sort(key=lambda x : x['id'])

    print(f"{cat} = {len(g)}")
    for p in g:
        print(f"{p['id']}\t\t{p['name']}\t\t{p['category']}\t\t{p['price']}")

A = int(input())
M = int(input())

for order in range(1, A+1):
    print(f"ORDER_NO", order)

    K = random.randint(1, M)

    order_items = []
    for i in range(K):
        p = random.choice(products)
        order_items.append(p)

    order_items.sort(key=lambda x : x['id'])

    sum_price = 0

    counts = {}
    for item in order_items:
        print(item["id"], item["name"], item["category"], item["price"])
        sum_price += item["price"]

        pid = item["id"]
        if pid not in counts:
            counts[pid] = {"price": item["price"], "qty": 0}
        counts[pid] ["qty"] += 1

    discount = 0
    for pid in counts:
        price = counts[pid] ["price"]
        qty = counts[pid]["qty"]
        pair = qty // 2
        discount += pair * price *2 // 10
    net = sum_price - discount

    print("Sum =", sum_price)
    print("Discount =", discount)
    print("Net =", net)