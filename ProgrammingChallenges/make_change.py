# [$]> python3 make_change.py

def make_change(change_amount):
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

print(make_change(26) == [1, 0, 0, 1])
print(make_change(26))

print(make_change(45) == [0, 0, 2, 1])
print(make_change(45))
