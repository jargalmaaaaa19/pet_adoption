class Pet:
    def __init__(self, name: str, species: str, age: int, is_adopted: bool = False):
        if age < 0:
            raise ValueError("Амьтны нас сөрөг байж болохгүй")
        self.name = name
        self.species = species
        self.age = age
        self.is_adopted = is_adopted

    def adopt(self):
        if self.is_adopted:
            raise ValueError("Энэ амьтан хэдийнээ үрчлэгдсэн байна")
        self.is_adopted = True

    def __str__(self):
        return f"{self.species}: {self.name} ({self.age} настай)"


class AdoptionRequest:
    def __init__(self, pet: Pet, adopter_name: str, adopter_email: str):
        self.pet = pet
        self.adopter_name = adopter_name
        self.adopter_email = adopter_email
        self.status = "Pending"

    def approve(self):
        self.pet.adopt()
        self.status = "Approved"
