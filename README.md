**Activate the virtual environment**

```

source blockchain-env/bin/activate
```

**Install all packages**
```

pip3 install -r requirements.txt
```

**Run the tests**

Make sure to activate the virtual environment

```
python -m pytest backend/tests
```

**Run the application and API**

Make sure to activate the virtual environment

```
python -m backend.app
```

**Run a peer instance**

Make sure to activate the virtual environment

```
set PEER=True 
python -m backend.app  #I had to run these in 2 separate lines to get it to work whereas Dave put them in same, connected with "&&"
```

**Run the frontend**

In the frontend directory:
```
npm run start
```

**Seed the backend with data**

Make sure to activate the virtual environment

```
set  SEED_DATA=True
python -m backend.app
```