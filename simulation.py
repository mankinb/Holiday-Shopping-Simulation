from ArrayADT import Array
from BasicQueue import Node, Queue
from PriorityQueue import PNode, PriorityQueue
import random

class Event:  

  def __init__(self, event_time, event_type, id):
    self.ARRIVAL = "Arrival"
    self.BEGIN_SERVICE = "Begin Service"
    self.END_SERVICE = "End Service"
    self.ARRIVE_WRAP = "Arrive Wrap"
    self.BEGIN_WRAP = "Begin Wrap"
    self.END_WRAP = "End Wrap"
    self.time = event_time
    self.type = event_type
    self.id_num = id
    
    self.cashier = None
    self.giftwrapper = None

  def assign_cashier(self, cashier):
    self.cashier = cashier

  def assign_wrapper(self, wrapper):
    self.giftwrapper = wrapper

  def arrival_time(self):
    return self.time

  def type(self):
    return self.type

  def identify(self):
    return self.type


class Customer:

  def __init__(self, id, arrival_time):
    """
    Creates a passenger object
    """
    self.id_num = id
    self.arrival_time = arrival_time

  def id_num(self):
    """
    Gets the customer's id number
    """
    return self.id_num

  def time_arrived(self):
    """
    Gets the customer's arrival time
    """
    return self.arrival_time



class Cashier:
   
  def __init__(self, id_num):
    """
    Constructor for the Cashier class. 
    It takes in an id_num argument. the _passenger attribute is used to track the state of an agent (free or not free)
    """
    self.id_num = id_num
    self.customer = None
    self.stop_time = -1
    
  def id_num(self):
    """
    Returns the ID assigned to the cashier
    """
    return self.id_num 
    
  def is_free(self):
    """
    Returns a boolean value that represents is an cashier is free or not. "True" means that the cashier is free. "False" means that the cashier is currently servicing a customer
    """
    return self.customer is None 
      

  def is_finished(self, cur_time):
    """
    Determines if the customer that is currently being serviced by an cashier is done by returning a boolean
    """
    return self.customer is not None and self.stop_time == cur_time

  def start_service(self, customer, stop_time):
    """
    Assigns the customer and stop_time attributes with their respective arguments when an object is created
    """
    self.customer = customer
    self.stop_time = stop_time


  def stop_service(self):
    """
    Ends the transaction between the cashier and customer. It stores the self.customer object in a variable, the_customer,then sets customer to None so that the cashier is free again. It then return the customer object, the_customer
    """
    the_customer = self.customer
    self.customer = None
    return the_customer



class Giftwrapper:

  def __init__(self, id_num):
    self.id_num = id_num
    self.customer = None
    self.stop_time = -1

  def id_num(self):
    return self.id_num 
      
  def is_free(self):
    return self.customer is None 
        

  def is_finished(self, cur_time):
    return self.customer is not None and self.stop_time == cur_time

  def start_service(self, customer, stop_time):
    self.customer = customer
    self.stop_time = stop_time


  def stop_service(self):
    the_customer = self.customer
    self.customer = None
    return the_customer

