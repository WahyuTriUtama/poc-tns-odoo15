{
    'name': 'Backend Theme', 
    'summary': 'Backend Theme',
    'version': '15.0.1.0.1', 
    'category': 'Themes/Backend', 
    'license': 'LGPL-3', 
    'author': '-',
    'website': '',
    'depends': [
        'base_setup',
        'web_editor',
        'mail',
    ],
    'excludes': [
        'web_enterprise',
    ],
    'data': [
       'templates/webclient.xml',
       'views/res_config_settings_view.xml',
       'views/res_users.xml',
    ],
    'assets': {
        'web.assets_qweb': [
            'poc_web_theme/static/src/**/*.xml',
        ],
        'web._assets_primary_variables': [
            'poc_web_theme/static/src/colors.scss',
        ],
        'web._assets_backend_helpers': [
            'poc_web_theme/static/src/variables.scss',
            'poc_web_theme/static/src/mixins.scss',
        ],
        'web.assets_backend': [
            'poc_web_theme/static/src/webclient/**/*.scss',
            'poc_web_theme/static/src/webclient/**/*.js',
            'poc_web_theme/static/src/search/**/*.scss',
            'poc_web_theme/static/src/search/**/*.js',
            'poc_web_theme/static/src/legacy/**/*.scss',
            'poc_web_theme/static/src/legacy/**/*.js',
        ],
    },
    'images': [
        'static/description/banner.png',
        'static/description/theme_screenshot.png'
    ],
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'uninstall_hook': '_uninstall_reset_changes',
}
