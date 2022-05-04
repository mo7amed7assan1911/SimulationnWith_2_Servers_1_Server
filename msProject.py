import time
from tkinter import N



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

def getWhichServer(LastCustomer_Able, LastCustomer_Baker, Arrival):
    """
        Takes:
            LastCustomer_Able: the end of the last service on that Able server.
            LastCustomer_Baker: the end of the last service on that Baker server.
            Arrival: the time of the next arriaval service.
            
        Return:
            'Able': if Able is Free.
            'Baker': if Able is not Free and Baker is free.
            'Wait': if neither Able nor Baker is free.
    """ 
    AbleState = 1
    BakerState = 1
    
    if Arrival >= LastCustomer_Able:
        AbleState = 0
    
    if Arrival >= LastCustomer_Baker:
        BakerState = 0
        
    if (AbleState == 0 and BakerState == 0) or (AbleState == 0 and BakerState == 1):
        return 'Able'
    elif (AbleState == 1 and BakerState == 0): 
        return 'Baker'
    else:
        return 'Wait'

def initialization():
    """
        Just to intialize each varibale and array we will use
        in our simulaion.
    """
    
    InterArrivalTimes = [0, 2, 4, 4, 2, 2]
    ArrivalTimes = getArrivalTimes(InterArrivalTimes)
    ServiceTimes = [5, 3, 3, 5, 6, 3]
    
    Able = {
        'ServiceTime': 0,
        'Service_Start': 0,
        'Service_End': 0
    }
    
    Baker = {
        'ServiceTime': 0,
        'Service_Start': 0,
        'Service_End': 0
    }
    
    queue = []
    TotalWaitingTimes = 0
    clk = 0
    EndOfSimulation = ArrivalTimes[-1] + ServiceTimes[-1] + 1
    Able_ToBeFree = Able['Service_End']
    Baker_ToBeFree = Baker['Service_End']
    
    Rebort = {
        'e) Average Waiting time of those who wait in queue d(n)': 0,
        'f) Time-average number in queue q(n)': 0,
        'g) total busy time B(t)': sum(ServiceTimes) / 2,
        'h) utilization u(n) of the server': 0,
        'i) average service time': 0,
        'j) average waiting time': 0,
        'k) average time customer spends in the system': 0,
        'l) Throughput': 0, 
    }
    
    return ArrivalTimes, ServiceTimes, Able, Baker, queue, TotalWaitingTimes, clk, EndOfSimulation, Able_ToBeFree, Baker_ToBeFree, Rebort

def WhoFreeNow(Able, Baker):
    """
        Takes:
            Able, Baker:    2 integers represent the amount of
                            time for each server to be free.
        Return:
            Able, Baker:    The same as the Tokens after less them by one.
        
        Print: 
            sign for the new free servers.
    """
    
    if (Able == 0) and (Baker == 0):
            print('Able is FREE *** Baker is FREE') 
    elif (Able != 0) and (Baker == 0):
            print('Baker is FREE')
            Able -= 1
    elif (Able == 0) and (Baker != 0):
            print('Able is FREE')
            Baker -= 1
    elif (Able != 0) and (Baker != 0):
            Baker -= 1
            Able -= 1 
        
    return Able, Baker

def amountOfWait(Able, Baker, clk):
    """
        Take:
            Able, Baker: 2 integers to identify the end of the 
                        services that done by each server.
            clk: integer to identify the current clk.
        Return:
            the amount of time from current clock to the end of 
            nearest end of service done by the two servers.
    """
    wait = 0
    if Able <= Baker:
        wait = Able
    else:
        wait = Baker
    
    return wait - clk

def Simulation():
    """
        Our main function to make the simulation.
    """
    ArrivalTimes, ServiceTimes, Able, Baker, queue, TotalWaitingTimes, clk, EndOfSimulation, Able_ToBeFree, Baker_ToBeFree, Rebort = initialization()
    service_id = 0
    NumberOfWaitings = 0
    lenOfServices = len(ServiceTimes)
    TotalServiceTimes = sum(ServiceTimes)
    
    while clk <= EndOfSimulation :
        
        print('clk', clk) 
        Able_ToBeFree, Baker_ToBeFree = WhoFreeNow(Able_ToBeFree, Baker_ToBeFree)
        try: # to help continue the simulation till the end seconds of the last service. Not to take new services.  
            
            # if there is an arrival event exist:
            if queue or (clk == ArrivalTimes[0]):
                Server = getWhichServer(Able['Service_End'], Baker['Service_End'], clk)  # getting the avilable server to take this service.
                
                # if there is any services in the queue.
                if queue and (Server is not 'wait'):
                    WaitService = queue.pop(0)
                    
                    start = clk
                    serviceTime = WaitService['ServiceTimes']
                    service_id = WaitService['service_id']
                    
                    print('** Waiting Service **')
                else:
                    # So, there is no thing in queue and there is a new service.
                    print('** NEW Service **')
                    start = ArrivalTimes.pop(0)
                    serviceTime = ServiceTimes.pop(0)
                    
                End = start + serviceTime
                
                if Server == 'Able':
                    
                    Able = {
                        'ServiceTime': serviceTime,
                        'Service_Start': start,
                        'Service_End': End
                    }
                    
                    # time for Able to be free by ending the current service he toke.
                    Able_ToBeFree = Able['ServiceTime'] - 1
                    
                    print(f'========== Able Take this service for {serviceTime} Seconds! ==========')
                    
                elif Server == 'Baker':
                    Baker = {
                        'ServiceTime': serviceTime,
                        'Service_Start': start,
                        'Service_End': End
                    }
                    # time for Baker to be free by ending the current service he toke.
                    Baker_ToBeFree = Baker['ServiceTime'] - 1
                    
                    print(f'========== Baker Take this service for {serviceTime} Seconds! ==========')
                
                # if the 2 servers are busy ... wait till one of them being available and give it the waited services 
                else:
                    queue = []
                    services = [serv['service_id'] for serv in queue]
                    service_id = clk
                    
                    if service_id not in services:
                        amount_of_waiting = amountOfWait(Able['Service_End'], Baker['Service_End'], clk)
                        
                        # dictionary to save the data of the waiting service.
                        queue.append({
                            'service_id': service_id,
                            'ServiceTimes': serviceTime,
                            'amountOfWait': amount_of_waiting
                        })
                        TotalWaitingTimes += amount_of_waiting
                        NumberOfWaitings += 1
                    
                    print('******** Servers are busy now, Waiting ...')
        except:
            pass
        
        time.sleep(1)
        clk += 1
    
    print('\n[ End Of Simulation! ]\n')
    
    
    Rebort['e) Average Waiting time of those who wait in queue d(n)'] = TotalWaitingTimes /  NumberOfWaitings
    Rebort['f) Time-average number in queue q(n)'] = TotalWaitingTimes / EndOfSimulation
    Rebort['h) utilization u(n) of the server'] = Rebort['g) total busy time B(t)'] / EndOfSimulation
    Rebort['i) average service time'] = TotalServiceTimes / lenOfServices
    Rebort['j) average waiting time'] = TotalWaitingTimes / lenOfServices
    Rebort['k) average time customer spends in the system'] = (TotalServiceTimes + TotalWaitingTimes) / lenOfServices
    Rebort['l) Throughput'] = lenOfServices / EndOfSimulation
    
    # printing the report.
    print('=' * 47, 'Report', '=' * 47, '\n')
    
    for key, value in Rebort.items():
        print(key, ' = ', round(value, 4))
        
    print('\n', '=' * 100)


if __name__ == '__main__':
    Simulation()