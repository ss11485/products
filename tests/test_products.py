# Copyright 2016, 2017 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Pet Model

Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from app.productmodel import Product, ValidationError, db
from app import app

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestPets(unittest.TestCase):
    """ Test Cases for Pets """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        Pet.init_db(app)
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_pet(self):
        """ Create a pet and assert that it exists """
        pet = Pet(name="fido", category="dog", available=True)
        self.assertTrue(pet != None)
        self.assertEqual(pet.id, None)
        self.assertEqual(pet.name, "fido")
        self.assertEqual(pet.category, "dog")
        self.assertEqual(pet.available, True)

    def test_add_a_pet(self):
        """ Create a pet and add it to the database """
        pets = Pet.all()
        self.assertEqual(pets, [])
        pet = Pet(name="fido", category="dog", available=True)
        self.assertTrue(pet != None)
        self.assertEqual(pet.id, None)
        pet.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(pet.id, 1)
        pets = Pet.all()
        self.assertEqual(len(pets), 1)

    def test_update_a_product(self):
        """ Update a Product """
        product = Product(1, "Couch", "White couch", "Furniture", 200, "Boxed", 50, " ", 8)
        product.save()
        self.assertEqual(product.id, 1)
        # Change it and save it
        product.category = "Home"
        product.save()
        self.assertEqual(product.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].category, "Home")

    def test_delete_a_product(self):
        """ Delete a Product """
        product = Product(1, "Couch", "White couch", "Furniture", 200, "Boxed", 50, " ", 8)
        product.save()
        self.assertEqual(len(Product.all()), 1)
        # delete the product and make sure it isn't in the database
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_serialize_a_pet(self):
        """ Test serialization of a Pet """
        pet = Pet(name="fido", category="dog", available=False)
        data = pet.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], None)
        self.assertIn('name', data)
        self.assertEqual(data['name'], "fido")
        self.assertIn('category', data)
        self.assertEqual(data['category'], "dog")
        self.assertIn('available', data)
        self.assertEqual(data['available'], False)

    def test_deserialize_a_pet(self):
        """ Test deserialization of a Pet """
        data = {"id": 1, "name": "kitty", "category": "cat", "available": True}
        pet = Pet()
        pet.deserialize(data)
        self.assertNotEqual(pet, None)
        self.assertEqual(pet.id, None)
        self.assertEqual(pet.name, "kitty")
        self.assertEqual(pet.category, "cat")
        self.assertEqual(pet.available, True)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        pet = Pet()
        self.assertRaises(DataValidationError, pet.deserialize, data)

    def test_find_pet(self):
        """ Find a Pet by ID """
        Pet(name="fido", category="dog", available=True).save()
        kitty = Pet(name="kitty", category="cat", available=False)
        kitty.save()
        pet = Pet.find(kitty.id)
        self.assertIsNot(pet, None)
        self.assertEqual(pet.id, kitty.id)
        self.assertEqual(pet.name, "kitty")
        self.assertEqual(pet.available, False)

    def test_find_by_category(self):
        """ Find Pets by Category """
        Pet(name="fido", category="dog", available=True).save()
        Pet(name="kitty", category="cat", available=False).save()
        pets = Pet.find_by_category("cat")
        self.assertEqual(pets[0].category, "cat")
        self.assertEqual(pets[0].name, "kitty")
        self.assertEqual(pets[0].available, False)

    def test_find_by_name(self):
        """ Find a Pet by Name """
        Pet(name="fido", category="dog", available=True).save()
        Pet(name="kitty", category="cat", available=False).save()
        pets = Pet.find_by_name("kitty")
        self.assertEqual(pets[0].category, "cat")
        self.assertEqual(pets[0].name, "kitty")
        self.assertEqual(pets[0].available, False)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
