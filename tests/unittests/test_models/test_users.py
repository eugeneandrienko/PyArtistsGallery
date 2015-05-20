"""Tests description of "users" table in database."""

import hashlib
import unittest

from pagapp.models.users import Users


class UsersTableTestCase(unittest.TestCase):
    """Tests for pagapp.models.Users class which describes DB table.

    Test cases:
    test_service_methods -- tests Users constructor and __repr__
    function.
    test_service_login_methods -- tests special methods, which uses by
    flask_login.
    test_password_operations -- tests methods, which works with passwords.
    """

    def test_service_methods(self):
        """Test for Users constructor and __repr__ function.

        Test cases:
        All constructor's parameters is ok.
        Return value of __repr__() function should contain parameters,
        given to constructor.
        Constructor should raise TypeError exception if one or more
        parameters are not strings.
        """
        test_arguments = ('nickname', 'password', True)
        test_user = Users(*test_arguments)
        self.assertTupleEqual((test_arguments[0], test_arguments[2]),
                              (test_user.nickname, test_user.active),
                              msg="Login and password should be equal!")

        wrong_arguments_array = [(1, 'password', True),
                                 ('nickname', 1, False),
                                 ('nickname', 'password', True),
                                 ('nickname', 'password', 1)]
        for wrong_arguments in wrong_arguments_array:
            self.assertRaises(TypeError, Users.__init__, *wrong_arguments,
                              msg="TypeError should be raised!")

    def test_service_login_methods(self):
        """Test for methods, which uses by flask_login.

        Test cases:
        Static method is_authenticated() should return True and static
        method is_anonymous() should return False.
        Method is_active() should return self.active field.
        Method get_id() should return string representation of self.id
        field.
        """
        active_field = True
        test_user = Users('nickname', 'password', active_field)
        self.assertTrue(test_user.is_authenticated(),
                        msg="User should be authenticated!")
        self.assertFalse(test_user.is_anonymous(),
                         msg="User shouldn't be anonymous!")
        self.assertEqual(test_user.is_active(), active_field,
                         msg="User's active field and is_active() not equal!")
        string_id = str(test_user.id)
        self.assertEqual(test_user.get_id(), string_id,
                         msg="User's ID string representation is wrong!")

    def test_password_operations(self):
        """Test for methods, which work with passwords.

        Test cases:
        Method check_password() should return True if given plain password
        plus saved salt have match with saved hashed password. And it should
        return False if plain password does not have match.
        Method check_password() should raise TypeError exception if it get
        non-string object.
        Method set_new_password() should save hashed password and salt in
        internal structures of Users class. Plain password + salt from object
        of Users class should be equal with hashed password from object of
        Users class.
        """
        plain_password = 'Very big secret'
        test_user = Users('nickname', plain_password, True)

        self.assertTrue(test_user.check_password(plain_password),
                        msg="Password is valid!")
        self.assertFalse(test_user.check_password('wrong password'),
                         msg="Password is not valid!")
        self.assertRaises(TypeError, test_user.check_password, 1,
                          msg="Should raise TypeError if password not string.")

        test_user = Users('nickname', 'fake_password', True)
        test_user.set_new_password(plain_password)
        hashed_password = hashlib.sha512(
            plain_password.encode('utf-8') +
            test_user.salt.encode('utf-8')).hexdigest()
        self.assertEqual(hashed_password, test_user.password,
                         msg="Hashed passwords should be equal!")


if __name__ == '__main__':
    unittest.main()
