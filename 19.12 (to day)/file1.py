import random

category = ['Drink', 'Food', 'General', 'Cloth', 'Service']
vens = ['V01', 'V02', 'V03', 'V04', 'V05']

def createpd():
    N = random.randint(15, 25)
    product = []
    for i in range(1, N + 1):
        product.append({    
            "id" : i,
            "code" : f'ITEM{i:03d}',
            "category" : random.choice(category),
            "vendor" : random.choice(vens),
            "price" : random.randint(25, 250),
            "stock" : random.randint(1, 20),
            "sold_qty" : 0,
            "revenue" : 0,
            "vouch_sum" : 0,
            "net_revenue" : 0
        })
    return product

def show1(product):
    print('ID\tCODE\t\tCATE\t\tVEN\tPRC\tSTK')
    for s in product:
        print(f'{s['id']}\t{s['code']}\t\t{s['category']:8}\t{s['vendor']}\t{s['price']}\t{s['stock']}')
        
def show2(product):
    print('\n----- 1. Max Price per Category -----')
    for cat in category:
        g = [p for p in product if p['category'] == cat]
        if g:
            g.sort(key=lambda x: (-x['price'], x['code']))
            p = g[0]
            print(f"{cat:8} : {p['code']} | Price : {p['price']}")
            
    print('\n----- 2. System Cheapest -----')
    temp = product[:]
    temp.sort(key=lambda x: (x['price'], x['vendor'], x['code']))
    low = temp[0]
    print(f'Code: {low['code']} | Vendor : {low['vendor']} | Price : {low['price']}')
    
    print('\n----- 3. Category List -----')
    for cat in category:
        g = [p for p in product if p['category'] == cat]
        g.sort(key=lambda x: x['code'])
        print(f'{cat} = {len(g)}')
        for p in g:
            print(f' {p['code']}\t{p['price']}')
            
    print("\n----- 4. Price Band Histogram -----")
    bands = {'0-49': 0, '50-99': 0, '100-149': 0, '150-199': 0, '200-249': 0, '250+': 0}
    for p in product:
        v = p['price']
        if v < 50: bands['0-49'] += 1
        elif v < 100: bands['50-99'] += 1
        elif v < 150: bands['100-149'] += 1
        elif v < 200: bands['150-199'] += 1
        elif v < 250: bands['200-249'] += 1
        else: bands['250+'] += 1
    for k, v in bands.items():
        print(f'{k:8} : {'*' * v} ({v})')
        
def process(product):
    A = int(input('A : '))
    M = int(input('M : '))
    CAP = int(input('Daily Voucher Cap : '))
    
    nets = []
    
    for o in range(1, A + 1):
        print('\nCUSTOMER NO.', o)
        K = random.randint(1, M)
        cart = []
        vouch_left = CAP
        
        for _ in range(K):
            target = random.choice(product)
            if target['stock'] <= 0:
                opts = [p for p in product if p['category'] == target['category'] and p['stock'] > 0]
                if opts:
                    opts.sort(key=lambda x: (x['price'], x['code']))
                    target = opts[0]
                else:
                    target = None
                    
            if target:
                target['stock'] -= 1
                cart.append(target)
                
        cart.sort(key=lambda x: (x['code'], x['vendor']))
        
        print(f"{'CODE':8} | {'CAT':8} | {'VEN':4} | {'PRC':4} | {'QTY':3} | {'VOUC':5} | {'VDISC':5} | {'SDISC':5} | {'FEE':4} | {'NET'}")
        
        bill_gross = 0
        bill_vouch = 0
        bill_disc = 0
        bill_fee = 0
        
        incart = []
        for c in cart:
            if c['code'] not in incart:
                incart.append(c['code'])
                
        v_spend = {}
        process_line = []
        
        for c_code in incart:
            items = [i for i in cart if i['code'] == c_code]
            qty = len(items)
            p = items[0]
            
            line_v = 0
            for _ in range(qty):
                v_req = p['price'] * 0.5
                v_act = min(v_req, vouch_left)
                line_v += v_act
                vouch_left -= v_act
                
            line_disc = 0
            if qty >= 2:
                line_disc = p['price'] * 0.10 * (qty - 1)
                
            line_fee = 0
            if p['category'] == 'Service':
                line_fee = (p['price'] * qty - line_v) * 0.05
                
            v_spend[p['vendor']] = v_spend.get(p['vendor'], 0) + (p['price'] * qty - line_v - line_disc)
            
            process_line.append({
                "p" : p,
                "qty" : qty,
                "v" : line_v,
                "sd" : line_disc,
                "fee" : line_fee
            })
        
        promo_map = {}
        for ven in v_spend:
            v_qty = sum(1 for c in cart if c['vendor'] == ven)
            if v_qty >= 3:
                promo_map[ven] = min(v_spend[ven] * 0.07, 50)
                
        for line in process_line:
            p = line['p']
            vd = 0
            if p['vendor'] in promo_map:
                share = (p['price'] * line['qty']) / sum(x['price'] for x in cart if x['vendor'] == p['vendor'])
                vd = promo_map[p['vendor']] * share
                
            net_line = (p['price'] * line['qty']) - line['v'] - line['sd'] - vd + line['fee']
            print(f"{p['code']:8} | {p['category']:8} | {p['vendor']:4} | {p['price']:4} | {line['qty']:3} | {line['v']:5.1f} | {vd:5.1f} | {line['sd']:5.1f} | {line['fee']:4.1f} | {net_line:.1f}")
            
            bill_gross += p['price'] * line['qty']
            bill_vouch += line['v']
            bill_disc += (line['sd'] + vd)
            bill_fee += line['fee']
            
            p['sold_qty'] += line['qty']
            p['revenue'] += p['price'] * line['qty']
            p['vouch_sum'] += line['v']
            p['net_revenue'] += net_line
            
        net_bill = bill_gross - bill_vouch - bill_disc + bill_fee
        print(f"Gross : {bill_gross}, Voucher : {bill_vouch:.1f}, Discount : {bill_disc:.1f}, Fee : {bill_fee:.1f}, Net : {net_bill:.1f}")
        nets.append({
            "id" : o,
            "gross" : bill_gross,
            "net" : net_bill,
            "vouch" : bill_vouch,
            "disc" : bill_disc
        })
    
    return nets

