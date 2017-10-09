# ucmaxlapi

#####NAME
    ucmaxlapi
#####FILE
    ucmaxlapi.py
#####CLASSES
    RawAxl
    
    class RawAxl
     |  A Very Basic AXL implementation
     |  
     |  The class will create the xml for the soap payload 'from scratch', using dicttoxml to create the calls and
     |  their arguments.
     |  The execute function will take the method name to be called, together with a dict of the arguments. The call
     |  will be executed and the returned xml will be returned as a dict using xmltodict
     |  
     |  Methods defined here:
     |  
     |  __init__(self, username, password, server=None, version='10.5')
     |      Initiate the AXL Client
     |      
     |      this will set the necessary user, passwd, server and version
     |      
     |      :param username (str):
     |      :param password (str):
     |      :param server (str): server name or IP where the AXL service is running
     |      :param version (str): version of CUCM, defaults to 10.5
     |  
     |  execute(self, call, args)
     |      Execute an AXL Call
     |      
     |      Given the method name and a Dict with the arguments, this method will build the SOAP message,
     |      send the call and convert the answer into a Dict and return
     |      
     |      :param call (str): the method name
     |      :param args (Dict): a dictionary for the arguments needed
     |      :return: a dictionary with the returned data

#####TESTS
Run the module as a script to see some basic calls.   
The examples are all 'read' ones, so they are safe to run, althoug they may return 'not found' errors 
for your system (the commented out example will 'add' something, uncomment on your own risk)

`$ python ucmaxlapi.py <username> <password> <server>`