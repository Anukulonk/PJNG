import random

category = ['Drink', 'Food', 'General', 'Cloth']
shops = ['S01', 'S02', 'S03', 'S04', 'S05']

def createpd():
    N = random.randint(15,25)
    products = []
    for i in range(1, N + 1):
        products.append({
            'id' : i,
            'code' : f'P{i:03d}',
            'category' : random.choice(category),
            'shop' : random.choice(shops),
            'price' : random.randint(10, 300),
            'stock' : random.randint(1, 20),
            'sold_qty' : 0,
            'net_revenue' : 0,
            'gov_used_sum' : 0,
        })
    return products

def show1(products):
    print('ID\tCODE\tCATE\tSHOP\tPRC\tSTK')
    for s in products:
        print(f'{s['id']}\t{s['code']}\t{s['category']}\t{s['shop']}\t{s['price']}\t{s['stock']}')

def show2(products):
    print('\n===== PART 1 =====')
    for cat in category:
        g = [p for p in products if p['category'] == cat]
        if g:
            g.sort(key=lambda x: (-x['price'], x['code']))
            p = g[0]
            print(f"Max {cat:8} : {p['code']} | Price : {p['price']}")
            
    temp = products[:]
    temp.sort(key=lambda x: (x['price'], x['shop'], x['code']))
    cheapest = temp[0]
    print(f"\nCheapest : {cheapest['code']} |  Shop : {cheapest['shop']} | Price : {cheapest['price']}")

    for cat in category:
        g = [p for p in products if p['category'] == cat]
        g.sort(key=lambda x: x['code'])
        print(f"\nCategory {cat} ({len(g)} items) : ")
        for p in g:
            print(f" {p['code']} | {p['price']} THB")
            
    print('\nShop Sammary : ')
    for s in shops:
        s_items = [p for p in products if p['shop'] == s]
        val = sum(p['price'] * p['stock'] for p in s_items)
        print(f" {s}: Items : {len(s_items)} | Stock : {sum(p['stock'] for p in s_items)} | Value : {val}")
        
def simul(products):
    print('\n===== PART 2 =====')
    A = int(input('A : '))
    M = int(input('M : '))
    CAP_DAY = int(input('CAP DAY : '))
    CAP_SHOP = int(input('CAP SHOP : '))
    
    bills = []
    for cust_no in range(1, A + 1):
        print(f'\nCUSTOMER NO.{cust_no}')
        K = random.randint(1, M)
        capl_day = CAP_DAY
        capl_shop = {s: CAP_SHOP for s in shops}
        
        cart = []
        for _ in range(K):
            target = random.choice(products)
            if target['stock'] <= 0:
                opts = [p for p in products if p['shop'] == target['shop'] and p['category'] == target['category'] and p['stock'] > 0]
                if opts :
                    opts.sort(key=lambda x: (x['price'], x['code']))
                    target = opts[0]
                else:
                    target = None
            if target:
                target['stock'] -= 1
                cart.append(target)
        
        cart.sort(key=lambda x: (x['shop'], x['code']))
        print(f'{'SHOP' :5} | {'CODE' :5} | {'CATE' :8} | {'PRICE' :5} | {' GOV' :5} | {'CUST'}')
        
        bill_gross, bill_gov, bill_disc = 0, 0, 0
        shop_group = {}
        for item in cart:
            shop_group.setdefault(item['shop'], []).append(item)
            
        final_items = []
        for s_id, items in shop_group.items():
            pre_disc_pay = 0
            shop_gov_total = 0
            for p in items:
                gov_req = p['price'] // 2
                if p['category'] == 'Cloth' : gov_req = min(gov_req, 30)
                elif p['category'] == 'General' and p['price'] > 200: gov_req = 0
                
                gov_act = min(gov_req, capl_day, capl_shop[s_id])
                cust_pay = p['price'] - gov_act
                
                capl_day -= gov_act
                capl_shop[s_id] -= gov_act
                bill_gross += p['price']
                bill_gov += gov_act
                pre_disc_pay += cust_pay
                shop_gov_total += gov_act
                
                final_items.append({
                    'shop' : s_id,
                    'code' : p['code'],
                    'cate' : p['category'],
                    'price' : p['price'],
                    'gov' : gov_act,
                    'cust' : cust_pay,
                    'ref' : p
                })
                
            promo = 0
            if len(items) >= 3: promo = min(pre_disc_pay * 0.07, 40)
            bill_disc += promo
            
            for row in [r for r in final_items if r['shop'] == s_id]:
                share = row['cust'] / pre_disc_pay if pre_disc_pay > 0 else 0
                row['ref']['sold_qty'] += 1
                row['ref']['gov_used_sum'] += row['gov']
                row['ref']['net_revenue'] += (row['cust'] - (promo * share))
                
        for r in final_items:
            print(f'{r['shop'] :5} | {r['code'] :5} | {r['cate'] :8} | {r['price'] :5} | {r['gov'] :5} | {r['cust']}')
            
        net = bill_gross - bill_gov - bill_disc
        print(f'GROSS : {bill_gross} GOV : {bill_gov}, DISC : {bill_disc:.2f}, NET : {net:.2f}')
        print(f'CAP LEFT : DAY : {capl_day} | ' + ', '.join([f'{s}: {capl_shop[s]}' for s in shops]))
        bills.append({
            'id' : cust_no,
            'gross' : bill_gross,
            'gov' : bill_gov,
            'disc' : bill_disc,
            'net' : net
        })
    return bills
                
