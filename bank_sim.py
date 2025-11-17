import threading
import queue
import random
import time

NUM_TELLERS = 3
NUM_CUSTOMERS = 50

# Queue for customers
customer_queue = queue.Queue()
customer_ready = threading.Semaphore(0)

# Semaphores required by assignment
door_sem = threading.Semaphore(2)       # Only 2 customers entering/leaving
safe_sem = threading.Semaphore(2)       # Only 2 tellers in safe
manager_sem = threading.Semaphore(1)    # Only 1 teller talking to manager

# Shared state per customer
transaction_type = [None] * NUM_CUSTOMERS
assigned_teller = [-1] * NUM_CUSTOMERS

# Thread sync objects per-customer
customer_selected = [threading.Semaphore(0) for _ in range(NUM_CUSTOMERS)]
teller_asked = [threading.Semaphore(0) for _ in range(NUM_CUSTOMERS)]
transaction_given = [threading.Semaphore(0) for _ in range(NUM_CUSTOMERS)]
transaction_done = [threading.Semaphore(0) for _ in range(NUM_CUSTOMERS)]
customer_left = [threading.Semaphore(0) for _ in range(NUM_CUSTOMERS)]

# Prevent overlapping prints
print_lock = threading.Lock()

def tlog(tid, inner, msg):
    if inner is None:
        tag = "[]"
    else:
        tag = f"[{inner}]"
    with print_lock:
        print(f"Teller {tid} {tag}: {msg}")

def clog(cid, inner, msg):
    if inner is None:
        tag = "[]"
    else:
        tag = f"[{inner}]"
    with print_lock:
        print(f"Customer {cid} {tag}: {msg}")


def teller_thread(tid):
    tlog(tid, None, "ready to serve")

    while True:
        tlog(tid, None, "waiting for a customer")
        customer_ready.acquire()
        cid = customer_queue.get()

        if cid is None:  # sentinel: end
            break

        # Start serving
        tlog(tid, f"Customer {cid}", "serving a customer")
        assigned_teller[cid] = tid
        customer_selected[cid].release()

        # Ask for transaction
        tlog(tid, f"Customer {cid}", "asks for transaction")
        teller_asked[cid].release()

        # Wait for customer to tell us deposit/withdrawal
        transaction_given[cid].acquire()
        ttype = transaction_type[cid]

        # If withdrawal, go to manager
        if ttype == "withdrawal":
            tlog(tid, f"Customer {cid}", "handling withdrawal transaction")
            tlog(tid, f"Customer {cid}", "going to the manager")
            manager_sem.acquire()
            tlog(tid, f"Customer {cid}", "getting manager's permission")
            time.sleep(random.uniform(0.005, 0.03))
            tlog(tid, f"Customer {cid}", "got manager's permission")
            manager_sem.release()
        else:
            tlog(tid, f"Customer {cid}", "handling deposit transaction")

        # Go to safe
        tlog(tid, f"Customer {cid}", "going to safe")
        safe_sem.acquire()
        tlog(tid, f"Customer {cid}", "enter safe")
        time.sleep(random.uniform(0.01, 0.05))
        tlog(tid, f"Customer {cid}", "leaving safe")
        safe_sem.release()

        # Finish
        if ttype == "withdrawal":
            tlog(tid, f"Customer {cid}", "finishes withdrawal transaction.")
        else:
            tlog(tid, f"Customer {cid}", "finishes deposit transaction.")

        transaction_done[cid].release()

        # Wait for customer to leave
        tlog(tid, f"Customer {cid}", "wait for customer to leave.")
        customer_left[cid].acquire()

    tlog(tid, None, "leaving for the day")


def customer_thread(cid):
    # Choose deposit/withdrawal
    ttype = random.choice(["deposit", "withdrawal"])
    transaction_type[cid] = ttype
    clog(cid, None, f"wants to perform a {ttype} transaction")

    # Walk to bank
    time.sleep(random.uniform(0, 0.10))

    # Enter through limited door
    clog(cid, None, "going to bank.")
    door_sem.acquire()
    clog(cid, None, "entering bank.")
    door_sem.release()

    # Get in line
    clog(cid, None, "getting in line.")
    clog(cid, None, "selecting a teller.")
    customer_queue.put(cid)
    customer_ready.release()

    # Wait for teller to choose us
    customer_selected[cid].acquire()
    tid = assigned_teller[cid]
    clog(cid, f"Teller {tid}", "selects teller")
    clog(cid, f"Teller {tid}", "introduces itself")

    # Teller asks for transaction
    teller_asked[cid].acquire()
    clog(cid, f"Teller {tid}", f"asks for {ttype} transaction")
    transaction_given[cid].release()

    # Wait for teller to finish
    transaction_done[cid].acquire()

    # Leave bank
    clog(cid, f"Teller {tid}", "leaves teller")
    door_sem.acquire()
    clog(cid, None, "goes to door")
    clog(cid, None, "leaves the bank")
    door_sem.release()

    customer_left[cid].release()


def main():
    random.seed()

    # Start tellers
    tellers = [threading.Thread(target=teller_thread, args=(i,)) 
               for i in range(NUM_TELLERS)]
    for t in tellers:
        t.start()

    # Start customers
    customers = [threading.Thread(target=customer_thread, args=(i,))
                 for i in range(NUM_CUSTOMERS)]
    for c in customers:
        c.start()

    # Wait for customers
    for c in customers:
        c.join()

    # End tellers
    for _ in range(NUM_TELLERS):
        customer_queue.put(None)
        customer_ready.release()

    for t in tellers:
        t.join()

    print("The bank closes for the day.")


if __name__ == "__main__":
    main()
