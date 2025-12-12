



def max_profit(prices):
    min_price = float("inf")
    best = 0
    for p in prices:
        if p < min_price:
            min_price = p
        if p - min_price > best:
            best = p - min_price
    return best


print(max_profit([7, 1, 5, 3, 6, 4]))
