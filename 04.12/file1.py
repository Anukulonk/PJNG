import random

category = ["Drink", "Food", "General", "Cloth"]

def Create_pd():
    N = random.randint(10, 15)
    products = []
    for i in range(1, N + 1):
        products.append({
            "id" : i,
            "name" : "PRODUCT" + str(i),
            "category" : random.choice(category),
            "price" : random.randint(10, 30)
        })
    return products

def show_pd(products):
    print("ID\tName\t\tCategory\tPrice")
    for s in products:
        print(f"{s["id"]}\t{s["name"]}\t{s["category"]}\t\t{s["price"]}")

def show2_pd(products):
    max_price = max({p['price'] for p in products})

    highest = []
    for p in products:
        if p['price'] == max_price:
            highest.append(p)

    highest.sort(key=lambda x : x['id'])

    print("\n----- MAX Price -----")
    print("ID\tName\t\tCategory\tPrice")
    for p in highest:
        print(f"{p['id']}\t{p['name']}\t{p['category']}\t\t{p['price']}")

    min_price = min({p['price'] for p in products})

    lowest = []
    for p in products:
        if p['price'] == min_price:
            lowest.append(p)

    lowest.sort(key=lambda x : x['id'])

    print("\n----- Min Price -----")
    print("ID\tName\t\tCategory\tPrice")
    for p in lowest:
        print(f"{p['id']}\t{p['name']}\t{p['category']}\t\t{p['price']}")

    for cat in category:
        g = []
        for p in products:
            if p['category'] == cat:
                g.append(p)
            if len(g) == 0:
                continue
        g.sort(key=lambda x : x['id'])

        print(f"\n{cat} = {len(g)}")
        print("ID\tName\t\tCategory\tPrice")
        for p in g:
            print(f"{p['id']}\t{p['name']}\t{p['category']}\t\t{p['price']}")
            
def process_pd(products):
    A = int(input("A : "))
    M = int(input("M : "))
    
    sales = {}
    nets = []
    
    for o in range(1, A + 1):
        print("\nORDER NO.",o)
        K = random.randint(1, M)
        order = [random.choice(products) for _ in range(K)]
        order.sort(key=lambda x: x["id"])
        print("ID\tNAME\t\tCATE\t\tPRICE")
        s = 0
        cnt = {}
        for item in order:
            print(f"{item["id"]}\t{item["name"]}\t{item["category"]}\t\t{item["price"]}")
            s += item["price"]
            pid = item["id"]
            cnt[pid] = cnt.get(pid, 0) + 1
            if pid not in sales:
                sales[pid] = {"name": item["name"], "category": item["category"], "price": item["price"], "qty":0}
            sales[pid]["qty"] += 1
            
        d = 0
        for pid in cnt:
            pair = cnt[pid] // 2
            d += pair * sales[pid]["price"] * 2 // 10
        net = s - d
        nets.append(net)
        print("Sum : ", s)
        print("Discount : ", d)
        print("Net : ", net)
    return sales, nets

def summary(sales, nets):
    best = max(sales.items(), key=lambda x : x[1]["qty"])
    print("\n----- 1. BEST SELLING -----")
    print("ID\tNAME\t\tCATE\t\tPRICE\t\tNUM")
    print(f"{best[0]}\t{best[1]["name"]}\t{best[1]["category"]}\t\t{best[1]["price"]}\t\t{best[1]["qty"]}")
    
    top = max(sales.items(), key=lambda x : x[1]["price"])
    print("\n----- 2. HIGHEST PRICE SOLD -----")
    print("ID\tNAME\t\tCATE\t\tPRICE\t\tNUM")
    print(f"{top[0]}\t{top[1]["name"]}\t{top[1]["category"]}\t\t{top[1]["price"]}\t\t{top[1]["qty"]}")
    
    total = sum(nets)
    avg = total / len(nets)
    print("\n----- 3. SUMMARY NET SALES -----")
    print("Sum = ", total, ", Count = ", len(nets), ", Average = %.2f" % avg )
    
def main():
    print("\n===== PART 1 =====")
    product = Create_pd()
    show_pd(product)
    show2_pd(product)
    print("\n===== PART 2 =====")
    sales, nets = process_pd(product)
    print("\n===== PART 3 =====")
    summary(sales, nets)
    
main()