import React from 'react';
import calls_root from '../../api/calls_root';
import { Link } from 'react-router-dom';

class AirportsAll extends React.Component {
	
	constructor(props) {
		super(props);
		this.state = {
			airports: [],
		}
	}

	getAirports = async () => {
		const response = await calls_root.get('/airports', {

		});
		this.setState({
			airports: response.data
		})

		console.log(this.state.airports);

	}

	renderAirports() {
		return this.state.airports.map( airport => {
			return (
				<div className="item" key={airport.code}>
					<div style={{ fontWeight: 'bold' }}>
						{airport.code}
					</div>
					  {airport.name}
					  <br/>
					 <Link to={`/airports/${airport.code}/operating-carriers`} className="ui button primary">
						All carriers operating at this airport
					</Link>
					  <br/>
					  <br/>
				</div>
			);
		});
	}

	componentDidMount() {
		this.getAirports();
	}

	render() {
		return (
			<div className="ui list">
				{this.renderAirports()}
			</div>
		);
	}

}

export default AirportsAll;
