import React from 'react';
import { Link } from 'react-router-dom';

class Home extends React.Component {

	renderList() {
		return(
			<div>
				<Link to={`/airports`} className="ui button primary">
					<div className="content">
						1. List of all airports
					</div>
				</Link>
				<br/>
				<br/>
				<Link to={`/carriers`} className="ui button primary">
					<div className="content">
						2. List of all carriers
					</div>
				</Link>
				<br/>
				<br/>
				<Link to={`/descriptive-statistics`} className="ui button primary">
					<div className="content">
						3. Descriptive statistics
					</div>
				</Link>
			</div>
		);
	}


	render() {
		return (
			<div>
				<h2>
					Home page
				</h2>
				<div className="ui celled list">
					{this.renderList()}
				</div>
			</div>
			
		);
	}

}

export default Home;