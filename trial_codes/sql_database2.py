# Simple Python program to compare dates
import datetime
# importing datetime module
DATE="29/04/2021"
DATE1="31/04/2021"
d1 = datetime.datetime(int(str(DATE[6])+str(DATE[7])+str(DATE[8])+str(DATE[9])),int(str(DATE[3])+str(DATE[4])),int(str(DATE[0])+str(DATE[1])))
d2 = datetime.datetime(int(str(DATE1[6])+str(DATE1[7])+str(DATE1[8])+str(DATE1[9])),int(str(DATE1[3])+str(DATE1[4])),int(str(DATE1[0])+str(DATE1[1])))