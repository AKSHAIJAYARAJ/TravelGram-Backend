# MODULE DETAILS
# __________________________________________________________________________________________________________________________
# MODULE NAME   : RedisManager
# VERSION       : 1.0
# SYNOPSYS      : This module is developed to perform redis operations.
# AUTHOR        : AKSHAI JAYARAJ
# CREATED ON    : 2023-MAY-27
# METHODS       : 
# 
# ENHANCEMENT HISTORY
# __________________________________________________________________________________________________________________________
# AUTHOR        : <AUTHOR>
# CREATED ON    : <CREATED ON>
# METHODS       : <METHODS>
# __________________________________________________________________________________________________________________________
import sys
sys.path.append("/opt/projects-A/trip_media/")
import pydgraph
import json 
with open("/opt/projects-A/trip_media/config_and_credentials/env_conf.json",'r') as conf:
    conf = json.load(conf)



class DgraphManager:

    """ This module deals with dgraph crud operations. """

    def __init__(self):

        """ Get Dgraph client. """

        self.client_stub = pydgraph.DgraphClientStub('localhost:9080')
        self.client = pydgraph.DgraphClient(self.client_stub)

    def create_node(self, data):
        """
        This method is used for creating nodes.
        Algorithm:

        1) Get data to be stored
        2) Create a node based on input data
        3) Return uid if data successfully else return false

        """
        txn = self.client.txn()
        try:
            mutation = pydgraph.Mutation()
            txn.mutate(set_obj=data,mutation=mutation)
            response = txn.mutate(mutation)
            uid = response.uids
            txn.commit()

            uid = list(uid.values())[0]
            # print(f"Created node with UID: {uid}")
            return uid
        finally:
            txn.discard()
            return False

    def update_node(self, data : dict, uid :str):
        """
        This method is used for updating nodes.
        Algorithm:

        1) Get data to be stored and uid of the node to be updated.
        2) Set uid in data.
        2) Mutate the input data to update the node.
        3) Return uid if data successfully else return false

        """
        txn = self.client.txn()
        try:
            data.update({"uid":uid})
            mutation = pydgraph.Mutation()
            txn.mutate(set_obj=data,mutation=mutation)
            response = txn.mutate(mutation)
            txn.commit()
        finally:
            txn.discard()
            return False

    def delete_node(self, uid):
        """
        This method is used for deleting nodes.
        Algorithm:

        1) Get data to be stored and uid of the node to be updated.
        2) Set uid in data.
        2) Mutate the input data to update the node.
        3) Return uid if data successfully else return false

        """

        txn = self.client.txn()
        try:
            node_uid = uid
            query= '''
            {
            deleteNode(input: {{ uid: '{node_uid}' }}) {
                numUids
            }
            }
            '''
                        
            print(query)
            txn.query(query)
            # mutation = pydgraph.Mutation()
            # txn.mutate(del_obj=query)
            txn.commit()
        except Exception as e:
            print(e)

        finally :
            txn.discard()
            return False

    def get_node(self, query:str):
       
        response = self.client.txn(read_only=True).query(query)
        data = response.json

        return data.decode("utf-8")
    
    def __del__(self):
        self.client_stub.close()

# id = DgraphManager().update_node(data = {
#     'uid':'0x1',
#     'dgraph.type': 'Test',
#     'Test.name': 'AJAY',
#     'Test.age': 50,
#     # "friend" :{
#     #     "uid":"0x2712"
#     # }
#     })

# data = DgraphManager().get_node(query="""{
# get(func :uid(0x1)){
#     id : uid
#     name : Test.name
#     age: Test.age
#     friends: friend{
#     uid
#     friend_name : Test.name
#     friend_age: Test.age

#     }
    
# }
# }""")
# print(data)
# DgraphManager().delete_node(uid="0x2")