def show_Analytics(products, bills):
    print('\n===== PART 3 =====')
    print('\n----- 1. Top 3 Best Selling -----')
    products.sort(key=lambda x: (-x['sold_qty'], -x['net_revenue'], x['code']))
    for i in range(min(3, len(products))):
        p = products[i]
        print(f'Top{i+1} : {p['code']} | CATE : {p['category']} | Shop : {p['shop']} | Qty : {p['sold_qty']} | NetRev : {p['net_revenue']:.2f} | Gov : {p['gov_used_sum']}')
        
    s_stats = []
    for s in shops:
        gov = sum(p['gov_used_sum'] for p in products if p['shop'] == s)
        net = sum(p['net_revenue'] for p in products if p['shop'] == s)
        qty =sum(p['sold_qty'] for p in products if p['shop'] == s)
        s_stats.append({
            'shop' : s,
            'gov' : gov,
            'net' : net,
            'qty' : qty
        })
    print('\n----- 2. Top 2 GovTotal -----')
    s_stats.sort(key=lambda x: ( -x['net'], -x['gov']))
    for i in range(2):
        st = s_stats[i]
        print(f'ShopRank{i+1}:  {st['shop']} | Gov : {st['gov']} | NetRev : {st['net']:.2f} | Sold : {st['qty']}')
    
    print('\n----- 3. Best Saver -----')
    for b in bills : b['rate'] = b['gov'] / b['gross'] if b['gross'] > 0 else 0
    bills.sort(key=lambda x: (-x['rate'], x['net'], x['id']))
    best = bills[0]
    print(f'Best Saver : Cust {best['id']} | Gross : {best['gross']} | Gov: {best['gov']} | Net : {best['net']:.2f} | Rate : {best['rate']:.4f}')
    
    print('\n----- 4. Low Stock -----')
    low = sorted([p for p in products if p['stock'] <= 2], key=lambda x: (x['stock'], x['shop'], x['code']))
    for p in low:
        print(f'Low Stock : {p['code']} | Shop : {p['shop']} | Left : {p['stock']}')
    
    print('\n----- 5. Integrity Check -----')
    tg, tgov, td ,tn = sum(b['gross'] for b in bills), sum(b['gov'] for b in bills), sum(b['disc'] for b in bills), sum(b['net'] for b in bills)
    print(f'\nIntegrity : Gross {tg} | Gov {tgov} | Disc {td:.2f} | Net {tn:.2f}')
    print(f'Check : {tg - tgov - td:.2f}')

def main():
    random.seed(int(input('Seed : ')))
    products = createpd()
    show1(products)
    show2(products)
    bills = simul(products)
    show_Analytics(products, bills)
    
main()