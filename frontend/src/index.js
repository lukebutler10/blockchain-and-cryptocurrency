import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Switch, Route } from 'react-router-dom'; // the combination of these allows us to set up a frontend router that can navigate to various frontend routes i.e. multiple pages of a website
import history from './history'; 
import './index.css';
import App from './components/App';
import Blockchain from './components/Blockchain';
import ConductTransaction from './components/ConductTransaction';
import TransactionPool from './components/TransactionPool';

ReactDOM.render(
	<Router history={history}> // this is what we imported from our history.js file
		<Switch>  // //the Switch component allows us to group together multiple routes in the application
			<Route path='/' exact component={App} /> // 'exact' here means we need path to exactly match '/', not a string that includes '/'
			<Route path='/blockchain' component={Blockchain} />
			<Route path='/conduct-transaction' component={ConductTransaction} />
			<Route path='/transaction-pool ' component={TransactionPool} />

		</Switch> 
	</Router>,
	document.getElementById('root')
);

