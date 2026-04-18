from datetime import datetime

def iOrchid_clock(zone):
    timeFile = open(f"{zone}/data_DO_NOT_MODIFY/time.txt", "w")
    hour = datetime.now().hour
    timeFile.write(str(hour))
    timeFile.close()
    
def iOrchid_seasonal_clock(zone):
    seasonFile = open(f"{zone}/data_DO_NOT_MODIFY/season(summer=1winter=2).txt", "w")
    month = datetime.now().month
    if month in [5, 6, 7, 8, 9, 10]:  # May to October - Summer (active growing season)
        seasonFile.write("1")
    else:  # November to April - Winter (dormant season)
        seasonFile.write("2")
    seasonFile.close()
