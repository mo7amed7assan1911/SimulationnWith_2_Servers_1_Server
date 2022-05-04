import time



def getArrivalTimes(InterArrivalTimes):
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
    TimeInQueue = 0
    clk = 0
    EndOfSimulation = ArrivalTimes[-1] + ServiceTimes[-1]
    Able_ToBeFree = Able['Service_End']
    Baker_ToBeFree = Baker['Service_End']
    
    return ArrivalTimes, ServiceTimes, Able, Baker, queue, TimeInQueue, clk, EndOfSimulation, Able_ToBeFree, Baker_ToBeFree

def WhoFreeNow(Able, Baker):
    if (Able == 0) and (Baker == 0):
            print('Able is FREE') 
            print('Baker is FREE')
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

def Simulation():
    
    ArrivalTimes, ServiceTimes, Able, Baker, queue, TimeInQueue, clk, EndOfSimulation, Able_ToBeFree, Baker_ToBeFree = initialization()
    
    while clk <= EndOfSimulation:
        
        print(clk) 
        Able_ToBeFree, Baker_ToBeFree = WhoFreeNow(Able_ToBeFree, Baker_ToBeFree)
        try: # to help continue the simulation till the end seconds of the last service. Not to take new services.  
            # if there is an arrival event exist:
            if clk == ArrivalTimes[0]:  
                Server = getWhichServer(Able['Service_End'], Baker['Service_End'], clk)  # getting the avilable server to take this service.
                if Server == 'Able':
                    start = ArrivalTimes.pop(0)
                    serviceTime = ServiceTimes.pop(0)
                    End = start + serviceTime
                    
                    Able = {
                        'ServiceTime': serviceTime,
                        'Service_Start': start,
                        'Service_End': End
                    }
                    Able_ToBeFree = Able['Service_End'] - 1
                    
                    print(f'========== Able Take a service for {serviceTime} Seconds! ==========')
                
                elif Server == 'Baker':
                    start = ArrivalTimes.pop(0)
                    serviceTime = ServiceTimes.pop(0)
                    End = End = start + serviceTime
                    
                    Baker = {
                        'ServiceTime': serviceTime,
                        'Service_Start': start,
                        'Service_End': End
                    }
                    Baker_ToBeFree = Baker['Service_End'] - 1
                    print(f'========== Baker Take a service for {serviceTime} Seconds! ==========')
                
                # if the 2 servers are busy ... wait till one of them being available and give it the waited services 
                else:
                    TimeInQueue += 1
                    queue.append(clk)
                    ArrivalTimes[0] += 1
                    print('******** Servers are busy now, Waiting ...')
        except:
            pass

        time.sleep(1.4)
        clk += 1
    
    print('\n[ End Of Simulation! ]')
    print('Queue: ', queue)
    print('Total waiting time: ', TimeInQueue)    







if __name__ == '__main__':
    Simulation()