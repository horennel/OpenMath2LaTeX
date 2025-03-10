"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'iconfile': './icons/logo.icns',
    'packages': [
        'anyio',
        'pynput',
        'fastapi',
        'openai',
        'PIL',
        'pyperclip',
        'rumps',
        'setuptools',
        'starlette',
        'uvicorn',
    ],
    'includes': ['backend', 'tools'],
    'plist': {
        'LSUIElement': True,  # no icon in the dock
        'CFBundleName': 'OpenMath2LaTex',  # Application Name
        'CFBundleDisplayName': 'OpenMath2LaTex',  # Application Display Name
        'CFBundleVersion': '0.01',
        'CFBundleIdentifier': 'OpenMath2LaTex',
    },
    'resources': [
        'icons',
        'backend',
        'tools',
        'LICENSE',
    ]
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=[
        'py2app',
        'backend',
        'tools',
    ],
)
