def calculate(items, shipping=0, tax_percent=0, budget=None):
    rows=[]; subtotal=0
    for item in items:
        line=item.quantity*item.unit_price; subtotal += line
        rows.append({"name":item.name,"quantity":item.quantity,"unit_price":item.unit_price,"subtotal":round(line,2)})
    tax=subtotal*(tax_percent/100); total=subtotal+shipping+tax
    return {"items":rows,"subtotal":round(subtotal,2),"shipping":round(shipping,2),"tax":round(tax,2),"total":round(total,2),"budget":budget,"currency":"INR","within_budget":None if budget is None else total<=budget,"difference":None if budget is None else round(budget-total,2)}
