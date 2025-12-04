import random

category = ["Drink", "Food", "General", "Cloth"]

def create():
    N = random.randint(10, 15)
    products = []
    for i in range(1, N+1):
        products.append({
            "id": i,
            "name": "PRODUCT" + str(i),
            "category": random.choice(category),
            "price": random.randint(10, 30),
        })
    return products
def show_pd(products):
    print("ID\tNAME\tCATEGORY\tPRICE")
    for p in products:
        print(p["id"], p["name"], p["category"], p["price"])
    
def process_order(products):
    A = int(input("A : "))
    M = int(input("M : "))
    sales = {}
    nets = []
    for o in range(1, A+1):
        print("\nORDER NO.", o)
        K = random.randint(1, M)
        order = [random.choice(products) for _ in range(K)]
        order.sort(key=lambda x: x["id"])
        print("ID\t\tNAME\t\tCATE\tPRICE")
        s = 0
        cnt = {}
        for item in order:
            print(f"{item['id']}\t\t{item['name']}\t{item['category']}\t{item['price']}")
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
            
        net = s-d
        nets.append(net)
        
        print("Sum = ", s)
        print("Discount = ", d)
        print("Net = ", net)
    return sales, nets
    
def summary(sales, nets):
    best = max(sales.items(), key=lambda x: x[1]["qty"])
    
    print("\n1. BEST SELLING")
    print("ID\t\t NAME\t\tCATE\t\tPRICE\t\tNUM")
    print(best[0], best[1]["name"], best[1]["category"], best[1]["price"], best[1]["qty"])
    
    top = max(sales.items(), key=lambda x: x[1]["price"])
    
    print("\n2. HIGHEST PRICE SOLD")
    print("ID\t\tNAME\t\tCATE\t\tPRICE\t\tNUM")
    print(top[0], top[1]["name"], top[1]["category"], top[1]["price"], top[1]["qty"])
    
    total = sum(nets)
    avg = total / len(nets)
    print("\n3. SUMMARY NET SALES")
    print("Sum = ", total, ", Count = ", len(nets), ", Average = %.2f" % avg)
    
def main():
    print("\n=== PART 1 ===")
    products = create()
    show_pd(products)
    print("\n=== PART 2 ===")
    sales, nets = process_order(products)
    print("\n=== PART 3 ===")
    summary(sales, nets)
main()