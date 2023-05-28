# MODULE DETAILS
# __________________________________________________________________________________________________________________________
# MODULE NAME   : QueryGenerator
# VERSION       : 1.0
# SYNOPSYS      : This module is developed to generate postgres queries dynamically
# AUTHOR        : AKSHAI JAYARAJ
# CREATED ON    : 2023-MAY-01
# METHODS       : - insert : - Input args : projection, table_name 
#                            - Output     : Returns Insert postgres query based on projection and table_name
#                 - select : - Input args : projection, table_name, predicates 
#                            - Output     : Returns select postgres query based on projection , table_name and predicate
#                 - update : - Input args : projection, table_name, predicates 
#                            - Output     : Returns Update postgres query based on projection , table_name and predicate
#                 - delete : - Input args :table_name, predicates 
#                            - Output     : Returns delete postgres query based on table_name and predicate
# ENHANCEMENT HISTORY
# __________________________________________________________________________________________________________________________
# AUTHOR        : <AUTHOR>
# CREATED ON    : <CREATED ON>
# METHODS       : <METHODS>
# __________________________________________________________________________________________________________________________

import datetime

class QueryGenerator:

    def insert(self,projection : list or dict,table_name: str):

        """
        This module generate query based on input args and returns query
        
        Args:

        - projection : Contains field names and values as dictionary. it can be dictionary ot list of dictionaries
        - table _name : Name of the table as string

        Returns:
            - Returns query as string or list based on the number of query generated

        Algorithm:

        1) Get predicate and convert to list if it is not a list
        2) Reformat the data with proper syntax
        3) Construct the query and return

        """

        projection = projection if isinstance(projection,list) else [projection]
        sql_list =list()
        for data in projection:
            query_formatted_values = list()
            fields = ",".join(data.keys())
            values = data.values()
            for value in values:
                if  isinstance(value,str) or isinstance(value,(datetime.date,datetime.datetime)):
                    value = "'"+str(value)+"'" 
                elif isinstance(value,str):
                    value = "'"+str(value)+"'" if value.isnumeric() else str(value)  
                query_formatted_values.append(str(value))
            values = ",".join(query_formatted_values)
            sql = "INSERT INTO "+table_name+" ("+fields+") VALUES ("+values+")"
            sql_list.append(sql)

        return sql if len(sql_list) == 1 else sql_list

    def select(self,projection : list or str = "*",table_name: str = None,predicates : list  = None,group_by : list = None,having :list=None,order_by:list=None):
        
        if not table_name:
            raise Exception("Table name not found")
        if isinstance(projection,list):
            projection = ",".join(projection)
        
        if predicates:
            predicates_string = str()
            for condition in predicates:
            
                if  isinstance(condition[2],str) or isinstance(condition[2],(datetime.date,datetime.datetime)):
                    condition[2] = "'"+str(condition[2])+"'" 
                elif isinstance(condition[2],str):
                    condition[2] = "'"+str(condition[2])+"'" if condition[2].isnumeric() else str(condition[2])  
                else:
                    condition[2] = str(condition[2]) 

                predicates_string = predicates_string+" ".join(condition) + " AND "

        return "SELECT "+projection+" FROM "+table_name+" WHERE "+ predicates_string +" 1=1 "
        
    
    def update(self,projection : list,table_name: str,predicates : list):
        
        if not table_name:
            raise Exception("Table name not found")
        if not projection:
            raise Exception("projection name not found")
        if not predicates:
            raise Exception("predicates name not found")

        if predicates:
            predicates_string = str()
            for condition in predicates:
            
                if  isinstance(condition[2],str) or isinstance(condition[2],(datetime.date,datetime.datetime)):
                    condition[2] = "'"+str(condition[2])+"'" 
                elif isinstance(condition[2],str):
                    condition[2] = "'"+str(condition[2])+"'" if condition[2].isnumeric() else str(condition[2])  
                else:
                    condition[2] = str(condition[2]) 

                predicates_string = predicates_string+" ".join(condition) + " AND "
            print(predicates_string)
        if projection:
            projection_string = str()
            predicates_list = list()
            for new_values in projection:
            
                if  isinstance(new_values[2],str) or isinstance(new_values[2],(datetime.date,datetime.datetime)):
                    new_values[2] = "'"+str(new_values[2])+"'" 
                elif isinstance(new_values[2],str):
                    new_values[2] = "'"+str(new_values[2])+"'" if new_values[2].isnumeric() else str(new_values[2])  
                else:
                    new_values[2] = str(new_values[2]) 
                predicates_list.append(" ".join(new_values))
            projection_string = ",".join(predicates_list)

        return "UPDATE "+table_name+" SET "+ projection_string + " WHERE "+ predicates_string +" 1=1;"
    
    def delete(self,table_name: str = None,predicates : list  = None):
        
        if not table_name:
            raise Exception("Table name not found")
        if predicates:
            predicates_string = str()
            for condition in predicates:
            
                if  isinstance(condition[2],str) or isinstance(condition[2],(datetime.date,datetime.datetime)):
                    condition[2] = "'"+str(condition[2])+"'" 
                elif isinstance(condition[2],str):
                    condition[2] = "'"+str(condition[2])+"'" if condition[2].isnumeric() else str(condition[2])  
                else:
                    condition[2] = str(condition[2]) 

                predicates_string = predicates_string+" ".join(condition) + " AND "

        return "DELETE FROM "+table_name+" WHERE "+ predicates_string +" 1=1 "
    
query = QueryGenerator().delete(table_name=table_name,predicates=[["name","=","Akshai"],["age","=","20"],["created",">",datetime.date.today()]])
print(query)





