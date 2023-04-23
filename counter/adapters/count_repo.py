from typing import List
import mysql.connector
from typing import List
from domain.models import ObjectCount
from domain.ports import ObjectCountRepo


class CountInMemoryRepo(ObjectCountRepo):

    def __init__(self):
        self.store = dict()

    def read_values(self, object_classes: List[str] = None) -> List[ObjectCount]:
        if object_classes is None:
            return list(self.store.values())

        return [self.store.get(object_class) for object_class in object_classes]

    def update_values(self, new_values: List[ObjectCount]):
        for new_object_count in new_values:
            key = new_object_count.object_class
            try:
                stored_object_count = self.store[key]
                self.store[key] = ObjectCount(
                    key, stored_object_count.count + new_object_count.count)
            except KeyError:
                self.store[key] = ObjectCount(key, new_object_count.count)


class CountMySQLRepo(ObjectCountRepo):

    def __init__(self, host, port, username, password, database):
        """
        Initializes a CountMySQLRepo object and establishes a connection to the specified MySQL database.

        Args:
        - host: A string representing the database host address.
        - port: An integer representing the database port number.
        - username: A string representing the database username.
        - password: A string representing the database user's password.
        - database: A string representing the name of the database to connect to.
        """
        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__database = database
        self.__connection = mysql.connector.connect(
            host=self.__host,
            port=self.__port,
            user=self.__username,
            password=self.__password,
            database=self.__database
        )

    def read_values(self, object_classes: List[str] = None) -> List[ObjectCount]:
        """
        Retrieves object count values from the connected MySQL database.

        Args:
        - object_classes: A list of strings representing the names of the objects to fetch counts for.
        If None is provided, all objects in the database will be returned.

        Returns:
        - A list of ObjectCount objects representing the object counts in the database.
        """
        cursor = self.__connection.cursor()
        try:
            query = f"SELECT * FROM objectcounts"
            cursor.execute(query)
            result = cursor.fetchall()
            object_counts = [ObjectCount(row[0], row[1]) for row in result]
            return object_counts
        except Exception as e:
            self.__logger.error(
                f"Error occurred while reading from database: {e}")
            raise e

    def update_values(self, new_values: List[ObjectCount]):
        """
        Updates object count values in the connected MySQL database.

        Args:
        - new_values: A list of ObjectCount objects representing the new object counts to be updated
        in the database.
        """
        cursor = self.__connection.cursor()
        try:
            for values in new_values:
                objectname = str(values.object_class)
                count = int(values.count)
                fetch_qureay = "SELECT * FROM objectcounts where objectname= %s"
                val = (objectname,)
                cursor.execute(fetch_qureay, val)
                myresult = cursor.fetchall()
                if myresult:
                    old_count = int(myresult[0][1])
                    new_count = old_count+1
                    update_query = "UPDATE objectcounts SET count = %s WHERE objectname = %s"
                    val = (new_count, objectname,)
                    cursor.execute(update_query, val)
                else:
                    insert_query = "INSERT INTO objectcounts(objectname, count) VALUES( %s,%s)"
                    val = (objectname, count)
                    cursor.execute(insert_query, val)
            self.__connection.commit()
        except Exception as e:
            self.__logger.error(f"Error occurred while updating database: {e}")
            raise e
        finally:
            cursor.close()
