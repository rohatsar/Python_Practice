names= ["Ali","Ayşe","Mehmet","Zeynep"]
ages =[25, 30, 35, 28]

for index, (name, age) in enumerate(zip(names, ages)):
    print(f"{index} - {name} is {age} years old")