# Creating a Blockchain and Cryptocurrency 

### Description
In this project my aim was to have a build my development experience in blockchain technology, cryptocurrencies, and frontend development. Here's some key components:
* Building the Blockchain backend in Python
* Testing the application with Pytest
* Creating the blockchain network using Flask and Pub/Sub
* Integrate the Cryptocurrency, building Wallets, Keys, and Transactions
* Building the fronted portion with React.js

For this project I followed David Katz's course on Udemy: https://www.udemy.com/course/python-js-react-blockchain/?referralCode=9051A01550E782315B77 

### How to install and run
**Create and activate the virtual environment**

```
python -m venv blockchain-env

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
python -m backend.app
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

### How to Use the Project
1. **Running the Backend**: Start the backend server by running the **`backend.app`** module. This initializes the blockchain and cryptocurrency system, enabling you to interact with the blockchain via API endpoints.
2. **Running the Frontend**: Navigate to the frontend directory and run **`npm run start`** to launch the React frontend. This opens a web interface where you can interact with the blockchain and cryptocurrency system.
3. **Interacting with the Blockchain**:
      * **Create Transactions**: Use the frontend to create new cryptocurrency transactions. These transactions will be added to the blockchain and validated by the network.
      * **Mine Blocks**: Trigger the mining process to add new blocks to the blockchain. This involves solving a computational puzzle to ensure the integrity and security of the blockchain.
      * **View Blockchain Data**: Access and view the current state of the blockchain, including all blocks and transactions, through the frontend interface.
4. **Running Peer Instances**: To simulate a decentralized network, run multiple peer instances of the backend. Each peer maintains its own copy of the blockchain and communicates with other peers to ensure consensus and data consistency.
5. **Seeding Data**: Use the **`SEED_DATA=True`** environment variable to initialize the backend with sample data. This is useful for testing and demonstration purposes, as it provides a pre-populated blockchain and set of transactions.
