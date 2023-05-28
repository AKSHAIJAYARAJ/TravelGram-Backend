# MODULE DETAILS
# __________________________________________________________________________________________________________________________
# MODULE NAME   : PsqlExecutor
# VERSION       : 1.0
# SYNOPSYS      : This module is developed to execute postgres queries.
# AUTHOR        : AKSHAI JAYARAJ
# CREATED ON    : 2023-MAY-01
# METHODS       : 
# 
# ENHANCEMENT HISTORY
# __________________________________________________________________________________________________________________________
# AUTHOR        : <AUTHOR>
# CREATED ON    : <CREATED ON>
# METHODS       : <METHODS>
# __________________________________________________________________________________________________________________________

import psycopg2

class PsqlExecutor:

    def _init_(self):
        self.connection = self.connect()

    def connect(self):

        connection = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            port=self.port)
        self.cursor = connection.cursor()

        return connection
    def disconnect(self):

        self.cursor.close()
        self.connection.close()

    def query_executer(self, query):

        try:
            self.cursor.execute(query=query)
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print("psql-exec-Exception : ",e)
        finally:
            self.disconnect()
    def select(self, query):
        try:
            self.cursor.execute(query=query)
            values = self.cursor.fetchall()
            field_names = [desc[0] for desc in self.cur.description]
            result = list()
            for row in values:
                row_list = list(row)
                result.append(dict(zip(field_names, row_list))) 
            return result
        except Exception as e:
            print("psql-exec-Exception : ",e)
        finally:
            self.disconnect()
    def insert(self, query):
        self.execute_query(query)

    def update(self,query):
        self.execute_query(query)

    def delete(self, query):
        self.execute_query(query)