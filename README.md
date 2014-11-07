ewwrp
=====

Emory Women Writers Research Project in Django

How to start editing (Mac)
=====

If you don't have virtualenv: http://virtualenv.readthedocs.org/en/latest/virtualenv.html
'''
sudo easy_install pip
sudo pip install virtualenv
'''

Create and start a virtual environment:
'''
virtualenv venv
source venv/bin/activate
'''

This project uses LXML. Make sure you have XCode's command line utilities instialled. This can be done with
'''
xcode-select --install
'''

Finally, install dependencies.
'''
pip install -r pip-dependencies
'''
