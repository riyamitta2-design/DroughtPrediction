print("Hello world")

temp = 78
rainfall = 3.12
city = "novi"
print(not (temp>60 or rainfall>10))
rainfall+=0.1

#name = input("Enter your name: ")
#age = int(input("Enter your age: "))
#print(age+10)
print(2)
temps = [70,60,80,110,112,112]

for i in range(0,3):
    print(temps[i])

for i in temps:
    print(i)

for i in range(10,-1,-1):
    print(i)

if rainfall<10:
    print("drought")

elif rainfall<5:
    print("possible drought")

else:
    print("not at risk")


    
def temp_check(temp):
    if temp>30:
        return "hot"
    else:
        return "not hot"

def num_hot_days(temps):
    count = 0
    for i in temps:
        if i>100:
            count+=1
    return count

#drought_check(105, 2)
print(num_hot_days(temps))


student = {
    "name": "Riya",
    "age" : 15,
    "grade": 10
}
print(student["name"])
student["id"] = 123

if "id" not in student:
    student["id"] = 456
print(student)

for i in student:
    print(i,student[i])

for value in student.values():
    print(value)

for key,value in student.items():
    print(key,value)

weather = {
    "rainfall": 25,
    "temperature": 40
}

def predict_drought(dict):
    if dict["rainfall"]<5 and dict["temperature"]>100:
        print("drought")
    elif dict["rainfall"]<10 and dict["temperature"]>80:
        print("possible drought")
    else:
        print("not possible")

predict_drought(weather)

weather_data = {
    "Delhi": {
        "rainfall": 25,
        "temperature": 40
    },
    "Mumbai": {
        "rainfall": 120,
        "temperature": 30
    },
    "Banglore": {
        "rainfall": 150,
        "temperature" : 50
    }
}

print(weather_data["Delhi"]["rainfall"])
sum = 0
min = 1000
min_temp_city = ""
for key in weather_data:
    if(weather_data[key]["temperature"]<min):
        min = weather_data[key]["temperature"]
        min_temp_city = key
    print (key , weather_data[key]["rainfall"])
    sum+=weather_data[key]["rainfall"]
    print(sum)
print("Avg rainfall: " , sum/len(weather_data))
print("Min temp: ", min_temp_city + ": " , min , weather_data[min_temp_city]["rainfall"])


weather_data2 = {
    "Delhi": {
        "rainfall": [20, 35, 10, 0, 45],
        "temperature": [38, 39, 41, 42, 40],
        "humidity": [30, 28, 25, 20, 27]
    },
    "Mumbai": {
        "rainfall": [120, 110, 95, 130, 100],
        "temperature": [30, 31, 32, 30, 29],
        "humidity": [80, 82, 85, 79, 81]
    },
    "Chennai": {
        "rainfall": [50, 40, 35, 20, 10],
        "temperature": [34, 35, 36, 37, 38],
        "humidity": [60, 58, 55, 50, 48]
    },
    "Jaipur": {
        "rainfall": [5, 0, 10, 15, 8],
        "temperature": [42, 43, 44, 41, 40],
        "humidity": [18, 20, 17, 19, 21]
    }
}

def avg(city, feature, dict):
    sum = 0
    for i in dict[city][feature]:
        sum+=i
    return sum/len(dict[city][feature])

print(avg("Jaipur", "rainfall", weather_data2))

def num_possible_drought(dict):
    for key in dict:
        print(key)
        drought = 0
        dict[key]["risk"] = []
        print(dict)
        for i in range(5):
            if drought_check(dict[key]["rainfall"][i] ,dict[key]["temperature"][i]) == "drought":
                drought+=1
                dict[key]["risk"].append("drought")

            elif drought_check(dict[key]["rainfall"][i], dict[key]["temperature"][i]) == "possible drought":
                dict[key]["risk"].append("possible drought")
            else:
                dict[key]["risk"].append("no risk")
        
        print(dict)
        


def drought_check(rainfall, temp):
    if rainfall<5 and temp_check(temp)=="hot":
        return ("drought")
    elif rainfall<10:
        return ("possible drought")
    else:
        return ("no risk")
num_possible_drought(weather_data2) 