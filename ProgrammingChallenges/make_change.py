# [$]> python3 make_change.py

def make_change_v1(change_amount):
  QUARTER = 25
  DIME = 10
  NICKEL = 5
  PENNY = 1

  pennies = 0
  nickels = 0
  dimes = 0
  quarters = 0

  for coin_value in [QUARTER, DIME, NICKEL, PENNY]:
    if change_amount < coin_value:
      continue

    num_of_coins = change_amount // coin_value
    change_amount -= coin_value * num_of_coins

    if coin_value == QUARTER:
      quarters += num_of_coins
    elif coin_value == DIME:
      dimes += num_of_coins
    elif coin_value == NICKEL:
      nickels += num_of_coins
    elif coin_value == PENNY:
      pennies += num_of_coins

  return [pennies, nickels, dimes, quarters]

print('\nVersion 1')

print(make_change_v1(26) == [1, 0, 0, 1])
print(make_change_v1(26))

print(make_change_v1(45) == [0, 0, 2, 1])
print(make_change_v1(45))

def make_change_v2(change_amount):
  coins = [25, 10, 5, 1]
  sorted_coins = sorted(coins)
  num_of_coin_types = len(coins)
  output = [0] * num_of_coin_types

  for index, coin_value in enumerate(coins):
    if change_amount < coin_value:
      continue

    coin_index = sorted_coins.index(coin_value)
    output[coin_index] = change_amount // coin_value
    change_amount -= coin_value * output[coin_index]

  return output

print('\nVersion 2')

print(make_change_v2(26) == [1, 0, 0, 1])
print(make_change_v2(26))

print(make_change_v2(45) == [0, 0, 2, 1])
print(make_change_v2(45))
