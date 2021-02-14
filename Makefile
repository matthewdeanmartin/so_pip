#
# Workflow
# 	install / install_setup_py / install_poetry
#   check (reformats, tests, etc.)
#	clean (remove old compiled files and packages)
#	package / package_setup_py
#	deploy / deploy_pipenv
#

# Get changed files
SRC := so_pip
SRC_FILES := $(wildcard so_pip/**/*.py)
FILES := $(wildcard **/*.py)
CONFIG_FOLDER := .config

# if you wrap everything in pipenv run, it runs slower.
ifeq ($(origin VIRTUAL_ENV),undefined)
    VENV := pipenv run
else
    VENV :=
endif

Pipfile.lock: Pipfile
	@echo "Installing dependencies"
	@pipenv install --dev

.PHONY: install
install: Pipfile.lock

clean-pyc:
	#@echo "Removing compiled files"
	#@find . -name '*.pyc' -exec rm -f {} +
	#@find . -name '*.pyo' -exec rm -f {} +
	#@find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	#@echo "Removing coverage data"
	#@rm -f .coverage
	#@rm -f .coverage.*

clean: # clean-pyc clean-test

# tests can't be expected to pass if dependencies aren't installed.
# tests are often slow and linting is fast, so run tests on linted code.
unittest: clean-pyc .build_history/flake8 .build_history/bandit Pipfile.lock
	@echo "Running unittest tests"
	$(VENV) python -m unittest discover

pytest: clean .build_history/flake8 .build_history/bandit Pipfile.lock
	@echo "Running pytest tests"
	$(VENV) py.test test --cov=$(SRC) --cov-report html:coverage --cov-fail-under 90

.build_history:
	@mkdir -p .build_history

.build_history/isort: .build_history $(SRC_FILES)
	@echo "Formatting imports"
	$(VENV) isort $(SRC)
	@touch .build_history/isort

.PHONY: isort
isort: .build_history/isort

.build_history/black: .build_history .build_history/isort $(SRC_FILES)
	@echo "Formatting code"
	$(VENV) black $(SRC)
	@touch .build_history/black

.PHONY: black
black: .build_history/black

.build_history/pre-commit: .build_history .build_history/isort .build_history/black
	@echo "Pre-commit checks"
	$(VENV) pre-commit run --all-files
	@touch .build_history/pre-commit

.PHONY: pre-commit
pre-commit: .build_history/pre-commit

.build_history/bandit: .build_history $(SRC_FILES)
	@echo "Security checks"
	$(VENV)  bandit $(SRC)
	@touch .build_history/bandit

.PHONY: bandit
bandit: .build_history/bandit

.build_history/flake8: .build_history .build_history/isort .build_history/black $(SRC_FILES)
	@echo "Linting with flake8"
	$(VENV) flake8 --config $(CONFIG_FOLDER)/.flake8 $(SRC)
	@touch .build_history/flake8

.PHONY: flake8
flake8: .build_history/flake8

# for when using -j (jobs, run in parallel)
.NOTPARALLEL: .build_history/isort .build_history/black

.PHONY: deploy
package_setup_py: clean
	@echo package for later deployment with pip
	@echo Wheel packaging has more failure points, particularly with omitting files.
	python setup.py build sdist

package: clean $(SRC_FILES)
	@echo package with poetry for later deployment with pip
	@echo You do not need to use poetry for dependency installation, but pyproject.toml will need to be up to date.
	poetry build

.PHONY: deploy
deploy_pipenv: clean
	@echo Deploying from pip lock file.
	@echo Assumes you've copied your source to destination and want to install the exact dependencies
	@echo If you are using setup.py or poetry or flit for packaging, you don't need pipenv sync.
	pipenv sync

check: pytest flake8 bandit pre-commit

define BUMP_VERSION_PY
from setuptools_scm import get_version
from setuptools_scm.version import guess_next_version

def version_scheme(version):
    verstr = str(version.tag)
    ver = verstr.split(".")
    return "{}.{}.{}".format(ver[0],ver[1],int(ver[2])+1)

v = get_version(
    version_scheme=version_scheme,
    local_scheme=lambda *args, **kwargs:"",
)
print(guess_next_version(v))
endef
export BUMP_VERSION_PY

NEXT_VERSION_BASH := $(VENV) python -c "$$BUMP_VERSION_PY"

bump_version:
	# current version, assuming at least one tag of say, 0.1.0
	echo $(NEXT_VERSION_BASH)
	# echo
	export NEXT_VERSION=
	@echo
	git tag "$$($(NEXT_VERSION_BASH))"
	git commit -m bump version to $$NEXT_VERSION



.DEFAULT_GOAL := check
