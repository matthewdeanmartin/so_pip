# so these tools don't conflict with each other
pipx install isort
pipx install pygount
pipx install mypy
pipx install vulture

# in so_pip
#pipx install black
#pipx install pyupgrade
pipx install pylint
pipx install radon
pipx install flake8
pipx inject flake8 dlint mccabe pyflakes pep8-naming flake8-bugbear
pipx install pipenv-to-requirements
pipx install yamllint
pipx install apistar
pipx install openapi-spec-validator
pipx install jiggle_version
pipx install pyroma
pipx install twine
pipx install bandit

# pipx install "check-manifest==0.40"
