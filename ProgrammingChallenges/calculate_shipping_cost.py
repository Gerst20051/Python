# [$]> python3 calculate_shipping_cost.py

def calculate_shipping_cost(order, cost_matrix):
  order_cost = 0
  order_country = order['country']
  country_shipping_cost = cost_matrix[order_country]
  for item in order['items']:
    item_cost = [matrix_item for matrix_item in country_shipping_cost if matrix_item['product'] == item['product']][0]
    remaining_quantity = item['quantity']
    for cost in item_cost['costs']:
      if remaining_quantity:
        item_quantity = remaining_quantity
        if cost['maxQuantity'] is not None and item_quantity > cost['maxQuantity']:
          item_quantity = cost['maxQuantity']
        order_cost += item_quantity * cost['cost']
        if cost['maxQuantity'] is None:
          remaining_quantity = 0
        else:
          remaining_quantity -= cost['maxQuantity']
  return order_cost

order_us = {
  "country": "US",
  "items": [
    {"product": "mouse", "quantity": 20},
    {"product": "laptop", "quantity": 5}
  ]
}

order_ca = {
  "country": "CA",
  "items": [
    {"product": "mouse", "quantity": 20},
    {"product": "laptop", "quantity": 5}
  ]
}

shipping_cost = {
  "US": [
    {
      "product": "mouse",
      "costs": [
        {
          "minQuantity": 0,
          "maxQuantity": None,
          "cost": 550
        }
      ]
    },
    {
      "product": "laptop",
      "costs": [
        {
          "minQuantity": 0,
          "maxQuantity": 2,
          "cost": 1000
        },
        {
          "minQuantity": 3,
          "maxQuantity": None,
          "cost": 900
        }
      ]
    }
  ],
  "CA": [
    {
      "product": "mouse",
      "costs": [
        {
          "minQuantity": 0,
          "maxQuantity": None,
          "cost": 750
        }
      ]
    },
    {
      "product": "laptop",
      "costs": [
        {
          "minQuantity": 0,
          "maxQuantity": 2,
          "cost": 1100
        },
        {
          "minQuantity": 3,
          "maxQuantity": None,
          "cost": 1000
        }
      ]
    }
  ]
}

print(calculate_shipping_cost(order_us, shipping_cost) == 15700)
print(calculate_shipping_cost(order_ca, shipping_cost) == 20200)
