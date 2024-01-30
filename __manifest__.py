# -*- coding: utf-8 -*-
{
    'name': "Sagas",
    'summary': "Gestion de sagas",
    'description': """
        Gestor de Sagas
        ==============
        """,  
    'application': True,
    'author': "Autor",
    'website': "website",
    'category': 'Tools',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        
        #Cargamos los ficheros con vistas tanto de biblioteca_comic como de biblioteca_comic_categoria
        'views/biblioteca_comic.xml',
        'views/biblioteca_comic_categoria.xml'
    ],
}
