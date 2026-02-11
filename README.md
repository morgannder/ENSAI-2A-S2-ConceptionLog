# ENSAI-2A-projet-Conception-Logicielle : Valorant data analyst


## :arrow_forward: Software and tools

- [Visual Studio Code](https://code.visualstudio.com/)
- [Python 3.13](https://www.python.org/)
- [Git](https://git-scm.com/)
- [SQLite]
- [Database] (https://www.dropbox.com/scl/fi/fxcg4bmsrs1ucisgwn9cs/rocket_league.db?rlkey=ab24v93i3ksifkztmv8mf8csn&st=srnedikq&dl=0)

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


### Usage

- [ ] Enter in console : uv sync
- [ ] Create .env file (.env.template is here to help you)
- [ ] Download DB at https://www.dropbox.com/scl/fi/fxcg4bmsrs1ucisgwn9cs/rocket_league.db?rlkey=ab24v93i3ksifkztmv8mf8csn&st=srnedikq&dl=0
- [ ] Name it "rocket_league.db" and put it in [database] directory
- [ ] run main.py to start API process


### API Key Generation

- [ ] Create an account on Ballchasing.com using a Steam account
- [ ] Go to [Upload] tab
- [ ] Upload Token -> Generate one and put it in your .env

NB : You have a limited number of requests : 2/second, 500/hour

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

Normally, for the purposes of your project, you won't need to modify these files, except for `.env` and `requirements.txt`.


## :arrow_forward: Install required packages

- [ ] In Git Bash, run the following commands to:
  - install all package from file `requirements.txt`

```bash
uv sync
```



## :arrow_forward: Unit tests

- [ ] In Git Bash: `pytest -v`
  - or `python -m pytest -v` if *pytest* has not been added to *PATH*


### Test coverage