class StoreSimulation:

  def __init__(self, num_cashiers, total_sim_time, interarrival_time, service_time, giftwrap_time, num_wrappers, percent_wrap_service):
    # declare debug status
    self.debug = True
    #self.debug = False

    # simulation components
    self.sim_time = total_sim_time
    self.event_q = PriorityQueue()   
    self.the_cashiers = Array(num_cashiers)    
    for i in range(num_cashiers):
      self.the_cashiers[i] = Cashier(i+1)

    self.the_wrappers = Array(num_wrappers)
    for i in range(num_wrappers): 
      self.the_wrappers[i] = Giftwrapper(i+1)
    
    # Computed during the simulation.
    self.total_wait_time = 0
    self.num_customers = 0
    self.waiting_q = Queue()
    self.wrapping_q = Queue()
    self.customers_served = 0
    self.still_in_service = 0
    self.service_time = service_time
    self.inter_time = interarrival_time
    self.wrapping_time = giftwrap_time
    self.p_wrap_service = percent_wrap_service
    self.in_wrapping_queue = 0
    self.total_wrap_time = 0
    self.done_wrapping = 0


  def generate_arrival_events(self, lamda):
    current_time = random.randint(1, self.inter_time)

    while current_time < self.sim_time:
      new_customer = Customer(self.num_customers, current_time)
      arrival = Event(current_time, "Arrival", new_customer)
      self.event_q.enqueue(current_time, arrival)
      
      

      self.num_customers += 1
      rand_inter_time = random.randint(1, self.inter_time)
      current_time += rand_inter_time


  def print_results(self):

    
    num_served = self.num_customers - self.customers_served
    try:
      avg_wait = float(self.sim_time) / self.customers_served
    except ZeroDivisionError:
      print("Average service time is too high for your other simulation parameters!")  
    try:
      avg_wrap_wait = float(self.total_wrap_time) / self.done_wrapping
    except ZeroDivisionError:
      print("Hmm, there's something wrong with these simulation parameters.")
    print("")
    print("=========Simulation Statistics=========")
    print("Number of customers: " + str(self.num_customers))
    print("Number of customers served: " + str(self.customers_served))
    print("Average wait time: " + str(avg_wait))
    print("Number of customers remaining in line: %d" % num_served)
    print("Number of customers remaining in the wrapping queue: " + str(self.in_wrapping_queue))
    print("Average gift-wrapping wait time: " + str(avg_wrap_wait))
    print("========================================")

  def run(self):
    cur_time = 0
    self.generate_arrival_events(self.service_time)
    while not self.event_q.is_empty() and cur_time < self.sim_time:
      current = self.event_q.dequeue()
      cur_time = current.time
      if cur_time > self.sim_time:
        break

      if current.type == current.ARRIVAL:
        self.handle_arrival(current)
      elif current.type == current.BEGIN_SERVICE:
        self.handle_begin_service(current)
      elif current.type == current.END_SERVICE:
        self.handle_end_service(current)
      elif current.type == current.ARRIVE_WRAP:
        self.wrap_arrival(current)
      elif current.type == current.BEGIN_WRAP:
        self.begin_wrap(current)
      elif current.type == current.END_WRAP:
        self.end_wrap(current)



  def handle_arrival(self, event):
    free_cashier = self.find_free_cashier(event.time)
    if free_cashier != -1:
      begin_event = Event(event.time, event.BEGIN_SERVICE, event.id_num)
      begin_event.assign_cashier(free_cashier)
      self.event_q.enqueue(begin_event.time, begin_event)
      self.num_customers += 1

    else:
      self.waiting_q.enqueue(event.id_num)

    if self.debug == True: 
        print("Time: " + str(event.time) + " | Customer " + str(event.id_num.id_num) + " arrived.")
    else:
      pass


  def handle_begin_service(self, event):
    current_cashier = event.cashier
    current_customer = event.id_num
    
    # schedule and end service @ next random time
    end_time = random.randint(1, self.service_time) + event.time
    end_event = Event(end_time, event.END_SERVICE, event.id_num)

    current_cashier.start_service(current_customer, event.time + end_event.time)
    end_event.assign_cashier(current_cashier)
    # enqueue the end time event to the queue
    self.event_q.enqueue(end_event.time, end_event)
    
    if self.debug == True:
      print("Time: " + str(event.time) + " | Customer " + str(current_customer.id_num) + " has begun service with cashier " + str(current_cashier.id_num))
    
    else:
      pass

    self.still_in_service += 1
    self.total_wait_time += event.time
    


  def handle_end_service(self, event):

    current_cashier = event.cashier

    if self.debug == True:
      print("Time: " + str(event.time) + " | Customer " + str(event.id_num.id_num) + " has ended service with cashier " + str(current_cashier.id_num))
    else:
      pass

    self.customers_served += 1
    self.still_in_service -= 1

    if not self.waiting_q.is_empty():
      customer = self.waiting_q.dequeue()
      next_event = Event(event.time, event.END_SERVICE, customer)

      next_event.assign_cashier(event.cashier)
      self.handle_begin_service(next_event)
      


    elif event.cashier != None:
        event.cashier.stop_service()


    percent = random.randint(1, 100)
    if (100 - self.p_wrap_service) <= percent:
      onto_wrapping = Event(event.time, event.ARRIVE_WRAP, event.id_num)
      self.wrap_arrival(onto_wrapping)
    
    elif event.giftwrapper != None:
        event.giftwrapper.stop_service()



  def wrap_arrival(self, event):
    free_wrapper = self.find_free_wrapper(event.time)
    if free_wrapper != -1:
      start_wrapping = Event(event.time, event.BEGIN_WRAP, event.id_num)
      start_wrapping.assign_wrapper(free_wrapper)
      self.event_q.enqueue(start_wrapping.time, start_wrapping)

    else:
      self.wrapping_q.enqueue(event.id_num)
      self.in_wrapping_queue += 1


      if self.debug == True: 
          print("Time: " + str(event.time) + " | Customer " + str(event.id_num.id_num) + " has joined the gift wrapping queue")
      else:
        pass



  def begin_wrap(self, event):
    current_wrapper = event.giftwrapper
    current_customer = event.id_num

    # schedule and end wrapping service @ next random time, self.wrapping_time = mu2
    wrap_time = random.randint(1, self.wrapping_time)
    end_wrap_event = Event(wrap_time + event.time, event.END_WRAP, event.id_num)

    self.total_wrap_time += wrap_time

    current_wrapper.start_service(current_customer, event.time + end_wrap_event.time)
    end_wrap_event.assign_wrapper(current_wrapper)
    self.event_q.enqueue(end_wrap_event.time, end_wrap_event)

    if self.debug == True:
      print("Time: " + str(event.time) + " | Customer " + str(current_customer.id_num) + "'s gift is being wrapped by wrapper " + str(current_wrapper.id_num))
    
    else:
      pass


  def end_wrap(self, event): 

    if self.debug == True:
      print("Time: " + str(event.time) + " | Customer " + str(event.id_num.id_num) + " has ended service with gift wrapper " + str(event.giftwrapper.id_num))
    else:
      pass

    if not self.wrapping_q.is_empty():
      customer = self.wrapping_q.dequeue()
      self.in_wrapping_queue -= 1
      next_event = Event(event.time, event.END_WRAP, customer)

      next_event.assign_wrapper(event.giftwrapper)
      self.begin_wrap(next_event)
      
    
    else:
      if event.giftwrapper != None:
        event.giftwrapper.stop_service()
        self.done_wrapping += 1


  def find_free_cashier(self, end_time):
    for i in range(len(self.the_cashiers)):
      if self.the_cashiers[i].is_free() and self.the_cashiers[i].stop_time < end_time:
        return self.the_cashiers[i]
  # found a free one
    return -1      # no free agent is found

  def find_free_wrapper(self, end_time):
    for i in range(len(self.the_wrappers)):
      if self.the_wrappers[i].is_free() and self.the_wrappers[i].stop_time < end_time:
        return self.the_wrappers[i]
    return -1


