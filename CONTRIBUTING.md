Contributing
------------
You will need to get a [stackexchange key](https://stackapps.com/apps/oauth/register). Use your name, not the so_pip name so StackExchange doesn't think
I personally am registering multiple keys for the same product.

To run a build
```
git clone https://github.com/matthewdeanmartin/so_pip.git
pipenv install --dev --skip-lock
# todo list pipx installs, e.g. pylint, isort, etc.
pipenv shell
# verify code
python -m navio package
# update version number...
poetry build
# twine upload...
```

The rest is fork/edit/pull request.

### Here is how to run the app starting from a clone.
```
git clone https://github.com/matthewdeanmartin/so_pip.git
python -m venv venv
. venv/Scripts/activate
pip install -r .config/requirements.txt
# some tools can't co-exist in the same virtual environment
pipx install pylint
pipx install isort
python -m so_pip --version
```

### Here is how to do a docker build locally.
```
cd docker
./build.sh
./run.sh search zip --query="how do I zip" --tags="python" --verbose --output=/data
```
