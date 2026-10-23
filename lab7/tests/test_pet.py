import unittest
from lab7.app.models import Pet

class TestPet(unittest.TestCase):
    def setUp(self):
        self.pet = Pet("Банхар", "Нохой", 2)

    def test_pet_creation(self):
        self.assertEqual(self.pet.name, "Банхар")
        self.assertEqual(self.pet.species, "Нохой")
        self.assertEqual(self.pet.age, 2)
        self.assertFalse(self.pet.is_adopted)

    def test_pet_age_validation(self):
        with self.assertRaises(ValueError):
            Pet("Мими", "Муур", -1)

    def test_pet_adoption(self):
        self.pet.adopt()
        self.assertTrue(self.pet.is_adopted)

    def test_already_adopted_pet(self):
        self.pet.adopt()
        with self.assertRaises(ValueError):
            self.pet.adopt()
