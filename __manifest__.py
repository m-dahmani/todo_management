# -*- coding: utf-8 -*-

{
    'name': 'To Do App',
    'author': 'Mohamed DAHMANI',
    'version': '17.0.0.1.0',
    'category': '',
    'website': '',
    
    'depends': [
        'base','mail','contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/todo_task_view.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'todo_management/static/src/scss/*.scss',
        ],
    },

    'application': True,
}






















