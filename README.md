# Bank Simulation (CS 4348 – Project 2)

This project implements a multi-threaded bank simulation using Python’s `threading` module and semaphores. The simulation models interactions between customers, tellers, the manager, and the safe while ensuring correct concurrency control and proper event ordering.

## Overview
The simulation includes:
- 50 Customer threads  
- 3 Teller threads  
- Shared semaphores controlling:
  - Door capacity (2 customers max)
  - Manager permission (1 teller at a time)
  - Safe access (2 tellers at a time)
  - Teller availability queue
  - Customer–teller synchronization

Output order varies due to threading but always respects the assignment’s rules.

## How to Run

### 1. Navigate to the folder
```bash
cd "C:\Users\senay\OneDrive\Desktop\python\python"
```
## Run the program
python bank_sim.py
## Sample output
Teller 1: waiting for a customer
Customer 12 [Teller 1]: asks for withdrawal transaction
Teller 1 [Customer 12]: getting manager's permission
Teller 1 [Customer 12]: going to safe
Customer 12 [-]: leaves teller
...
The bank closes for the day.

## Project Structure

| File            | Description                                 |
|-----------------|---------------------------------------------|
| bank_sim.py     | Main simulation code                        |
| example.py      | Professor’s example semaphore program       |
| thread_demo.py  | Simple thread demonstration                 |
| devlog.md       | Full development log with timestamps        |

---

## Simulation Logic

### Customer Flow
1. Randomly chooses deposit or withdrawal  
2. Waits 0–100ms  
3. Enters the bank (door limit = 2)  
4. Waits in line for a teller  
5. Provides ID and transaction request  
6. Waits for teller to complete manager/safe operations  
7. Leaves teller → goes to door → exits bank  

### Teller Flow
1. Starts ready and waiting  
2. Accepts a customer  
3. Requests transaction details  
4. For withdrawal: get manager approval  
5. For all transactions: access safe  
6. Completes transaction  
7. Waits for customer to leave  
8. Repeats until all customers are served  
9. Prints “leaving for the day” when finished  

---

## Semaphores Used

| Semaphore          | Max         | Purpose                                      |
|--------------------|-------------|----------------------------------------------|
| door_sem           | 2           | Controls max customers entering              |
| manager_sem        | 1           | Manager approval (withdrawals only)          |
| safe_sem           | 2           | Limits concurrent teller access to safe      |
| teller_ready_sem[i]| 1 per teller| Signals teller availability                   |
| customer_done_sem[i]| 1 per teller| Ensures teller waits until customer leaves   |

---

## End of Simulation

After all 50 customers finish:

- All tellers print: `Teller X [-]: leaving for the day`  
- Final message: **"The bank closes for the day."**
