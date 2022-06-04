from setuptools import setup


setup(
    name='jija',
    version='0.0.6',
    description='',
    packages=[
        'jija',
        'jija.database',
        'jija.forms',
        'jija.commands',
        'jija.utils',
        'jija.middlewares',
        'jija.config',

        'jija.cli',
        'jija.cli.commands'
    ],
    author='Kain',
    author_email='kainedezz.2000@gmail.com',
    zip_safe=False,

    install_requires=[
        'aiohttp==3.8.1',
        'aerich==0.6.3',
        'tortoise-orm==0.19.1',
        'asyncpg==0.25.0',
        'cryptography==37.0.2',
        'watchdog==2.1.8',
        'aiohttp_session[secure]==2.11.0',
    ],

    entry_points={
        'console_scripts': [
            'jija=jija.cli.main:main',
        ]
    }
)
