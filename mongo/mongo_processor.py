import json

from datetime import datetime
from pymongo import MongoClient


class MongoProcessor:
    def __init__(
            self, 
            button_mapping: dict[str, str] = None,
            mongo_host: str = "localhost",
            mongo_port: int = 27017):
        """
        ### Class Summary
        This class is used for interacting with a MongoDB database. Specifically, it
        should take in data from a microcontroller/arduino/rpi and log it in a users
        collection.

        ---
        ### Parameters
        - button_mapping (dict[str, str]): mapping of buttons to specific states.
          Defaults to None.
        - mongo_host (str): IP address of the MongoDB server.
          Defaults to "localhost"
        - mongo_port (int): Port number that the MongoDB server uses.
          Defaults to 27017.
        
        ---
        ### Return
        Void
        """
        self.button_mapping: dict[str, str] = button_mapping
        # if no button input is given, then set these defaults
        if button_mapping is None:
            self.button_mapping = {
                "green": "happy",  # moods
                "white": "neutral",
                "red": "sad",
                "black": "started concentrating",  # concentrations
                "yellow": "stopped concentrating"
            }
        self.button_list = list(self.button_mapping.keys())  # list of all buttons
        # configure MongoDB 
        self.client = MongoClient(mongo_host, mongo_port)  # init mongo connection
        self.db = self.client.PsychTracker  # configure working database
        self.col_list = self.db.list_collection_names()
        self.user_index = self.db['user_indices']  # configure user_indices collection
    
    def add_button_press_data(self, button: str, user: str, emotion: str = None, temp: int = None) -> None:
        """
        ### Function Summary
        Adds button press data (index, button pressed, state, and date) 
        to a users collection.

        ---
        ### Parameters
        - button (str): Button pressed.
        - user (str): Name of the user you want to add the data to.
        - emotion (str, optional): detected emotion if available. Defaults to None.
        - temp (int, optional): detected body temperature if available. Defaults to None.
        
        ---
        ### Return
        Void
        """
        if button not in self.button_list:  # check if the input button exist within the list of buttons
            raise Exception(f"The {button} does not exist in the button list")
        elif user not in self.col_list:  # if user does not exist, raise error
            raise Exception(f"The user *{user}* does not exist in the database")
        user_col = self.db[user]  # configure user collection
        idx: int = self.user_index.find_one()[user.lower()]  # get user index
        data_package: dict[str, str] = {
            "index": idx + 1,
            "button": button,
            "state": self.button_mapping[button],
            "datetime": datetime.now().isoformat()
        }
        # if temperature data is available, add it to the data package
        if temp is not None: 
            data_package["temp"] = temp
        # if emotion data is available, add it to the data package
        if emotion is not None:
            data_package["emotion"] = emotion
        user_col.insert_one(data_package)  # insert data/document into collection
        # increment the index for new the new inserted document
        self.user_index.update_one(
            {user.lower(): idx},
            {"$set": {user.lower(): idx + 1}}
        )

    def add_user(self, user: str) -> None:
        """
        ### Function Summary
        Adds a users collection to the database.

        ---
        ### Parameters
        - user (str): Name of the user you want to add.
        
        ---
        ### Return
        Void
        """
        if user in self.col_list:
            raise Exception("User already exists in the database. Try again\n")
        else:
            self.db.create_collection(user)
            print(f"User {user} successfully added to the database\n")

    def delete_user(self, user: str) -> None:
        """
        ### Function Summary
        Deletes a users collection in the database.

        ---
        ### Parameters
        - user (str): Name of the user you want to delete
        
        ---
        ### Return
        Void
        """
        if user not in self.col_list:
            raise Exception("User does not exist in the database. Try again\n")
        else:
            user_col = self.db[user]  # configure user collection
            user_col.drop()  # delete user/drop collection
            print(f"Successfully deleted user *{user}* from the database")
    
    def import_from_json(self, file_pth: str) -> dict:
        """
        ### Function Summary
        Parses a json file for adding the data to a collection

        ---
        ### Parameters
        - file_pth (str): Path to the json file you want to parse

        ---
        ### Return
        Returns a dictionary with the json file data
        """
        data: dict[str, str] = None
        with open (file_pth, 'r') as f:
            data = json.load(f) 
        return data

    def reset_index(self) -> None:
        """
        ### THIS IS ONLY USED FOR TESTING. It resets the currently loaded indices.
        """
        idx: int = self.user_index.find_one()  # get user index
        self.user_index.update_one(
            {"sophie": idx['sophie']},
            {"$set": {'sophie': 0}}
        )
        self.user_index.update_one(
            {"andrew": idx['andrew']},
            {"$set": {'andrew': 0}}
        )


if __name__ == '__main__':
    mong = MongoProcessor()
    # mong.add_button_press_data('red', 'Andrew')
    # mong.reset_index()