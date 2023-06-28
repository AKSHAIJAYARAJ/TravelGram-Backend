import sys
sys.path.append("/opt/projects-A/trip_media/")
from database_manager.dynamic_dgql import DgraphQueryGenerator
from database_manager.dgraph_manager import DgraphManager 

import json

with open("/opt/projects-A/trip_media/database_manager/dgraph_schema.json",'r') as schema:
    schema = json.load(schema)

class Location:
    
    def get(self,location_id:str=None):
        try:
            if location_id:
                graph_ql = DgraphQueryGenerator().generate_get_query(schema_owner="location",uid = location_id,normalize=True)
                location_details = DgraphManager().get_node(query=graph_ql)
            return {"status":"ok","result":location_details,'message':'location fetched'}
        except:
            return {"status":"error","result":'','message':'error'}
    def post(self,location_data:dict):
        try:
            graph_ql= DgraphQueryGenerator().generate_upsert_query(schema_owner='location',input_payload=location_data)
            uid = DgraphManager().create_node(data = graph_ql)
            return {"status":"ok","result":uid,'message':'location added'}
        except:
            return {"status":"error","result":'','message':'error'}
    def put(self,location_data: dict,location_id : str):
        try:
            graph_ql= DgraphQueryGenerator().generate_upsert_query(schema_owner='location',input_payload=location_data)
            uid = DgraphManager().update_node(data=graph_ql,uid=location_id)
            return {"status":"ok","result":uid,'message':'location updated'}
        except:
            return {"status":"error","result":'','message':'error'}
    def delete(self,location_id):
        try:
            DgraphManager().delete_node(uid=location_id,schema="\n".join(schema['location']['predicates']))
            return {"status":"ok","result":'','message':'location added'}
        except:
            return {"status":"error","result":'','message':'error'}
    def add_rating(self):
        pass
    def nearby(self):
        pass