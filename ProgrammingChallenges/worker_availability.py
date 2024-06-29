availability = {
  'worker_1': [(9, 11), (13, 15)],
  'worker_2': [(10, 12), (14, 16)],
  'worker_3': [(11, 13), (15, 17)],
}

def get_available_workers(worker_availability, time_range):
  available_workers = []
  for index, worker in enumerate(worker_availability):
    availability = worker_availability[worker]
    for time_block in availability:
      if time_block[0] <= time_range[0] and time_block[1] >= time_range[1]:
        available_workers.append(worker)
        break
  return available_workers

print(get_available_workers(availability, (10, 11)) == ['worker_1', 'worker_2'])
print(get_available_workers(availability, (15, 16)) == ['worker_2', 'worker_3'])
print(get_available_workers(availability, (18, 19)) == [])
