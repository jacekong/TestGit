{
    'name': 'Bs add tasks, reference',
    'version': '14.6.4',
    'summary': '''
        refer task to project
    ''',
    'category': 'CRM',
    'author': 'Basic-Solution Co., Ltd.',
    'website': 'https://www.basic-solution.com/',
    'description': "",
    'depends': [
        'web',
        'base',
        'project',
        'bs_task_add',
        'bs_project_implement',
        'bs_project_menu'
    ],
    'data':[
        'views/project_view.xml',
        'views/product_category_view.xml',
        'security/ir.model.access.csv',
        'views/template.xml',
        'views/project_task_type_view.xml',
        'views/project_task_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}