import socket
import threading
from queue import Queue
import time
import logging

"""
Multithreaded port scanner that scans for open ports on a single target IP
"""


# create a queue object
queue = Queue()

openports = []

start_time = time.time()
logging.debug(f"Scanning begins at: {start_time}")

# to prevent the overwriting or double modification of shared resources/variables
print_lock = threading.Lock()


def worker(target_IP):
	while not queue.empty():
		port = queue.get()
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# similar to connect() but returns error indicator instead of error type on failure
		connect_s = s.connect_ex( (target_IP, port) )
		if(connect_s == 0):
			with print_lock:
				logging.debug (f'Port {port}: OPEN')
				openports.append(port)
 


def scan_ports_on_host(target):
	target_IP = socket.gethostbyname(target)
	logging.debug (f'Starting scan on host: {target_IP}')

	# queueing ports
	for port in range(1, 1001):
		queue.put(port)

	# scanning from 1-1000 ports
	thread_list = []
	
	threads=100
	for t in range(threads):
		thread = threading.Thread(target=worker(target_IP))
		thread_list.append(thread)

	for thread in thread_list:
		thread.start()

	for thread in thread_list:
		thread.join()

	time_taken = str(time.time() - start_time)
	logging.debug(f'Time taken: {time_taken}')
	return(openports)
