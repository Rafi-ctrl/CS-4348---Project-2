## Development Log – Bank Simulation Project

Author: Rufael Tekleab

Course: Operating Systems (CS 4348.504)  

Project: Project 2 - Multithreaded Bank Simulation  

Date: 11/16/2025



## 2025-11-16 14:05 – Initial planning

* Read project spec. Plan to implement a multi-threaded bank simulation with 3 teller threads and 50 customer threads.
* Identified necessary shared resources: door capacity (2), manager approval (1), safe access (2), teller availability queue, and customer–teller handshake semaphores.
* Goals: correct synchronization, no deadlocks or starvation, realistic print ordering matching sample format.



**Plan for this session**

* Set up project folder and place all .py files inside.
* Build initial teller and custome thread loops with placeholder prints.
* Implement global semaphores and structure the teller/customer workflow.



## 2025-11-16 15:40 – Work session

* Implemented teller workflow: ready state, waiting for customer, asking transaction, manager access, safe access, finishing transaction, and waiting for customer to exit.
* Implemented customer workflow: random transaction selection, entering door, joining line, selecting teller, providing ID/transaction, waiting for completion, leaving bank.
* Added correct semaphores: door, manager, safe, teller\_ready, and per-customer completion signals.
* Confirmed print formatting matches assignment style.



**Work performed**

* **teller code**: created full sequence including blocking on manager/safe; added ordered print statements before and after each step.
* **customer code**: added door capacity control; added queue-based teller selection; added waiting logic for teller to finish.
* **sync fixes**: resolved early-leave issue, corrected safe release timing, fixed deadlock between tellers and waiting customers.



**Issues & fixes**

* Deadlock occurred when tellers and customers both waited on each other → fixed by restructuring signaling order.
* Safe semaphore remained locked after long runs → fixed release placement.
* Customers occasionally exited before tellers printed "wait for customer to leave" → enforced strict semaphore ordering.



**Results**

* Completed full simulation with proper sequencing.
* All 50 customers successfully served; tellers exit properly.
* End message appears: "The bank closes for the day."



**Next session**

* Write README with usage, explanation of semaphores, and design notes.
* Initialize git repo and commit files.
* Prepare final submission zip.



## 2025-11-16 18:10 – Final reflection

* Verified end-to-end behavior, including manager and safe constraints.
* README completed with instructions and explanation of concurrency model.
* Repo cleaned and committed. Project ready for submission.
