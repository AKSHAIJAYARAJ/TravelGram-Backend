from database_manager.dgraph_manager import DgraphManager
from database_manager.dynamic_dgql import DgraphQueryGenerator
class UserCRUD:

    def get(self,user_uid: str =None):

        # Get uid of node to be fetched
        # Get query based on uid and form of data needed
        # Get data from Dgraph
        # return data

        if user_uid:
            # Fetch one
            query = DgraphQueryGenerator().generate_get_query(schema_owner="user",uid=user_uid)
        else:
            # Fetch all
            query = DgraphQueryGenerator().generate_get_query(schema_owner="user")
        data = DgraphManager().get_node(query=query)['query']
        return data
    
    def post(self,user_data : dict):

        # Get Data to be posted
        # Get query based on data and schema owner
        # Add data to Dgraph
        # return uid

        query = DgraphQueryGenerator().generate_upsert_query(schema_owner="user",input_payload=user_data)
        uid = DgraphManager().create_node(data = query)
        return uid
    def put(self,user_uid: str,user_data : dict):

        # Get Data to be posted and uid of node
        # Get query based on data,uid and schema owner
        # Update data to Dgraph
        # return uid

        query = DgraphQueryGenerator().generate_upsert_query(schema_owner="user",input_payload=user_data,uid=user_uid)
        uid = DgraphManager().create_node(data = query)
        
        return True
    def delete(self,user_uid: str =None):
        pass