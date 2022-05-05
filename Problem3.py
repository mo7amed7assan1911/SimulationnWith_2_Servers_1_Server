import time

def teamNames():
    names = ['Mohamed Mohamed Mohamed Hassan', 'Mennat Allah Moataz Medhat Zaki', 'Mustafa Ahmed Abdel Azim Ibrahim', 'Yara Nasir El Din Mohamed Mabrouk', 'Muhammad Abdul Sattar Abdul Sattar']
    
    print('=' * 100)
    print(' ' * 15, '='* 29, 'Team Members', '='* 29, ' ' * 15)
    for name in names:
        print(' ' * 35, name)
        time.sleep(0.5)
    print(' ' * 15, '=' * 72, ' ' * 15)
    

def getArrivalTimes(InterArrivalTimes):
    """
        Takes:
            InterArrivalTimes[]: array of inter arrival times.
        Return: 
            arrivals[]: array of arrival times to use in our simulation.

    """
    arrivals = []
    for i in range(len(InterArrivalTimes)):
        if i == 0:
            arrivals.append(InterArrivalTimes[0])
            continue
        else:
            arrivals.append(
                InterArrivalTimes[i] + arrivals[i - 1]
            )
    return arrivals

def IsAvilServer(LastCustomer, Arrival):
    """
        Takes:
            LastCustomer: the end of the last service on that Server.
            Arrival: the time of the next arriaval service.
            
        Return:
            'Yes': is server is availServer.
            'No': if server is not avaliServer.
    """ 

    if Arrival >= LastCustomer:
        return 'Yes'
    else:
        return 'No'

def initialization():
    """
        Just to intialize each varibale and array we will use
        in our simulaion.
    """
    print('=' * 100)
    print('[ Start Of Simulation! ', '\n')
    
    
    InterArrivalTimes = [0, 2, 4, 4, 2, 2]
    ArrivalTimes = getArrivalTimes(InterArrivalTimes)
    ServiceTimes = [5, 3, 3, 5, 6, 3]
    
    Server = {
        'ServiceTime': 0,
        'Service_Start': 0,
        'Service_End': 0
    }
    
    queue = []
    TotalWaitingTimes = 0
    clk = 0
    EndOfSimulation = ArrivalTimes[-1] + ServiceTimes[-1] + 1
    Server_ToBeFree = Server['Service_End']
    
    service_id = 0
    NumberOfWaitings = 0
    lenOfServices = len(ServiceTimes)
    TotalServiceTimes = sum(ServiceTimes)
    
    
    Rebort = {
        '(e) Average Waiting time of those who wait in queue d(n)': 0,
        '(f) Time-average number in queue q(n)': 0,
        '(g) total busy time B(t)': sum(ServiceTimes),
        '(h) utilization u(n) of the server': 0,
        '(i) average service time': 0,
        '(j) average waiting time': 0,
        '(k) average time customer spends in the system': 0,
        '(l) Throughput': 0
    }
    
    return ArrivalTimes, ServiceTimes, Server, queue, TotalWaitingTimes, clk, EndOfSimulation, Server_ToBeFree, Rebort, service_id, NumberOfWaitings, lenOfServices, TotalServiceTimes

def IsFreeNow(Server):
    """
        Takes:
            Server: integet represents the amount of
                    time fot the server to be free.
        Return:
            Server:  The same as the Tokens after less them by one.
        
        Print: 
            sign for the new free servers.
    """
    
    if (Server == 0):
        print('Server is FREE')
    else:
        Server -= 1
    return Server


