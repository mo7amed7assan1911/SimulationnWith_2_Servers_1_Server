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

def Simulation():
    InterArrivalTimes = [0, 2, 4, 4, 2, 1]
    ArrivalTimes = getArrivalTimes(InterArrivalTimes)
    ServiceTimes = [5, 3, 3, 5, 6, 3]
    
    Able = {
        'ServiceTime': 0,
        'Service_Start': 0,
        'Servide_End': 0
    }
    
    Baker = {
        'ServiceTime': 0,
        'Service_Start': 0,
        'Servide_End': 0
    }
    queue = []
    TimeInQueue = 0
    clk = 0
    EndOfSimulation = ArrivalTimes[-1] + ServiceTimes[-1] + 1
    
    while clk <= EndOfSimulation:
        print(clk)
        try: # to help contiuing the simulation till the end seconds of the last service.
            
            # if there is an arrival event exist:
            if clk == ArrivalTimes[0]:  
                Server = getWhichServer(Able['Servide_End'], Baker['Servide_End'], clk)  # getting the avilable server to take this service.
                if Server == 'Able':
                    start = ArrivalTimes.pop(0)
                    serviceTime = ServiceTimes.pop(0)
                    End = start + serviceTime
                    
                    Able = {
                        'ServiceTime': serviceTime,
                        'Service_Start': start,
                        'Servide_End': End
                    }
                    
                    print(f'========== Able Take a service for {serviceTime} Seconds! ==========')
                
                elif Server == 'Baker':
                    start = ArrivalTimes.pop(0)
                    serviceTime = ServiceTimes.pop(0)
                    End = End = start + serviceTime
                    
                    Baker = {
                        'ServiceTime': serviceTime,
                        'Service_Start': start,
                        'Servide_End': End
                    }
                    print(f'========== Baker Take a service for {serviceTime} Seconds! ==========')
                
                # if the 2 servers are busy ... wait till one of them being available and give it the waited services 
                else: 
                    TimeInQueue += 1
                    queue.append(clk)
                    ArrivalTimes[0] += 1
                    print('******** Servers are busy now, Waiting ...')
        except:
            pass
        
        time.sleep(1)
        clk += 1
        
    print('\n[ End Of Simulation ]')







if __name__ == '__main__':
    Simulation()