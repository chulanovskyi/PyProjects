from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')
myData = []
for files in os.listdir('soundBox\\'):
    f1 = 'soundBox\\' + files
    if os.path.isfile(f1):
        f2 = 'soundBox', [f1]
        myData.append(f2)
for files in os.listdir('images\\'):
    f1 = 'images\\' + files
    if os.path.isfile(f1):
        f2 = 'images', [f1]
        myData.append(f2)
myData.append('config.cfg')
setup(
    data_files = myData,
    options = {'py2exe': {'bundle_files': 3, 'compressed': True}},
    windows = [{'script': "Ring.pyw"}],
    zipfile = None,
)
