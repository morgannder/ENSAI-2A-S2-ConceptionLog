# ENSAI-2A-projet-Conception-Logicielle : Rocket League data analyst

[![CI/CD Pipeline](https://github.com/morgannder/ENSAI-2A-S2-ConceptionLog/actions/workflows/deploy.yml/badge.svg?branch=develop)](https://github.com/morgannder/ENSAI-2A-S2-ConceptionLog/actions/workflows/deploy.yml)

## :arrow_forward: Software and tools

- [Visual Studio Code](https://code.visualstudio.com/)
- [Python 3.13](https://www.python.org/)
- [Git](https://git-scm.com/)
- [SQLite](https://www.sqlite.org/)
- [SSPCloud](https://datalab.sspcloud.fr/) : Databse hoster


### Option 1

- [ ] Go to http://rocketcl.api.kub.sspcloud.fr/


### Option 2

## :arrow_forward: Clone the repository

- [ ] Open VSCode
- [ ] Open **Git Bash**
- [ ] Clone the repo
  - `git clone https://github.com/morgannder/ENSAI-2A-S2-ConceptionLog`


### Open Folder

- [ ] Open **Visual Studio Code**
- [ ] File > Open Folder
- [ ] Select folder *ENSAI-2A-S2-ConceptionLog*
  - *ENSAI-2A-S2-ConceptionLog* should be the root of your Explorer
  - :warning: if not the application will not launch. Retry open folder


### Commands to execute

- [ ] in Git Bash : uv sync
- [ ] Create .env file (.env.template is here to help you) and fill it
- [ ] Download DB at https://www.dropbox.com/scl/fi/y0mtlg6s5iotbmn8599jg/rocket_league_updated.db?rlkey=mkw8ipfubu55kp84x7ot87ioz&st=s9vkfrc2&dl=0
- [ ] Name it "rocket_league.db" and put it in [database] directory
- [ ] run main.py to start API process

NB : Before the start of the project, we already had around 70 000 matches in json files. The folder scripts explains how we created the DB with those files. It is not used anymore, just explains how we started to fill our DB.

### API Key Generation

To run locally you'll need a Ballchasing API Key, here are the instructions to create your own key :

- [ ] Create an account on Ballchasing.com using a Steam account
- [ ] Go to [Upload] tab
- [ ] Upload Token -> Generate one and put it in your .env

NB2 : You have a limited number of requests : 2/second, 500/hour
NB3 : On http://rocketcl.api.kub.sspcloud.fr/, you can go up to 1000 requests/hour and 2/second

## Repository Files Overview


| Item                       | Description                                                              |
| -------------------------- | ------------------------------------------------------------------------ |
| `README.md`                | Provides useful information to present, install, and use the application |
| `LICENSE`                  | Specifies the usage rights and licensing terms for the repository        |
| `main.py`                  | execute to launch the API Swagger                                        |


### Configuration files

| Item                       | Description                                                              |
| -------------------------- | ------------------------------------------------------------------------ |
| `.env.template`            | Provides a template to create your own .env                              |



### Folders




### Settings files

This repository contains a large number of configuration files for setting the parameters of the various tools used.

Normally, for the purposes of your project, you won't need to modify these files, except for `.env`.



## :arrow_forward: Unit tests

- [ ] In Git Bash: `uv run pytest --cov=src tests/`
  - (run every tests and give a total coverage)
