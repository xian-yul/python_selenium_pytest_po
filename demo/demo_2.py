total_price = 0
for i in range(0, 100):
    price = int(input('输入价格：'))
    if price == 0:
        break
    total_price += price
print(str(total_price))
