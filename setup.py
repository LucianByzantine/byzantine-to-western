from setuptools import setup

APP = ['byzantine_to_western.py']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'packages': ['music21', 'PIL'],
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