def summary(product, nets):
    print('\n----- PART 3: ANALYTICS -----')
    print('\n1. Top 3 Sold Items')
    product.sort(key=lambda x: (-x['sold_qty'], -x['revenue'], x['code']))
    for i in range(min(3, len(product))):
        p = product[i]
        print(f"CODE: {p['code']} | CAT: {p['category']:8} | VEN: {p['vendor']} | PRC: {p['price']} | Qty: {p['sold_qty']} | Rev: {p['revenue']:.2f} | Vouc: {p['vouch_sum']:.1f}")
        
    print('\n2. Top 2 Vendor Net')
    v_net = []
    for ven in vens:
        vrev = sum(p['net_revenue'] for p in product if p['vendor'] == ven)
        v_qty_sum = sum(p['sold_qty'] for p in product if p['vendor'] == ven)
        v_net.append({
            "ven" : ven,
            "rev" : vrev,
            "qty" : v_qty_sum
        })
    v_net.sort(key=lambda x: -x['rev'])
    for i in range(2):
        print(f"Vendor: {v_net[i]['ven']} | NetRevenue: {v_net[i]['rev']:.2f} | SoldQty: {v_net[i]['qty']}")
        
    print('\n3. Best Saver')
    for n in nets:
        n['rate'] = (n['vouch'] + n['disc']) / n['gross'] if n['gross'] > 0 else 0
    nets.sort(key=lambda x: (-x['rate'], x['net'], x['id']))
    b = nets[0]
    print(f"Cust : {b['id']} | Rate : {b['rate']:.4f}")
    
    print('\n4. Average')
    count = len(nets)
    print(f"AvgGross: {sum(n['gross'] for n in nets)/count:.2f}")
    print(f"AvgNet: {sum(n['net'] for n in nets)/count:.2f}")
    print(f"AvgVoucher: {sum(n['vouch'] for n in nets)/count:.2f}")
    print(f"AvgDiscount: {sum(n['disc'] for n in nets)/count:.2f}")
    
    print('\n5. Low Stock (<= 2)')
    low = [p for p in product if p['stock'] <= 2]
    low.sort(key=lambda x: (x['stock'], x['code']))
    for p in low:
        print(f"{p['code']} : {p['stock']}")
        
def main():
    s_val = int(input('Seed : '))
    random.seed(s_val)
    print('\n===== PART 1 =====')
    product = createpd()
    show1(product)
    show2(product)
    print('\n===== PART 2 =====')
    nets = process(product)
    print('\n===== PART 3 =====')
    summary(product, nets)
    
main()