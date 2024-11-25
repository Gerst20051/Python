# [$]> python3 elevator.py

class ElevatorController:
  floor = 1
  requested_floors = []

  def __init__(self, number_of_floors):
    self.number_of_floors = number_of_floors

  def requested_floor(self, next_floor):
    if 1 <= next_floor <= self.number_of_floors and next_floor not in self.requested_floors:
      self.requested_floors.append(next_floor)

  def move(self):
    if self.requested_floors:
      self.floor = self.requested_floors.pop(0)
      print(self.floor)

elevator = ElevatorController(10)
elevator.requested_floor(3)
elevator.move() # 3
elevator.requested_floor(20)
elevator.move() # 3
elevator.requested_floor(10)
elevator.move() # 10
