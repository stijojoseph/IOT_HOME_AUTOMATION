from datetime import datetime
def str_check(main,check):
    i=j=k=0
    for i in range(0,len(main)):
        if main[i]==check[j] and j<len(check)-1:
            j=j+1
            
            
        if j!=0:
            k=k+1
        
        if k!=j and j!=len(check)-1:
            j=0;
            k=0
    if j==len(check)-1:
        return 1
    
    return 0
    
#print(str_check("securitykey:stijo","securitykey"))
def test():
 s="STIJO"
 t="stijo"
 if s.lower()==t.lower():
    print("yes")

 s="stijo"

def sql_data(s):
    s="'"+s+"'"
    return s
def timer():
 from datetime import datetime
 now = datetime.now()
 datenow= now.strftime("%d/%m/%Y")
 timenow=now.strftime("%H:%M:%S")
 print("date and time =", datenow,timenow)
 
def difference(h1, m1, h2, m2):
      
    # convert h1 : m1 into
    # minutes
    t1 = h1 * 60 + m1
      
    # convert h2 : m2 into
    # minutes 
    t2 = h2 * 60 + m2
      
    if (t1 == t2): 
        print("Both are same times")
        return 0
    else:
       diff=t1-t2  
        # calculating the difference
       if t2>t1: 
        diff = t2-t1
      
        
        
    # calculating hours from
    # difference
    h = (int(diff / 60)) % 24
      
    # calculating minutes from 
    # difference
    m = diff % 60
  
    print(h, ":", m)
    return h+float(m/60)
#difference(22,40,10,10)
 
# Python3 program two find number of
# days between two given dates

# A date has day 'd', month 'm' and year 'y'


class Date:
	def __init__(self, d, m, y):
		self.d = d
		self.m = m
		self.y = y


# To store number of days in all months from
# January to Dec.
monthDays = [31, 28, 31, 30, 31, 30,
			31, 31, 30, 31, 30, 31]

# This function counts number of leap years
# before the given date


def countLeapYears(d):

	years = d.y

	# Check if the current year needs to be considered
	# for the count of leap years or not
	if (d.m <= 2):
		years -= 1

	# An year is a leap year if it is a multiple of 4,
	# multiple of 400 and not a multiple of 100.
	return int(years / 4) - int(years / 100) + int(years / 400)


# This function returns number of days between two
# given dates
def getDifference(dt1, dt2):

	# COUNT TOTAL NUMBER OF DAYS BEFORE FIRST DATE 'dt1'

	# initialize count using years and day
	n1 = dt1.y * 365 + dt1.d

	# Add days for months in given date
	for i in range(0, dt1.m - 1):
		n1 += monthDays[i]

	# Since every leap year is of 366 days,
	# Add a day for every leap year
	n1 += countLeapYears(dt1)

	# SIMILARLY, COUNT TOTAL NUMBER OF DAYS BEFORE 'dt2'

	n2 = dt2.y * 365 + dt2.d
	for i in range(0, dt2.m - 1):
		n2 += monthDays[i]
	n2 += countLeapYears(dt2)

	# return difference between two counts
	return (n2 - n1)


# Driver program
#dt1 = Date(10, 12, 2018)
#dt2 = Date(25, 2, 2019)

#print(getDifference(dt1, dt2), "days")
def time_convert(time):
    return int(time[0])*10+int(time[1]),int(time[3])*10+int(time[4])
def date_convert(time):
    return int(time[0])*10+int(time[1]),int(time[3])*10+int(time[4]),int(time[6])*1000+int(time[7])*100+int(time[8])*10+int(time[9])
now = datetime.now()
datenow= now.strftime("%d/%m/%Y")
timenow=now.strftime("%H:%M:%S")    
time2="05:18:31"
time1=timenow
s,r=time_convert(time1)
p,k=time_convert(time2)
print(s,r,p,k)
timer=difference(s,r,p,k)
print(timer)
date1="28/04/2021"
date2=datenow
a,b,c=date_convert(date1)
d,e,f=date_convert(date2)
print(a,b,c,d,e,f)
dt1 = Date(a,b,c)
dt2 = Date(d,e,f)
date_hr=getDifference(dt1, dt2)*24
print(date_hr+timer)
    