import json

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
       
    return { 'installedApps': installed_apps }

