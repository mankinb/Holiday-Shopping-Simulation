Holiday Shopping Simulation

Takes in seven inputs from the user.

When debug mode is uncommented, a log of every customer arrival is printed, along with which cashier is servicing them. A percentage of these customers may then move to the gift-wrapping queue.

A statistical summary of the simulation is displayed, regardless of the status of debug mode.

Example run outputs:

Sample run outputs are as follows:

num_cashiers = 2
total_sim_time = 1000
interarrival_time = 2
service_time = 5
giftwrap_time = 2
num_wrappers = 1
percent_wrap_service = 50

=========Simulation Statistics=========
Number of customers: 674
Number of customers served: 660
Average wait time: 1.5151515151515151
Number of customers remaining in line: 14
Number of customers remaining in the wrapping queue: 69
Average gift-wrapping wait time: 78.2

________________________________________________________

num_cashiers = 5
total_sim_time = 3000
interarrival_time = 2
service_time = 14
giftwrap_time = 2
num_wrappers = 2
percent_wrap_service = 50

=========Simulation Statistics=========
Number of customers: 2004
Number of customers served: 1827
Average wait time: 1.6420361247947455
Number of customers remaining in line: 177
Number of customers remaining in the wrapping queue: 177
Average gift-wrapping wait time: 85.61538461538461