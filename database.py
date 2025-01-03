from pymongo import MongoClient
import pandas as pd
from datetime import datetime

class Database:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['vocaldiagnose']
        
    def save_user(self, user_data):
        users = self.db['users']
        user_data['created_at'] = datetime.now()
        return users.insert_one(user_data)
    
    def save_test_result(self, user_id, test_data):
        results = self.db['test_results']
        test_data['user_id'] = user_id
        test_data['created_at'] = datetime.now()
        return results.insert_one(test_data)
    
    def get_user_history(self, user_id):
        results = self.db['test_results']
        history = results.find({'user_id': user_id})
        return pd.DataFrame(list(history))
    
    def get_user_profile(self, user_id):
        users = self.db['users']
        return users.find_one({'_id': user_id})
    
    def update_user_profile(self, user_id, update_data):
        users = self.db['users']
        return users.update_one(
            {'_id': user_id},
            {'$set': update_data}
        )

class MockDatabase:
    def __init__(self):
        self.users = {}
        self.test_results = []
    
    def save_user(self, user_data):
        user_id = len(self.users) + 1
        self.users[user_id] = user_data
        return user_id
    
    def save_test_result(self, user_id, test_data):
        test_data['user_id'] = user_id
        test_data['created_at'] = datetime.now()
        self.test_results.append(test_data)
        return len(self.test_results)
    
    def get_user_history(self, user_id):
        user_results = [r for r in self.test_results if r['user_id'] == user_id]
        return pd.DataFrame(user_results)
    
    def get_user_profile(self, user_id):
        return self.users.get(user_id)