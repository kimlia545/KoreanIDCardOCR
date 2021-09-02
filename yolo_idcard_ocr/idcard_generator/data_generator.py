import random
from faker import Faker # pip install Faker

# fake name, address
fake = Faker("ko_KR")
nf = open("./name.txt", 'w', encoding='utf-8')
ad = open("./address.txt", 'w', encoding='utf-8')

for _ in range(1000):
    nf.write(fake.name()+'\n')
    ad.write(fake.address()+'\n') # 전라북도 영월군 서초중앙길 (정남김이읍)
nf.close()
ad.close()

import datetime
import random
import time

# fake issue date
start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2021, 12, 31)

time_between_dates = end_date - start_date
days_between_dates = time_between_dates.days

df = open("./date.txt", 'w', encoding='utf-8')
for _ in range(1000):
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    random_date = str(random_date).replace('-','.')
    df.write(random_date+'\n')
df.close()

# fake resident registration number
rf = open("./number.txt", 'w', encoding='utf-8')
for i in range(1000):
    for i in range(1,7):
        num = ""
        num += str(random.randrange(0, 10)) 
        num += str(random.randrange(0, 10)) 
        num += str(random.randrange(0, 2)) # if 0 1-9 else 0 - 2
        num += str(random.randrange(0, 10)) 
        num += str(random.randrange(1, 4)) # 2 0 if 2 
        num += str(random.randrange(0, 10)) 
    for j in range(1,8):
        num2 = ""
        num2 += str(random.randrange(0, 10)) 
        num2 += str(random.randrange(0, 10)) 
        num2 += str(random.randrange(0, 10)) 
        num2 += str(random.randrange(0, 10)) 
        num2 += str(random.randrange(0, 10))  
        num2 += str(random.randrange(0, 10)) 
        num2 += str(random.randrange(0, 10)) 
    rf.write(str(num)+'-'+str(num2)+'\n')
rf.close()


'''
def str_time_prop(start, end, time_format, prop):

    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y', prop)
print(random_date("1/1/1980", "1/1/2021", random.random()))
'''


'''
# fake korean name
first_name_samples = "김이박최강조윤장임한오서신권황안송류홍고문양손배조"
middle_name_samples = "유정민서예지도하주윤채현지강동현재순수혜선미상경종승"
last_name_samples = "준윤우원호후서연아은진훈호민현수남웅석순숙길일연람혜"

f = open("./name.txt", 'w', encoding='utf-8')
for i in range(1, 10):
    name = ""
    name += random.choice(first_name_samples)
    name += random.choice(middle_name_samples)
    name += random.choice(last_name_samples)
    f.write(name+'\n')
f.close()
'''