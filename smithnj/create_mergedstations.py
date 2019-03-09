import json
import dml
import prov.model
import uuid
import pandas as pd
import datetime

############################################
# create_communitydata.py
# Script for merging L-station GeoSpatial Data with Community Area Number GeoSpatial Data
############################################

class grab_ctastations(dml.Algorithm):
    contributor = 'smithnj'
    reads = []
    writes = ['smithnj.ctastats']

    @staticmethod
    def execute(trial=False):

        startTime = datetime.datetime.now()
        # ---[ Connect to Database ]---------------------------------
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('smithnj', 'smithnj')
        repo_name = 'smithnj.merged_stations'
        # ---[ Grab Data ]-------------------------------------------
        communityareas = geopandas.read_file(
            'https://data.cityofchicago.org/api/geospatial/cauq-8yn6?method=export&format=GeoJSON')
        stationloc = geopandas.read_file('http://datamechanics.io/data/smithnj/CTA_RailStations.geojson')
        # ---[ Create Data ]-----------------------------------------
        merged = geopandas.sjoin(communityareas, stationloc, how="inner", op='within')
        # ---[ Write Data to JSON ]----------------------------------
        data = merged.to_json()
        loaded = json.loads(data)
        # ---[ MongoDB Insertion ]-------------------------------------------
        repo.dropCollection('merged_stations')
        repo.createCollection('merged_stations')
        repo[repo_name].insert_one(loaded)
        repo[repo_name].metadata({'complete': True})
        # ---[ Finishing Up ]-------------------------------------------
        print(repo[repo_name].metadata())
        repo.logout()
        endTime = datetime.datetime.now()
        return {"start": startTime, "end": endTime}

    @staticmethod
    def provenance(doc=prov.model.ProvDocument(), startTime=None, endTime=None):
#TODO COMPLETE MERGEDSTATION PROV
        '''
            Create the provenance document describing everything happening
            in this script. Each run of the script will generate a new
            document describing that invocation event.
        '''
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        doc.add_namespace('bdp', 'https://data.cityofchicago.org/Transportation/CTA-Ridership-L-Station-Entries-Daily-Totals/5neh-572f')
        doc.add_namespace('dmc', 'http://datamechanics.io/data/smithnj')
        this_script = doc.agent('alg:smithnj#grab_stationstats', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        resource = doc.entity('dmc:5neh-572f.json', {'prov:label':'CTA - Ridership - L Station Entries - Daily Totals', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        grab_stationstats = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        doc.wasAssociatedWith(grab_stationstats, this_script)
        doc.usage(grab_stationstats, resource, startTime, None, {prov.model.PROV_TYPE.'ont:Retrieval'})
        stationstats = doc.entity('dat:smithnj#stationstats', {prov.model.PROV_LABEL:''})

        return doc