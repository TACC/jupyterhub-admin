from agavepy import Agave
from tapipy.tapis import Tapis
from django.conf import settings
import json


def get_config_metadata_name():
    return f"config.{settings.TENANT}.{settings.INSTANCE}.jhub"


def get_group_config_metadata_name(group):
    return f"{group}.group.{get_config_metadata_name()}"

def get_tapis_client():
    return Tapis(base_url=settings.TAPIS_API_URL, jwt=settings.TAPIS_SERVICE_TOKEN)

def get_agave_client():
    return Agave(api_server=settings.AGAVE_API, token=settings.AGAVE_SERVICE_TOKEN)

def get_tapis_config_metadata():
    t = get_tapis_client()
    filter = {"name": get_config_metadata_name()}
    metadata = t.meta.listDocuments(db='jupyterhub_v3_metadata', collection='jupyterhub_dev', filter=json.dumps(filter))
    return json.loads(metadata)[0]

def get_config_metadata():
    ag = get_agave_client()
    query = {'name':get_config_metadata_name()}
    metadata = ag.meta.listMetadata(q=json.dumps(query))
    return metadata[0]

def list_tapis_group_config_metadata():
    t = get_tapis_client()
    filter = {'name':{'$regex':f".*group.{get_config_metadata_name()}"}}
    metadata = t.meta.listDocuments(db='jupyterhub_v3_metadata', collection='jupyterhub_dev', filter=json.dumps(filter))
    return json.loads(metadata)

def list_group_config_metadata():
    ag = get_agave_client()
    query = { 'name': {'$regex': f".*group.{get_config_metadata_name()}"}}
    metadata = ag.meta.listMetadata(q=json.dumps(query))
    return metadata

def get_tapis_group_config_metadata(group):
    t = get_tapis_client()
    filter = {'name': get_group_config_metadata_name(group)}
    metadata = t.meta.listDocuments(db='jupyterhub_v3_metadata', collection='jupyterhub_dev', filter=json.dumps(filter))
    return json.loads(metadata)[0]

def get_group_config_metadata(group):
    ag = get_agave_client()
    query = {'name': get_group_config_metadata_name(group)}
    metadata = ag.meta.listMetadata(q=json.dumps(query))
    return metadata[0]

def write_tapis_group_config_metadata(group, value):
    t = get_tapis_client()
    meta = get_tapis_group_config_metadata(group)
    print("************** " * 30)
    meta['value'] = value
    print(meta)
    t.meta.modifyDocument(db='jupyterhub_v3_metadata', collection='jupyterhub_dev', request_body=meta, docId=meta['_id']['$oid'])

def write_group_config_metadata(group, value):
    ag = get_agave_client()
    meta = get_group_config_metadata(group)
    print("************** " * 30)
    meta['value'] = value
    print(meta)
    ag.meta.updateMetadata(body=meta, uuid=meta['uuid'])

def create_tapis_group_config_metadata(group):
    t = get_tapis_client()
    meta = {
        "name": get_group_config_metadata_name(group),
        "value": {
            "tenant": settings.TENANT,
            "instance": settings.INSTANCE,
            "user": [],
            "images": [],
            "config_type": "group",
            "volume_mounts": [],
            "group_name": group,
            "name": get_group_config_metadata_name(group)
        }
    }
    t.meta.createDocument(db='jupyterhub_v3_metadata', collection='jupyterhub_dev', basic='true', request_body=meta)

def create_group_config_metadata(group):
    ag = get_agave_client()
    meta = {
        "name": get_group_config_metadata_name(group),
        "value": {
            "tenant": settings.TENANT,
            "instance": settings.INSTANCE,
            "user": [],
            "images": [],
            "config_type": "group",
            "volume_mounts": [],
            "group_name": group,
            "name": get_group_config_metadata_name(group)
        }
    }
    ag.meta.addMetadata(body=meta)

def rename_tapis_group_config_metadata(original, group):
    t = get_tapis_client()
    meta = get_tapis_group_config_metadata(original)
    #del meta['_id']['$oid']
    new_meta_name = get_group_config_metadata_name(group)
    meta['name'] = new_meta_name
    meta['value']['group_name'] = group
    meta['value']['name'] = new_meta_name
    t.meta.modifyDocument(db='jupyterhub_v3_metadata', collection='jupyterhub_dev', request_body=meta, docId=meta['_id']['$oid'])
    #t.meta.createDocument(db='jupyterhub_v3_metadata', collection='jupyterhub_dev', basic='true', request_body=meta)
    #delete_tapis_group_config_metadata(original)

def rename_group_config_metadata(original, group):
    ag = get_agave_client()
    meta = get_group_config_metadata(original)
    del meta['uuid']
    new_meta_name = get_group_config_metadata_name(group)
    meta['name'] = new_meta_name
    meta['value']['group_name'] = group
    meta['value']['name'] = new_meta_name
    ag.meta.addMetadata(body=meta)
    delete_group_config_metadata(original)

def delete_tapis_group_config_metadata(group):
    t = get_tapis_client()
    meta = get_tapis_group_config_metadata(group)
    t.meta.deleteDocument(db='jupyterhub_v3_metadata', collection='jupyterhub_dev', docId=meta['_id']['$oid'])

def delete_group_config_metadata(group):
    ag = get_agave_client()
    meta = get_group_config_metadata(group)
    ag.meta.deleteMetadata(uuid=meta['uuid'])


def get_admin_tenant_metadata():
    ag = Agave(api_server=settings.AGAVE_API, token=settings.AGAVE_SERVICE_TOKEN)
    metadata = ag.meta.listMetadata()
    matching = []
    for entry in metadata:
        if 'admin_users' in entry['value'] and settings.TENANT in entry['value']['admin_users']:
            matching.append(entry)
    return matching

'''
def get_admin_group_metadata():
    ag = get_agave_client()
    query = {'name':'admins.groups.config'}
    metadata = ag.meta.listMetadata(q=json.dumps(query))
    print("METADATA: %s", metadata)
    #return metadata[0]
'''

def write_tapis_config_metadata(value):
    t = get_tapis_client()
    meta = get_tapis_config_metadata()
    meta['value'] = value
    t.meta.modifyDocument(db='jupyterhub_v3_metadata', collection='jupyterhub_dev', request_body=meta, docId=meta['_id']['$oid'])

def write_config_metadata(value):
    ag = get_agave_client()
    # TODO fix this
    meta = get_config_metadata()
    meta['value'] = value
    ag.meta.updateMetadata(body=meta, uuid=meta['uuid'])


def set_config(key, value):
    current = get_config_metadata()['value']
    current[key] = value
    write_config_metadata(current)
