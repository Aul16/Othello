import os

# Have to be run from the root directory
os.system("python -m pytest --cov=gameOthello --cov-report html")