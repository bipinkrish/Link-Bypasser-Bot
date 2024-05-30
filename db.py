import requests
import base64

class DB:
    def __init__(self, api_key, db_owner, db_name) -> None:
        self.api_key = api_key
        self.db_owner = db_owner
        self.db_name = db_name
        self.url = "https://api.dbhub.io/v1/tables"
        self.data = {
            "apikey": self.api_key,
            "dbowner": self.db_owner,
            "dbname": self.db_name
        }

        response = requests.post(self.url, data=self.data)
        if response.status_code == 200:
            if "results" not in response.json():
                raise Exception("Error, Table not found")
        else:
            raise Exception("Error in Auth")

    def insert(self, link: str, result: str):
        url = "https://api.dbhub.io/v1/execute"
        sql_insert = f"INSERT INTO results (link, result) VALUES ('{link}', '{result}')"
        encoded_sql = base64.b64encode(sql_insert.encode()).decode()
        self.data["sql"] = encoded_sql
        response = requests.post(url, data=self.data)
        if response.status_code == 200:
            if response.json()["status"] != "OK":
                raise Exception("Error while inserting")
            return True
        else:
            print(response.json())
            return None
    
    def find(self, link: str):
        url = "https://api.dbhub.io/v1/query"
        sql_select = f"SELECT result FROM results WHERE link = '{link}'"
        encoded_sql = base64.b64encode(sql_select.encode()).decode()
        self.data["sql"] = encoded_sql
        response = requests.post(url, data=self.data)
        if response.status_code == 200:
            try: return response.json()[0][0]["Value"]
            except: return None
        else:
            print(response.json())
            return None
