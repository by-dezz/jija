from setuptools import setup

setup(
    name='jija',
    version='0.0.8-3',
    description='',
    packages=[
        'jija',
        'jija.database',
        'jija.forms',
        'jija.commands',
        'jija.utils',
        'jija.middlewares',
        'jija.config',
        'jija.drivers',
        'jija.contrib.auth'
    ],
    author='Kain',
    author_email='kainedezz.2000@gmail.com',
    zip_safe=False,

    install_requires=[
        'aiohttp==3.8.1',
        'aiofile==3.8.1',
        'jija_orm==0.0.2',
        'cryptography',
        'aiohttp_session[secure]',
    ]
)
