from datetime import datetime, date, timedelta


dt1 = datetime.now()
for _ in range(19):
    dt2 = timedelta(days=7)
    delta = dt1 + dt2
    print(delta.strftime("%Y/%m/%d"))
    print(dt1.strftime("%W"))
    dt1 = delta

d1 = "01/05/2020"
d2 = "10/05/2020"
dt3 = datetime.strptime(d1, "%d/%m/%Y")
dt4 = datetime.strptime(d2, "%d/%m/%Y")
print(str(dt4 - dt3)[0])


d4 = datetime.now().strftime("%W")
print(int(d4))

d5 = datetime.strptime(d2, "%d/%m/%Y").strftime("%W")
print(d5)
