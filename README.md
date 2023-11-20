# Referite-Backend
This is repository of backend for referite project.

## Install & Run

### How to install

make sure that you have [python](https://www.python.org/downloads/) in your computer
first, clone [**this repository**](https://github.com/Referite/Referite-Backend) by type this command in your terminal at your choosen path

```js
git clone https://github.com/Referite/Referite-Backend.git Referite-Backend
```

go to project directory

```js
cd Referite-Backend
```

next, you have to create file name `.env` to configuration

`.env` file template looks like [sample.env](sample.env) you can modify value and copy it into `.env`  
**Note that you may get your .env by contacted siravich.te@ku.th or preawpan.t@ku.th via email.**

next, you have to create environment by typing this command

```js
python -m venv env
```

then, activate the environment using

```js
env\Scripts\activate.bat # Windows
. env/bin/activate # macOS and Linux
```

the terminal will using environment now then typing this command to install requirements

```js
pip install -r requirements.txt
```

### How to run

make sure you do all the install part and environment is activate.

#### now, to run server typing this command
```js
uvicorn main:app
```
go to `http://127.0.0.1:8000/` for application.  

### How to create database
1. Create ```dump``` folder in mongodb folder.
2. Copy ```referee``` folder from ```dump_data``` in the repository to new ```dump``` folder that you create in mongodb folder.
3. Run this command in terminal or docker terminal:
```
mongorestore  dump/
```

### Demo values for collections


