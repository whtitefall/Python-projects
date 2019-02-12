import csv 

with open('ex.csv', 'w') as f :
    writer = csv.writer(f)
    writer.writerow(['time','tmp','volts'])
   

