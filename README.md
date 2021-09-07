# smart-cache-prototype

### Requirements
Python 3.6

# How to Run
1. Run dag_generator.py to generate the large scale interdependent system.  
    The default parameters are set to 20 servers and 25 dependencies.  
    Edit the file to change the parameters as needed.

2. Run request_generator.py to generate a json file of all the requests.  
    The default parameters are set to 20 servers and 100 requests.  
    Edit the file to change the parameters as needed.

3. Run main.py to simulate.
    The default parameter is set to single_cluster = False. Which simulates the clustered Robinhood.  
    Set to single_cluster = True, to compare with standard Robinhood.

# Minimum working example

python dag_generator.py  
python request_generator.py  
python main.py