def Simulation():
    """
        Our main function to make the simulation.
    """
    ArrivalTimes, ServiceTimes, Server, queue, TotalWaitingTimes, clk, EndOfSimulation, Server_ToBeFree, Rebort, service_id, NumberOfWaitings, lenOfServices, TotalServiceTimes = initialization()

    
    while clk < 30 :
        
        print('Clk', clk)
        Server_ToBeFree = IsFreeNow(Server_ToBeFree)
        try: # to help continue the simulation till the end seconds of the last service. Not to take new services.  
            serverChecker = IsAvilServer(Server['Service_End'], clk)  # getting the avilServer server to take this service.
            
            # if there is an arrival event exist:
            if len(ArrivalTimes) == 0:
                ArrivalTimes.append(-10)    # only to still take from the queue.
                
            if ((len(queue) > 0) and (serverChecker is 'Yes')) or (clk == ArrivalTimes[0]):
                
                # if there is any services in the queue.
                if queue and (serverChecker is 'Yes'):
                    WaitService = queue.pop(0)
                
                    start = clk
                    serviceTime = WaitService['ServiceTimes']
                    service_id = WaitService['service_id']
                    
                    print('** Waiting Service **')
                    
                else:
                    # So, there is no thing in queue and there is a new service.
                    print('** NEW Service **')
                    
                    service_id = clk
                    start = ArrivalTimes.pop(0)
                    serviceTime = ServiceTimes.pop(0)
                    
                End = start + serviceTime
                
                if serverChecker == 'Yes':
                    
                    Server = {
                        'ServiceTime': serviceTime,
                        'Service_Start': start,
                        'Service_End': End
                    }
                    
                    # time for Server to be free by ending the current service he toke.
                    Server_ToBeFree = Server['ServiceTime'] - 1
                    
                    print(f'========== Server Take service [{service_id}] for {serviceTime} Seconds! ==========')
                    
                # if the server is busy ... wait till the server being availServer and give it the waited services 
                else:
                    
                    services = [serv['service_id'] for serv in queue]
                    service_id = clk
                    
                    if service_id not in services:
                        
                        if len(queue) == 0:
                            Bast_End = Server['Service_End']
                        else:
                            # past_waits = [serv['amountOfWait'] + serv['ServiceTimes'] for serv in queue]
                            # past_waits = sum(past_waits)
                            Bast_End = queue[-1]['Service_End']     # to use it as the start of the new service.
                            
                        amount_of_waiting = Bast_End - service_id
                        Service_End =  Bast_End + serviceTime
                        # dictionary to save the data of the waiting service.
                        queue.append({
                            'service_id': service_id,
                            'ServiceTimes': serviceTime,
                            'Service_Start': Bast_End,
                            'amountOfWait': amount_of_waiting,
                            'Service_End': Service_End
                        })
                        TotalWaitingTimes += amount_of_waiting
                        NumberOfWaitings += 1
                    
                    print('******** Server is busy now, Waiting ...')
        except:
            pass
        
        
        """if there is only one service in the queue and there is no arrival services
        so the end of simulation is the end of this service in the queue."""
        
        if (len(queue) == 1) and (ArrivalTimes[0] < 0):
            EndOfSimulation = queue[0]['Service_End'] 
        
        if clk == EndOfSimulation: 
            break
        
        time.sleep(1)
        clk += 1
    
    print('\n[ End Of Simulation! ]\n')
    
    
    Rebort['(e) Average Waiting time of those who wait in queue d(n)'] = TotalWaitingTimes /  NumberOfWaitings
    Rebort['(f) Time-average number in queue q(n)'] = TotalWaitingTimes / EndOfSimulation
    Rebort['(h) utilization u(n) of the server'] = Rebort['(g) total busy time B(t)'] / EndOfSimulation
    Rebort['(i) average service time'] = TotalServiceTimes / lenOfServices
    Rebort['(j) average waiting time'] = TotalWaitingTimes / lenOfServices
    Rebort['(k) average time customer spends in the system'] = (TotalServiceTimes + TotalWaitingTimes) / lenOfServices
    Rebort['(l) Throughput'] = lenOfServices / EndOfSimulation
    
    # printing the report.
    print('=' * 47, 'Report', '=' * 47, '\n')
    
    for key, value in Rebort.items():
        print(key, ' = ', round(value, 4))
        
    print('\n', '=' * 100)





if __name__ == '__main__':
    teamNames()
    Simulation()