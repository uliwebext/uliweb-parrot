def call(app, var, env, plugins=None, js=True, responsive=False, version=None):
    from uliweb import settings
    
    a = []
    version = version or settings.UI_CONFIG.bootstrap_version
    a.append('<!--[if lt IE 9]>')
    a.append('bootstrap/asset/html5.js')
    a.append('<![endif]-->')
    a.append('bootstrap/%s/css/bootstrap.min.css' % version)
    if responsive or settings.UI_CONFIG.bootstrap_responsive:
        a.append('bootstrap/%s/css/bootstrap-responsive.min.css' % version)
            
    if js:
        jquery = True
        a.append('bootstrap/%s/js/bootstrap.min.js' % version)
      
    d = {'toplinks':a, 'depends':[]}
    if jquery:
        d['depends'] = ['jquery', 'json2']
    return d
