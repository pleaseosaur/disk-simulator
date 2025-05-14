# DiskSim.py
# Disk scheduling simulator
# CSCI 447
# Spring 2024
#
# Andrew Cox
# 03 June 2024

import sys
import random

NUM_CYLINDERS = 10000

# FCFS: First-Come, First-Served
# proceses requests in the order they are received
def fcfs(head, direction, requests):
    order = requests[:]  # copy list
    movement = 1
    direction_changes = 0

    # iterate through requests
    for request in requests:
        # skip duplicate requests
        if request == head:
            order.remove(request)
            continue

        # calculate movement and direction changes
        movement += abs(request - head)
        if (request > head and direction == 'L') or (request < head and direction == 'H'):
            direction_changes += 1
            direction = 'H' if direction == 'L' else 'L'
        head = request

    return {'FCFS': (order, direction_changes, movement)}

# SSTF: Shortest Seek Time First
# processes the request closest to the head first
def sstf(head, direction, requests):
    requests = list(dict.fromkeys(requests)) # remove duplicates
    order = []
    movement = 1
    direction_changes = 0

    # iterate through requests
    while len(requests) > 0:
        # find the closest request
        closest = min(requests, key = lambda x: abs(x - head))
        movement += abs(closest - head)
        # calculate direction changes
        if (closest > head and direction == 'L') or (closest < head and direction == 'H'):
            direction_changes += 1
            direction = 'H' if direction == 'L' else 'L'
        # move head and update results
        head = closest
        requests.remove(closest)
        order.append(closest)

    return {'SSTF': (order, direction_changes, movement)}

# SCAN
# processes requests in the direction of the head until the end of the disk,
# then goes back in the opposite direction, processing requests until the beginning
def scan(head, direction, requests):
    requests = list(dict.fromkeys(requests)) # remove duplicates
    order = []
    movement = 1
    direction_changes = 0

    # iterate through requests
    while len(requests) > 0:
        if direction == 'H':
            # move head to the end of the disk
            for request in sorted(requests):
                if request >= head:
                    movement += abs(request - head)
                    head = request
                    requests.remove(request)
                    order.append(request)

            # switch direction
            if len(requests) > 0:
                # move head to the end of the disk
                movement += abs(NUM_CYLINDERS - 1 - head)
                head = NUM_CYLINDERS - 1
                direction = 'L'
                direction_changes += 1
        else:
            # move head to the beginning of the disk
            for request in reversed(sorted(requests)):
                if request <= head:
                    movement += abs(request - head)
                    head = request
                    requests.remove(request)
                    order.append(request)

            # switch direction
            if len(requests) > 0:
                # move head to the beginning of the disk
                movement += head
                head = 0
                direction = 'H'
                direction_changes += 1

    return {'SCAN': (order, direction_changes, movement)}

# C-SCAN
# processes requests in the direction of the head until the end of the disk,
# then goes back to the beginning
def c_scan(head, direction, requests):
    requests = list(dict.fromkeys(requests)) # remove duplicates
    order = []
    movement = 1
    direction_changes = 0

    # reset head if direction is 'H' and there are no requests to service
    if direction == 'H' and head > max(requests):
        movement += abs(NUM_CYLINDERS - 1 - head)
        direction_changes += 1
        movement += NUM_CYLINDERS - 1
        direction_changes += 1
        head = 0

    # reset head if direction is 'L'
    elif direction == 'L':
        movement += head
        head = 0
        direction_changes += 1
        direction = 'H'

    # iterate through requests
    while len(requests) > 0:
        # move head to the end of the disk
        for request in sorted(requests):
            if request >= head:
                movement += abs(request - head)
                head = request
                requests.remove(request)
                order.append(request)

        # update movement and move to the beginning of the disk
        if len(requests) > 0:
            movement += abs(NUM_CYLINDERS - 1 - head)
            direction_changes += 1
            movement += NUM_CYLINDERS - 1
            head = 0

    return {'C-SCAN': (order, direction_changes, movement)}

