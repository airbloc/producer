import json
from airbloc.proto import Identifier

def cleanse(data: dict) -> dict:
    assert isinstance(data.get('installedApps'), list)
    
    installed_apps = []
    for app in data['installedApps']:
        assert isinstance(app, object)
        assert isinstance(app.get('package'), str)
        assert isinstance(app.get('installedAt'), int)

        installed_apps.append({
            'package': app['package'],
            'installedAt': app['installedAt']
        }) 
       
    return {'installedApps': installed_apps}

blockchain_table = {
    'some-data': {}
}

def broadcast_to_pre(kfrags, topic=None):
    print('Re-Encryption key issued with Capsule {}'.format(topic))
    pass

def identity_match_request(identity: Identifier) -> str:
    found_id = 'PSEUDO_{}_{}'.format(identity.type, identity.identifier)
    return found_id
