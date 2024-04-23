"""
Leafy Legions: DatabaseManager

This module contains the DatabaseManager class
for managing the communication to Supabase
"""

# Library Imports
import bcrypt
import supabase


class DatabaseManager:
    """
    A class to manage the connection to the database.
    """

    def __init__(self, supabase_url: str, supabase_key: str) -> None:
        """
        Initialize the DatabaseManager using supabase login

        Args:
            supabase_url (str): The supabase URL to connect to
            supabase_key (str): The supabase API key
        """
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.client = supabase.Client(supabase_url, supabase_key)
        print("Initialized Database Connection")

        # Caching to prevent spamming API calls
        self.high_scores_cache = []
        self.user_login_cache = {}

    def get_high_scores(self) -> list[dict[str, str | int]]:
        """
        Fetch all high scores from the database in sorted order.

        Returns:
            list[dict[str, str | int]]: A list of dictionaries containing username and high score.
        """
        if self.high_scores_cache:
            return self.high_scores_cache

        res = (self.client.table('users')
               .select('username', 'high_score')
               .order('high_score', desc=True)
               .execute())

        # Update cache
        self.high_scores_cache = res.data

        return self.high_scores_cache

    def create_user(self, username: str, password: str) -> bool:
        """
        Create a new user with a username, password (hashed), and default high score of 0.

        Args:
            username (str): The username of the new user.
            password (str): The password of the new user.

        Returns:
            bool: True if the user was created, False is the user already exists
        """

        if username == '' or password == '':
            return False

        # Check if that username already exists
        res = (self.client.table('users')
               .select('username')
               .eq('username', username)
               .execute())

        if len(res.data) > 0:
            return False

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Create the user using the hashed password
        res = self.client.table('users').insert({
            'username': username,
            'password': hashed_password,
            'high_score': 0
        }).execute()

        if len(res.data) > 0:
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

        if username == '' or password == '':
            return False

        # Find the password of the supplied username
        if username in self.user_login_cache:
            stored_hash = self.user_login_cache[username]
        else:
            # Find the password of the supplied username
            res = (self.client.table('users')
                   .select('password')
                   .eq('username', username)
                   .execute())

            # If no password was found, return False
            if len(res.data) == 0:
                return False

            # Grab the hashed password returned
            stored_hash = res.data[0]["password"]

            # Cache the login data
            self.user_login_cache[username] = stored_hash

        # Use bcrypt to compare hashes and return True/False
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
        res = (self.client.table('users')
               .update({
                    'high_score': new_high_score
                })
               .eq('username', username)
               .execute())

        # Update cache if necessary
        if len(res.data) > 0:
            for user in self.high_scores_cache:
                if user['username'] == username:
                    user['high_score'] = new_high_score

            # Sort cached data
            self.high_scores_cache.sort(key=lambda x: x['high_score'], reverse=True)

        return len(res.data) > 0
