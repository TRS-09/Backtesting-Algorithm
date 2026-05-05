class animal:
    def __init__(self,breed,size):
        self.breed = breed
        self.size = size

    def speak(self):
        print(self.breed)
    


dog = animal("pitbull","small")
dog2 = animal("great dane","big")

print(dog.breed)
print(dog2.breed,dog2.size)

dog2.speak()
dog.speak()