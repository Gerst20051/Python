# [$]> python3 thread_pool_workers.py

# https://docs.python.org/3/library/concurrent.futures.html

from concurrent.futures import ThreadPoolExecutor, wait

def f(id, s):
  def work():
    # NOTE: counter will be 0 when finished
    # for _ in range(1000000):
    #   s['counter'] = (s['counter'] + 1) % 10

    # NOTE: counter will be 50000000 when finished
    for _ in range(10000000):
        s['counter'] += 1
    print(f'{id} done store {s}')

  return work

executor = ThreadPoolExecutor() # pool

store = {'counter': 0}

running = []

for task in [f(x, store) for x in range(5)]:
  running.append(executor.submit(task))

while running:
  done, running = wait(running, timeout = 2.5)

# shutdown(wait=True, *, cancel_futures=False)
executor.shutdown()

print(store)
