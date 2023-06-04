import time
import random
import multiprocessing


num_of_trials = 1000

num_of_prisoners = 100
checks_per_prisoner = 50

boxes = random.sample(range(1, num_of_prisoners+1), num_of_prisoners)


def run_random(boxes: list):
  found_numbers = []

  for i in range(1, num_of_prisoners+1):
    if i in random.sample(boxes, checks_per_prisoner):
      found_numbers.append(i)

  return len(found_numbers)


def run_loop_strategy(boxes: list):
  found_numbers = []

  for i in range(1, num_of_prisoners+1):
    check_num = 1
    box_val = boxes[i-1] # e.g. prisoner 5 starts at 5th box (index 4)

    while box_val != i:
      box_val = boxes[box_val-1]
      check_num += 1
      
    if check_num <= checks_per_prisoner:
      found_numbers.append(box_val)

  return len(found_numbers)

def run_both():
  new_boxes = boxes.copy()
  random.shuffle(new_boxes)

  return run_random(new_boxes), run_loop_strategy(new_boxes)

def print_results(success_count):
  print(f"prisoners survived {success_count}/{num_of_trials} times ({round(success_count/num_of_trials*100, 1)}%)")

def run_trials():
  print(f"\nrunning {num_of_trials} trials...")    
  pool = multiprocessing.Pool(multiprocessing.cpu_count())
  
  all_results = [pool.apply_async(run_both, args=[]) for _ in range(num_of_trials)]
  pool.close()
  pool.join()
  results = [r.get() for r in all_results]

  success_random = sum(1 for i in results if i[0] == num_of_prisoners)
  success_loop = sum(1 for i in results if i[1] == num_of_prisoners)

  print("\n**** Random ****")
  print_results(success_random)
  
  print("\n**** Loop Strategy ****")
  print_results(success_loop)

def get_elapsed_time(start, end):
  seconds = round(end - start, 2)
  if seconds >= 60:
    return f'{int(seconds/60)}m {seconds%60}s'
  return f'{seconds}s'

if __name__ == '__main__':
  start = time.time()
  
  run_trials()
  
  print(f'\ntime elapsed: {get_elapsed_time(start, time.time())}')
  print()