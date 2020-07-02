#!/usr/bin/env python3


#importing the necessary modules
import re
import operator
import csv

#declare two dictionaries one for couting the no.of users and other for collecting the count of varius errors
error_type = dict()
user_name = dict()

with open("syslog.log") as fhand:
    for line in fhand.readlines():
        error = re.search(r"ERROR ([\w ]*) ", line)
        uname = re.search(r"\((.+)\)",line)
        if uname[1] not in user_name:
            user_name[uname[1]] = [0]*2 #so that we can store a list of two values as key
        if error is not None:
          error_type[error[1]] = error_type.get(error[1],0)+1
          user_name[uname[1]][1] = user_name.get(uname[1])[1]+1
        else:
          user_name[uname[1]][0] = user_name.get(uname[1])[0]+1
    error = None


#sorting the dictionaries as needed
error_type = dict(sorted(error_type.items(),key=operator.itemgetter(1),reverse=True))
user_name = dict(sorted(user_name.items(),key=operator.itemgetter(0)))


#writing them to csv files using the csv module
csv_file = open("error_message.csv","w")
writer = csv.writer(csv_file)
writer.writerow(["Error","Count"])
for key,value in error_type.items():
    writer.writerow([key,value])
csv_file.close()

csv_file2 = open("user_statistics.csv","w")
writer = csv.writer(csv_file2)
writer.writerow(["Username","INFO","ERROR"])
for key,value in user_name.items():
    writer.writerow([key,value[0],value[1]])  
csv_file2.close()