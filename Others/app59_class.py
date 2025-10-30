class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(f"{self.name} says Hi!")


dog1 = Dog("Buddy", 1)
dog2 = Dog("Not Buddy", 2)

dog1.bark()
dog2.bark()
Dog.bark(dog1)
print(dog1.name)
