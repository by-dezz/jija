from setuptools import setup

setup(
    name='jija',
    version='0.0.7',
    description='',
    packages=[
        'jija',
        'jija.database',
        'jija.forms',
        'jija.commands',
        'jija.utils',
        'jija.middlewares',
        'jija.config'
    ],
    author='Kain',
    author_email='kainedezz.2000@gmail.com',
    zip_safe=False,

    install_requires=[
        'aiohttp==3.8.1',
        'aiofile==3.8.1',
        'jija_orm==0.0.1',
        'cryptography',
        'aiohttp_session[secure]',
    ]
)
