from datetime import datetime

def iOrchid_clock(zone):
    timeFile = open(f"{zone}/data_DO_NOT_MODIFY/time.txt", "w")
    hour = datetime.now().hour
    timeFile.write(str(hour))
    timeFile.close()
    
def iOrchid_seasonal_clock(zone):
    seasonFile = open(f"{zone}/data_DO_NOT_MODIFY/season(summer=1winter=2).txt", "w")
    month = datetime.now().month
    if month == 9 or month == 10 or month == 11 or month == 12 or month == 1 or month == 2 or month == 3 or month == 4:
        seasonFile.write("1")  # Summer 
    if month == 5 or month == 6 or month == 7 or month == 8:
        seasonFile.write("2")  # Winter
    seasonFile.close()
