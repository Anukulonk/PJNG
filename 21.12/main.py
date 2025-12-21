import random

category = ["Drink", "Food", "General", "Cloth"]
shops = ["S01", "S02", "S03", "S04", "S05"]

SEED = int(input("Seed : "))
CAP_DAY = int(input("CAP DAY : "))
CAP_SHOP = int(input("CAP SHOP : "))
A = int(input("A : "))

rng = random.Random(SEED)

def createpd():
    N = rng.randint(15, 25)
    products = []
    for i in range(1, N + 1):
        p_cate = rng.choice(category)
        p_shop = "S%02d" % rng.randint(1,5)
        p_price = rng.randint(10, 300)
        p_stock = rng.randint(1, 20)
        
        products.append({
            'id' : i,
            'code' : f'P{i:03d}',
            'category' : p_cate,
            'shop' : p_shop,
            'price' : p_price,
            'stock' : p_stock,
            'sold_qty' : 0,
            'net_revenue' : 0,
            'gov_used_sum' : 0
        })
    return products

def show1(products):
    print('CODE\tCATE\tSHOP\tPRICE\tSTK')
    for s in products:
        print(f"{s['code']}\t{s['category']}\t{s['shop']}\t{s['price']}\t{s['stock']}")
        
def show2(products):
    print("\n===== PART 1 =====")
    print("\n----- 1. Max Price of Category -----")
    for cat in category:
        g = [p for p in products if p['category'] == cat]
        if g:
            g.sort(key=lambda x: (-x['price'], x['code']))
            p = g[0]
            print(f"Max {cat:8} : {p['code']} | Price : {p['price']}")
    
    print("\n----- 2. Cheapest Price -----")
    temp = products[:]
    temp.sort(key=lambda x: (x['price'], x['shop'], x['code']))
    cheapest = temp[0]
    print(f"Cheapest : {cheapest['code']} | Shop : {cheapest['shop']} | Price {cheapest['price']}")
    
    print("\n----- 3. Category Count -----")
    for cat in category:
        g = [p for p in products if p['category'] == cat]
        g.sort(key=lambda x:x['code'])
        print(f"Category {cat} ({len(g)} items) : ")
        for p in g:
            print(f" {p['code']} | {p['price']} THB")
    
    print("\n----- 4. Shop Summary -----")
    print("Shop Summary : ")
    for s in shops:
        s_items = [p for p in products if p['shop'] == s]
        val = sum(p['price'] * p['stock'] for p in s_items)
        print(f" {s} : Items : {len(s_items)} | Stock : {sum(p['stock'] for p in s_items)} | Value : {val}")
        
def simul(products):
    print("\n===== PART 2 =====")
    bills = []
    
    for cust_no in range(1, A + 1):
        K = rng.randint(1, 10)
        capl_day = CAP_DAY
        capl_shop = {s: CAP_SHOP for s in shops}
        
        cart = []
        for _ in range(K):
            pid = rng.randint(1, len(products))
            target = products[pid-1]
            
            if target['stock'] <= 0:
                opts = [p for p in products if p['shop'] == target['shop'] and p['category'] == target['category'] and p['stock'] > 0]
                if opts:
                    opts.sort(key=lambda x: (x['price'], x['code']))
                    target = opts[0]
                else:
                    target = None
                    
            if target:
                gov_base = target['price'] // 2
                gov_paid = min(gov_base, capl_day, capl_shop[target['shop']])
                CustPay = target['price'] - gov_paid
                
                target['stock'] -= 1
                capl_day -= gov_paid
                capl_shop[target['shop']] -= gov_paid
                
                cart.append({
                    'shop': target['shop'],
                    'code' : target['code'],
                    'cate' : target['category'],
                    'price' : target['price'],
                    'gov' : gov_paid,
                    'cust' : CustPay,
                    'ref' : target
                })
        cart.sort(key=lambda x: (x['shop'], x['code']))
        print(f"\nCUSTOMER NO.{cust_no}")
        print(f"{'SHOP':5} | {'CODE':5} | {'CATE':10} | {'PRICE':5} | {'GOV':5} | {'CUST'}")
        
        bill_gross, bill_gov, bill_disc = 0,0,0
        shop_group = {}
        for item in cart:
            shop_group.setdefault(item['shop'], []).append(item)
            
        for s_id, items in shop_group.items():
            pre_disc_pay = sum(it['cust'] for it in items)
            promo = 0
            if len(items) >= 3:
                promo = int(pre_disc_pay * 0.05)
                
            bill_disc += promo
            for it in items:
                print(f"{it['shop']:5} | {it['code']:5} | {it['cate']:10} | {it['price']:5} | {it['gov']:5} | {it['cust']}")
                bill_gross += it['price']
                bill_gov += it['gov']
                
            share = it['cust'] / pre_disc_pay if pre_disc_pay > 0 else 0
            it['ref']['sold_qty'] += 1
            it['ref']['gov_used_sum'] += it['gov']
            it['ref']['net_revenue'] += (it['cust']) - (promo * share)
            
    net = bill_gross - bill_gov - bill_disc
    print(f"GROSS : {bill_gross}, GOV : {bill_gov}, DISC : {bill_disc}, NET : {net}")
    print(f'CAP LEFT : DAY : {capl_day} | ' + ', '.join([f'{s}:{capl_shop[s]}' for s in shops]))
    
    bills.append({
        'id' : cust_no,
        'gross' : bill_gross,
        'gov' : bill_gov,
        'disc' : bill_disc,
        'net' : net
    })
    return bills

def show_Analytics(products, bills):
    print("\n===== PART 3 =====")
    print("----- 1. Top 3 Best Selling -----")
    products.sort(key=lambda x: (-x['sold_qty'], x['code']))
    for i in range(min(3, len(products))):
        p = products[i]
        print(f"Top{i+1} : {p['code']} | Qty : {p['sold_qty']} | Gov : {p['gov_used_sum']}")
    s_stats = []
    for s in shops:
        gov = sum(p['gov_used_sum'] for p in products if p['shop'] == s)
        s_stats.append({
            'shop' : s,
            'gov' : gov
        })
    print("\n----- 2. Top 2 GovTotal -----")
    s_stats.sort(key=lambda x: (-x['gov'], x['shop']))
    for i in range(min(2, len(s_stats))):
        st = s_stats[i]
        print(f"ShopRank{i+1} : {st['shop']} | Gov : {st['gov']}")
        
    print("\n----- 3. Best Saver -----")
    if bills:
        for b in bills:
            b['rate'] = b['gov'] / b['gross'] if b['gross'] > 0 else 0
        bills.sort(key=lambda x: (-x['rate'], x['id']))
        best =bills[0]
        print(f"Best Saver : Cust {best['id']} | Rate : {best['rate']:.4f}")
    
    print("\n----- 4. Low Stock -----")
    low = sorted([p for p in products if p['stock'] <= 2], key=lambda x: (x['stock'], x['shop'], x['code']))
    for p in low:
        print(f"Low Stock : {p['code']} | Shop : {p['shop']} | Left : {p['stock']}")
        
    tg, tgov, td, tn = sum(b['gross'] for b in bills), sum(b['gov'] for b in bills), sum(b['disc'] for b in bills), sum(b['net'] for b in bills)
    print(f"\nIntegrity : Gross {tg} | Gov {tgov} | Disc {td} | Net {tn}")
    print(f"Match : {tg - tgov - td == tn}")

def main():
    products = createpd()
    show1(products)
    show2(products)
    bills = simul(products)
    show_Analytics(products, bills)
    
main()