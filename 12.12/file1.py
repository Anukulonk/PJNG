import random

category = ["Book", "Stationery", "Office", "Gift"]

def createpd():
    N = random.randint(10, 15)
    products = []
    for i in range(1, N + 1):
        products.append({
            "id" : i,
            "name" : "ITEM" + str(i),
            "category" : random.choice(category),
            "price" : random.randint(50, 300)
        })
    return products

def show1(products):
    print("ID\tName\t\tCategory\tPrice")
    for s in products:
        print(f"{s['id']}\t{s['name']}\t\t{s['category']}\t\t{s['price']}")

def show2(products):
    max_price = max({p['price'] for p in products})

    highest = []
    for p in products:
        if p['price'] == max_price:
            highest.append(p)

    highest.sort(key=lambda x : x['id'])

    print("\n----- MAX Price -----")
    print("ID\tName\t\tCategory\tPrice")
    for p in highest:
        print(f"{p['id']}\t{p['name']}\t\t{p['category']}\t\t{p['price']}")

    min_price = min({p['price'] for p in products})

    lowest = []
    for p in products:
        if p['price'] == min_price:
            lowest.append(p)

    lowest.sort(key=lambda x: x['id'])

    print("\n----- MIN Price -----")
    print("ID\tName\t\tCatagory\tPrice")
    for p in lowest:
        print(f"{p['id']}\t{p['name']}\t\t{p['category']}\t\t{p['price']}")

    for cat in category:
        g = []
        for p in products:
            if p['category'] == cat:
                g.append(p)
            if len(g) == 0:
                continue
        g.sort(key=lambda x : x['id'])

        print(f"\n{cat} = {len(g)}")
        print("ID\tName\t\tCatagory\tPrice")
        for p in g:
            print(f"{p['id']}\t{p['name']}\t\t{p['category']}\t\t{p['price']}")
        
def process(products):
    A = int(input("A : "))
    M = int(input("M : "))

    sales = {}
    nets = []

    for o in range(1, A + 1):
        print("\nORDER NO.", o)
        K = random.randint(1, M)
        order = [random.choice(products) for _ in range(K)]
        order.sort(key=lambda x: x['id'])
        print("ID\tNAME\t\tCATE\t\tPRICE")
        s = 0
        cnt = {}
        for t in order:
            print(f"{t['id']}\t{t['name']}\t\t{t['category']}\t\t{t['price']}")
            s += t['price']
            pid = t['id']
            cnt[pid] = cnt.get(pid, 0) + 1
            if pid not in sales:
                sales[pid] = {"name": t['name'], "category": t['category'], "price": t['price'], "qty":0}
            sales[pid]["qty"] += 1

        d = 0
        for pid in cnt:
            pair = cnt[pid] // 3
            d += pair * sales[pid]['price'] * 3 // 15
        net = s - d
        nets.append(net)
        print("Sum : ", s)
        print("Discount : ", d)
        print("Net : ", net)
    return sales, nets

def summary(sales, nets):
    b = max(sales.items(), key=lambda x : x[1]['qty'])
    print("\n----- 1. Best Selling -----")
    print("ID\tNAME\t\tCATE\t\tPRICE\t\tNUM")
    print(f"{b[0]}\t{b[1]['name']}\t\t{b[1]['category']}\t\t{b[1]['price']}\t\t{b[1]['qty']}")

    top = max(sales.items(), key=lambda x : x[1]['qty'])
    print("\n----- 2. Highest Price Sold -----")
    print("ID\tNAME\t\tCATE\t\tPRICE\t\tNUM")
    print(f"{top[0]}\t{top[1]['name']}\t\t{top[1]['category']}\t\t{b[1]['price']}\t\t{top[1]['qty']}")

    total = sum(nets)
    avg = total / len(nets)
    print("\n----- 3. Summary Net Sales -----")
    print("Sum = ", total, ", Count = ", len(nets), ", Average = %.2f" % avg)

def main():
    print("\n===== PART 1 =====")
    products = createpd()
    show1(products)
    show2(products)
    print("\n===== PART 2 =====")
    sales, nets = process(products)
    print("\n===== PART 3 =====")
    summary(sales, nets)

main()