def read_input():
  
  print('Input simulation parameters : ')
  num_agents = int(input('1. Number of cashiers: '))
  total_sim_time = int(input('2. Total simulation time: '))
  interarrival_time = int(input('3. Average interarrival time: '))
  service_time = int(input('4. Average service time: '))
  giftwrap_time = int(input("5. Max gift wrapping time: "))
  num_wrappers = int(input("6. Number of gift wrappers: "))
  percent_wrap_service = int(input("7. Percentage of customers to use gift-wrapping service: "))
  return num_agents, total_sim_time, interarrival_time, service_time, giftwrap_time, num_wrappers, percent_wrap_service

def main():
  '''
  Test parameters:
  
  num_cashiers = 2
  total_sim_time = 1000
  interarrival_time = 2
  service_time = 5
  giftwrap_time = 2
  num_wrappers = 1

  num_cashiers = 5
  total_sim_time = 3000
  interarrival_time = 2
  service_time = 14
  giftwrap_time = 2
  num_wrappers = 2
  '''
  num_cashiers, total_sim_time, interarrival_time, service_time, giftwrap_time, num_wrappers, percent_wrap_service = read_input()
  bison_retail_store = StoreSimulation(num_cashiers, total_sim_time, interarrival_time, service_time, giftwrap_time, num_wrappers, percent_wrap_service)

  print('Number of Cashiers: ', num_cashiers)
  print('Total Sim Time: ', total_sim_time)
  print('Interarrival Time: ', interarrival_time)
  print('Service Time: ', service_time)
  print('Max gift wrapping time: ', giftwrap_time)
  print('Number of gift wrappers: ', num_wrappers)
  print('Percentage of customers to use gift-wrapping service: ', percent_wrap_service)
  bison_retail_store.run()
  bison_retail_store.print_results()

main()
