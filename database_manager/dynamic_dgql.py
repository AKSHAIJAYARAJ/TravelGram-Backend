import json
import sys
sys.path.append("/opt/projects-A/trip_media/")
from datetime import datetime
with open("/opt/projects-A/trip_media/database_manager/dgraph_schema.json",'r') as schema:
    schema = json.load(schema)

class DgraphQueryGenerator:

    def generate_get_query(self,schema_owner : str =None,filter : str =None, normalize : bool = False,recurse : bool = False,depth : str = "10", uid : str =None,connected_node:str or list  =None,reverse_edge:bool =False):
        # Get schema based on schema owner
        # add filter condition if any
        # Construct query and return
        predicates = schema[schema_owner]["predicates"]
        connections = schema[schema_owner]["connections"]
        dgraph_type = schema[schema_owner]["dgraph.type"]
        if uid:
            part_1 = "{query(func :uid("+uid+"))"
        else :
             part_1 = "{query(func :has("+dgraph_type+"."+predicates[0]+"))"
        if filter:
             part_1 += "  @filter("+filter+") "
        if normalize:
            part_1 += " @normalize "
        if recurse:
            part_1 += " @recurse(depth: "+str(depth)+", loop: true)"
        predicate_str =" { "
        for fields in predicates:
            predicate_str = predicate_str+"\n"+ fields + " : " + dgraph_type+"."+fields
        if connections and connected_node:
            # convert to list if it not a list
            connected_node = [connected_node] if isinstance(connected_node,str) else connected_node
            for edge in connected_node: 
                if edge in connections:
                    connected_predicate_str = '{'   
                    connected_predicates = schema[edge]["predicates"]
                    connected_dgraph_type = schema[schema_owner]["dgraph.type"]
                    for fields in connected_predicates:
                        connected_predicate_str = connected_predicate_str+"\n"+ fields + " : " + connected_dgraph_type+"."+fields
                    connected_predicate_str += "}"
                    predicate_str += dgraph_type+"."+edge+" : "+connected_predicate_str
        predicate_str += "}}"
        query = part_1 + predicate_str
        print(query)
    def generate_upsert_query(self,schema_owner : str = None,input_payload:dict =None,uid : str = None):
        
        # Get schema based on schema owner
        # Get Input payload
        # Construct query based on schema and input payload and return
        predicates = schema[schema_owner]["predicates"]
        connections = schema[schema_owner]["connections"]
        dgraph_type = schema[schema_owner]["dgraph.type"]
        query = dict()
        for key,value in input_payload.items():
            if key in predicates:
                query.update({dgraph_type+"."+key : value})
            if connections:
                if key in connections:
                    query.update({dgraph_type+"."+key : {"uid":value}})
        if uid:
            query.update({"uid" :uid})
        query.update({"dgraph.type" :dgraph_type })
        
        return query
    # def generate_delete_query(self,schema_owner : str):
    #     # Get schema and update schema with key "uid"
    #     pass

################################################################ SAMPLES DATA ################################################################
"POST"
# DgraphQueryGenerator().generate_upsert_query(schema_owner="user",input_payload={
#             "first_name" : "AKSHAI",
#             "last_name" : "JAYARAJ",
#             "date_of_birth" : datetime.now(),
#             "gender" :"male",
#             "email" :"9037975068",
#             "phone" : "akshaijayaraj798@gmail.com",
#             "location" : "0x1"
#         })
"GET"
# DgraphQueryGenerator().generate_get_query(schema_owner="user",normalize=True,
#                                           uid="0x12",recurse=True,filter="(User.first_name,AKSHAI)",
#                                           depth= 15,)