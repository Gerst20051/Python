# [$]> python3 snapshot_map.py

from typing import Optional

class SnapshotMap:
  def __init__(self):
    self.maps = [{}]

  def get(self, k: str, snap_id: Optional[int] = None) -> int:
    starting_index = snap_id if snap_id is not None else (len(self.maps) - 1)
    for map_index in range(starting_index, -1, -1):
      if k in self.maps[map_index]:
        if self.maps[map_index][k] is None:
          raise KeyError
        return self.maps[map_index][k]
    raise KeyError

  def put(self, k: str, v: int) -> None:
    self.maps[len(self.maps) - 1][k] = v

  def delete(self, k: str) -> None:
    self.put(k, None)

  def take_snapshot(self) -> int:
    self.maps.append({})
    return len(self.maps) - 2

print("===== Initialization =====")

# Create an instance of SnapshotMap
s = SnapshotMap()

# Add key-value pairs to the map
s.put("a", 1)
s.put("b", 2)

# Take a snapshot of the current state of the map
snap_id_0 = s.take_snapshot()

# Update the map
s.put("a", 5)
s.delete("b")
s.put("a", 10)

# Take another snapshot
snap_id_1 = s.take_snapshot()

# Update the map again
s.put("b", 20)

# Take a final snapshot
snap_id_2 = s.take_snapshot()

# Update the map one last time
s.put("a", 100)

print("===== Validation =====")

# Assert the current state of the map and the state at each snapshot
assert s.get("a") == 100
assert s.get("a", snap_id_0) == 1
assert s.get("a", snap_id_1) == 10
assert s.get("a", snap_id_2) == 10

assert s.get("b") == 20
assert s.get("b", snap_id_0) == 2

# Check that a KeyError is raised for a key that does not exist in a snapshot
try:
  s.get("b", snap_id_1)
except KeyError:
  pass
else:
  raise Exception("KeyError was not raised")

assert s.get("b", snap_id_2) == 20

print("===== All Passed! =====")