# LOOK
# processes requests in the direction of the head until there are no more requests
# in that direction, then reverses direction and processes requests in the opposite direction
def look(head, direction, requests):
    requests = list(dict.fromkeys(requests)) # remove duplicates
    order = []
    movement = 1
    direction_changes = 0

    # iterate through requests
    while len(requests) > 0:
        if direction == 'H':
            for request in sorted(requests):
                # process requests toward higher cylinder numbers
                if request >= head:
                    movement += abs(request - head)
                    head = request
                    requests.remove(request)
                    order.append(request)
            # switch direction
            if len(requests) > 0:
                direction = 'L'
                direction_changes += 1
        else:
            # process requests in the opposite direction
            for request in reversed(requests):
                if request <= head:
                    movement += abs(request - head)
                    head = request
                    requests.remove(request)
                    order.append(request)
            # switch direction
            if len(requests) > 0:
                direction = 'H'
                direction_changes += 1

    return {'LOOK': (order, direction_changes, movement)}

# C-LOOK
# processes requests in the direction of the head until there are no more requests
# in that direction, then goes back to the beginning
def c_look(head, direction, requests):
    requests = list(dict.fromkeys(requests)) # remove duplicates
    order = []
    movement = 1
    direction_changes = 0

    # reset head to minimum request if direction is 'H' and there are no requests to service
    if direction == 'H' and head > max(requests):
        min_request = min(requests)
        movement += abs(head - min_request)
        head = min_request
        direction_changes += 1
        requests.remove(min_request)
        order.append(min_request)
        direction_changes += 1

    # reset head to minimum request if direction is 'L'
    elif direction == 'L' and len(requests) > 0:
        min_request = min(requests)
        movement += abs(min_request - head)
        head = min_request
        direction_changes += 1
        direction = 'H'
        requests.remove(min_request)
        order.append(min_request)

    # iterate through requests
    while len(requests) > 0:
        for request in sorted(requests):
            # process requests toward higher cylinder numbers
            if request >= head:
                movement += abs(request - head)
                head = request
                requests.remove(request)
                order.append(request)
        # switch direction
        if len(requests) > 0:
            min_request = min(requests)
            movement += abs(min_request - head)
            head = min_request
            direction_changes += 1
            requests.remove(min_request)
            order.append(min_request)

    return {'C-LOOK': (order, direction_changes, movement)}


# start the simulation
def run_simulation(head, direction, requests):

    results = {}

    # First Come First Serve (FCFS)
    results.update(fcfs(head, direction, requests[:]))
    # Shortest Seek Time First (SSTF)
    results.update(sstf(head, direction, requests[:]))
    # SCAN
    results.update(scan(head, direction, requests[:]))
    # C-SCAN
    results.update(c_scan(head, direction, requests[:]))
    # LOOK
    results.update(look(head, direction, requests[:]))
    # C-LOOK
    results.update(c_look(head, direction, requests[:]))

    return results

# generate random requests
def generate_requests(requests):
    return [random.randint(0, NUM_CYLINDERS - 1) for i in range(requests)]

# print results
def print_results(results):
    print("== Service history ==")
    for key, value in results.items():
        print(key, ' '.join(str(i) for i in value[0]))

    print("== Service stats ==")
    for key, value in results.items():
        print(key, value[1], value[2])

def main():

    head = 0
    direction = 'H'
    requests = []

    # parse command line arguments
    if len(sys.argv) == 2:
        # Random mode
        if sys.argv[1] == 'R':
            head = random.randint(0, NUM_CYLINDERS - 1)
            direction = random.choice(['H', 'L'])
            requests = generate_requests(1000)
        else:
            print("Invalid argument")
            sys.exit(1)
    # Parameter mode
    elif len(sys.argv) >= 4:
        head = int(sys.argv[1])
        direction = sys.argv[2]
        if sys.argv[3].startswith('R'):
            requests = generate_requests(int(sys.argv[3][1:]))
        else:
            requests = [int(i) for i in sys.argv[3:]]
    else:
        print("Invalid arguments")
        sys.exit(1)

    results = run_simulation(head, direction, requests)

    print_results(results)

if __name__ == '__main__':
    main()
