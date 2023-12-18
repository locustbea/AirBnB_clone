#!/usr/bin/python3
"""Defines unittests for models/amenity.py"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Amenity class."""

    def test_no_args_instantiates(self):
        """Test newly created object for correct type"""
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance_stored_in_objects(self):
        """Test for created object presence in dict"""
        self.assertIn(Amenity(), models.storage.all().values())

    def test_id_is_public_str(self):
        """Test for public id and string type"""
        self.assertEqual(str, type(Amenity().id))

    def test_created_at_is_public_datetime(self):
        """Test for datetime object using created at attribute"""
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_updated_at_is_public_datetime(self):
        """Test for datetime object using update at attribute"""
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_is_public_class_attribute(self):
        """Test for class & instance access & distinction"""
        am = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", am.__dict__)

    def test_two_amenities_unique_ids(self):
        """Test for unique IDs for two objects"""
        am1 = Amenity()
        am2 = Amenity()
        self.assertNotEqual(am1.id, am2.id)

    def test_two_amenities_different_created_at(self):
        """Test for created at timestamp for two objects"""
        am1 = Amenity()
        sleep(0.05)
        am2 = Amenity()
        self.assertLess(am1.created_at, am2.created_at)

    def test_two_amenities_different_updated_at(self):
        """Test for updated at timestamp for two objects"""
        am1 = Amenity()
        sleep(0.05)
        am2 = Amenity()
        self.assertLess(am1.updated_at, am2.updated_at)

    def test_str_representation(self):
        """Test for string representation for object"""
        dt = datetime.today()
        dt_repr = repr(dt)
        am = Amenity()
        am.id = "123456"
        am.created_at = am.updated_at = dt
        amstr = am.__str__()
        self.assertIn("[Amenity] (123456)", amstr)
        self.assertIn("'id': '123456'", amstr)
        self.assertIn("'created_at': " + dt_repr, amstr)
        self.assertIn("'updated_at': " + dt_repr, amstr)

    def test_args_unused(self):
        """Test for object internal state with ab attribute"""
        am = Amenity(None)
        self.assertNotIn(None, am.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test for instantiation with kwargs test method"""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        am = Amenity(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(am.id, "345")
        self.assertEqual(am.created_at, dt)
        self.assertEqual(am.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """Test for proper error handling for invalid keyword"""
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)


class TestAmenity_save(unittest.TestCase):
    """Unittests for testing save method of the Amenity class."""

    @classmethod
    def setUp(self):
        """Renames json to tmp on each test only"""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        """Removes json & renames tmp on each test"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        """Checks updated_at timestamp in object"""
        am = Amenity()
        sleep(0.05)
        first_updated_at = am.updated_at
        am.save()
        self.assertLess(first_updated_at, am.updated_at)

    def test_two_saves(self):
        """"Verifies multiple updates of updated_at timestamp"""
        am = Amenity()
        sleep(0.05)
        first_updated_at = am.updated_at
        am.save()
        second_updated_at = am.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        am.save()
        self.assertLess(second_updated_at, am.updated_at)

    def test_save_with_arg(self):
        """Checks error handling when passing arg to save method"""
        am = Amenity()
        with self.assertRaises(TypeError):
            am.save(None)

    def test_save_updates_file(self):
        """Verifies data written in "file.json" storage file"""
        am = Amenity()
        am.save()
        amid = "Amenity." + am.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())


class TestAmenity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Amenity class."""

    def test_to_dict_type(self):
        """Verifies return type of to_dict"""
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Check generated dict for necessary keys"""
        am = Amenity()
        self.assertIn("id", am.to_dict())
        self.assertIn("created_at", am.to_dict())
        self.assertIn("updated_at", am.to_dict())
        self.assertIn("__class__", am.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Check for custom attributes"""
        am = Amenity()
        am.middle_name = "Holberton"
        am.my_number = 98
        self.assertEqual("Holberton", am.middle_name)
        self.assertIn("my_number", am.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """Check datetime attribute conversion to string in dict"""
        am = Amenity()
        am_dict = am.to_dict()
        self.assertEqual(str, type(am_dict["id"]))
        self.assertEqual(str, type(am_dict["created_at"]))
        self.assertEqual(str, type(am_dict["updated_at"]))

    def test_to_dict_output(self):
        """Test dict output format"""
        dt = datetime.today()
        am = Amenity()
        am.id = "123456"
        am.created_at = am.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(am.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        """Compare to_dict and __dict___ for difference"""
        am = Amenity()
        self.assertNotEqual(am.to_dict(), am.__dict__)

    def test_to_dict_with_arg(self):
        """Checks arg to to_dict for error handling"""
        am = Amenity()
        with self.assertRaises(TypeError):
            am.to_dict(None)


if __name__ == "__main__":
    unittest.main()
