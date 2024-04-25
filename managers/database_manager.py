"""
Leafy Legions: DatabaseManager

This module contains the DatabaseManager class
for managing the communication to Supabase
"""
# Library Imports
import bcrypt
import firebase_admin
from firebase_admin import db, credentials


class DatabaseManager:
    """
    A class to manage the connection to the Firebase database.
    """
    def __init__(self) -> None:
        """
        Initialize the DatabaseManager using Firebase credentials.
        """
        cred = credentials.Certificate("credentials.json")
        firebase_admin.initialize_app(cred,{
            "databaseURL": "https://leafylegions-default-rtdb.firebaseio.com/"
        })

        self.database = db.reference()
        print("Firebase Connected")

        # Caching to prevent spamming API calls
        self.high_scores_cache = []

    def get_high_scores(self) -> list[dict[str, str | int]]:
        """
        Fetch all high scores from the database in descending order.

        Returns:
            list[dict[str, str | int]]: A list of dictionaries containing username and high score.
        """
        if self.high_scores_cache:
            return self.high_scores_cache

        res = self.database.child('user_data').order_by_child('high_score').get()

        if isinstance(res, dict):  # Check if the result is a dictionary
            self.high_scores_cache = []
            for username, user_data in res.items():  # Extract username and user data
                if isinstance(user_data, dict):
                    high_score = user_data.get("high_score", 0)
                    self.high_scores_cache.append({"username": username, "high_score": high_score})
                else:
                    print("Unexpected data structure for user data:", user_data)
        else:
            print("Unexpected data structure in get_high_scores:", res)

        # Sort the high scores in descending order
        self.high_scores_cache = sorted(self.high_scores_cache, key=lambda x: x["high_score"], reverse=True)

        return self.high_scores_cache

    def create_user(self, username: str, password: str) -> bool:
        """
        Create a new user with a username, password (hashed), and default high score of 0.

        Args:
            username (str): The username of the new user.
            password (str): The password of the new user.

        Returns:
            bool: True if the user was created, False if the user already exists or input data is invalid.
        """
        if not username or not password:
            return False

        # Check if that username already exists
        if self.database.child('users').child(username).get():
            return False

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create the user using the hashed password
        self.database.child('users').child(username).set({'password': hashed_password})

        # Create associated data table
        self.database.child('user_data').child(username).set({'high_score': 0})

        return True

    def verify_login(self, username: str, password: str) -> bool:
        """
        Verify a login by comparing the provided password with the hashed password in the database.

        Args:
            username (str): The username of the user.
            password (str): The password to verify.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        if not username or not password:
            return False

        # Find the password of the supplied username
        stored_hash = str(self.database.child('users').child(username).child('password').get())

        if not stored_hash:
            return False

        # Use bcrypt to compare hashes (true means working):
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

    def update_high_score(self, username: str, new_high_score: int) -> bool:
        """
        Update the high score based on the username

        Args:
            username (str): The username of the user.
            new_high_score (int): The new high score to set.

        Returns:
            bool: True if the high score was updated successfully, False otherwise.
        """
        if not username:
            return False

        user_data_ref = self.database.child('user_data').child(username)
        if not user_data_ref.get():
            return False

        user_data_ref.update({'high_score': new_high_score})

        # Update cache if necessary
        user_found = False
        for obj in self.high_scores_cache:
            if obj['username'] == username:
                obj['high_score'] = new_high_score
                user_found = True

        if not user_found:
            self.high_scores_cache.append({
                "username": username,
                "high_score": new_high_score
            })

        # Sort cached data
        self.high_scores_cache.sort(key=lambda x: x['high_score'], reverse=True)

        return True
