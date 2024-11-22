# [$]> python3 toggle_doors.py

# Question: 100 Doors
# There are 100 doors in a row that are all initially closed. You pass by the doors 100 times.
# The first time you pass, visit every door and toggle the door (if the door is closed, open it; if it is open, close it).
# The second time, only visit every 2nd door (i.e., door #2, #4, #6, ...) and toggle them.
# The third time, visit every 3rd door (i.e., door #3, #6, #9, ...) and toggle them.
# And so on, until you reach the 100th pass.

# Write a function that calculates the open/close state of the doors after all passes have been completed.
# Return the door numbers as an array starting from the first door and ending at the 100th door, only including the doors which are open.

# Partial result: [1, 4, 9, ...]

import unittest

def create_doors(num_doors):
  return [False for i in range(num_doors)]

def toggle_doors(doors):
  for i in range(0, len(doors)):
    for door_index in range(i, len(doors), i + 1):
      doors[door_index] = not doors[door_index]
  return doors

def get_doors(doors, open):
  return [index + 1 for index, is_door_open in enumerate(doors) if is_door_open == open]

class TestDoors(unittest.TestCase):
  def test_create_doors_empty(self):
    number_of_doors = 0
    doors = create_doors(number_of_doors)
    self.assertEqual(len(doors), number_of_doors)

  def test_create_doors(self):
    number_of_doors = 100
    doors = create_doors(number_of_doors)
    self.assertEqual(len(doors), number_of_doors)

  def test_get_doors_closed(self):
    self.assertEqual(get_doors([0, 0, 0, 0, 1], False), [1, 2, 3, 4])

  def test_get_doors_open(self):
    self.assertEqual(get_doors([0, 0, 0, 0, 1], True), [5])

  def test_toggle_doors_empty(self):
    toggled_doors = toggle_doors([])
    open_doors = get_doors(toggled_doors, True)
    self.assertEqual(open_doors, [])

  def test_toggle_doors(self):
    doors = create_doors(100)
    toggled_doors = toggle_doors(doors)
    open_doors = get_doors(toggled_doors, True)
    self.assertEqual(open_doors, [1, 4, 9, 16, 25, 36, 49, 64, 81, 100])

if __name__ == '__main__':
  unittest.main()
