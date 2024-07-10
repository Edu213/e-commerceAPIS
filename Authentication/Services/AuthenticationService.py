"""
This script defines an AuthenticationService class responsible for user registration and login logic.

It utilizes an AuthenticationModel to interact with the database for user registration and login.

The register_user method registers a new user by generating a unique user ID, hashing the password, and inserting user data into the database.

The generate_password_token method generates a secure password token using SHA-256 hash algorithm.

The insert_user_data method inserts user data into the database.

The login_user method handles user login by verifying the email and password against the database.

Usage:
    Import this script and create an instance of AuthenticationService to register and login users.

Dependencies:
    - AuthenticationModel class for database interaction
    - LoggerBase module for logging
    - hashlib module for hashing passwords
"""

from Models.AuthenticationModel import AuthenticationModel
from Logger.LoggerBase import log
import hashlib

class AuthenticationService:
    def __init__(self):
        """
        Initializes the AuthenticationService with an instance of AuthenticationModel.
        """
        self.authentication_model = AuthenticationModel()
    

    def register_user(self, data):
        """
        Registers a new user by generating a unique user ID, hashing the password,
        and inserting user data into the database.

        Args:
            data (dict): User data including email and password.

        Returns:
            int: User ID of the registered user.
        """
        try:
            self.authentication_model.connect_to_database()
            
            last_user = self.authentication_model.db.users.find().sort("_id", -1).limit(1)
            if last_user:
                last_id = last_user[0]["_id"]
                user_id = last_id + 1
            else:
                user_id = 1

            password_token = self.generate_password_token(data['password'])

            self.insert_user_data(user_id, data['email'], password_token)

            return user_id
        except Exception as e:
            log.critical(f'Failed to register user: {e}')
            raise
        finally:
            self.authentication_model.close_connection()

    def generate_password_token(self, password):
        """
        Generates a secure password token using SHA-256 hash algorithm.

        Args:
            password (str): Password to be hashed.

        Returns:
            str: Hashed password token.
        """
        password_bytes = password.encode('utf-8')
        password_hash = hashlib.sha256(password_bytes).digest()
        return hashlib.blake2b(password_hash, digest_size=16).hexdigest()

    def insert_user_data(self, user_id, email, password_token):
        """
        Inserts user data into the database.

        Args:
            user_id (int): Unique ID of the user.
            email (str): Email address of the user.
            password_token (str): Hashed password token.
        """
        try:
            user_data = {
                '_id': user_id,
                'email': email,
                'password_token': password_token 
            }
            self.authentication_model.db.users.insert_one(user_data)
        except Exception as e:
            log.critical(f'Failed to insert user data into MongoDB: {e}')
            raise
        
    def login_user(self, email, password):
        """
        Handles user login by verifying the email and password against the database.

        Args:
            email (str): Email address of the user.
            password (str): Password provided by the user.

        Returns:
            int or None: User ID if login is successful, None otherwise.
        """
        try:
            self.authentication_model.connect_to_database()

            user = self.authentication_model.db.users.find_one({'email': email})

            if user:
                password_token = self.generate_password_token(password)

                if password_token == user['password_token']:
                    return user['_id'] 
                else:
                    return None
            else:
                return None 
        except Exception as e:
            log.critical(f'Failed to login user: {e}')
            raise
        finally:
            self.authentication_model.close_connection()
            
    def delete_user(self, email, password, user_id, confirm):
        """
        Deletes a user from the system.

        Args:
            email (str): Email address of the user.
            password (str): Password provided by the user.
            user_id (int): ID of the user to be deleted.
            confirm (str): Confirmation string, should be 'yes'.

        Returns:
            str: Message indicating the success of deletion.
        """
        if confirm != 'yes':
            raise ValueError("Confirmation string must be 'yes'")

        try:
            self.authentication_model.connect_to_database()

            user = self.authentication_model.db.users.find_one({'_id': user_id, 'email': email})

            if user:
                password_token = self.generate_password_token(password)
                if password_token == user['password_token']:
                    self.authentication_model.db.users.delete_one({'_id': user_id})
                    return "User successfully deleted"
                else:
                    raise ValueError("Unauthorized: Incorrect password")
            else:
                raise ValueError("User not found")
        except Exception as e:
            log.critical(f'Failed to delete user: {e}')
            raise
        finally:
            self.authentication_model.close_connection()
