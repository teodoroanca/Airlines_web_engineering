import React from 'react';
import calls_root from '../../api/calls_root';
import { Link } from 'react-router-dom';

class CarriersAll extends React.Component {
	
	constructor(props) {
		super(props);
		this.state = {
			carriers: [],
		}
	}

	getCarriers = async () => {
		const response = await calls_root.get('/carriers', {

		});
		this.setState({
			carriers: response.data
		})

	}

	renderCarriers() {
		return this.state.carriers.map( carrier => {
			return (
				<div className="item" key={carrier.code}>
					<div style={{ fontWeight: 'bold' }}>
						{carrier.code}
					</div>
					  {carrier.name}
					  <br/>
					  <Link to={`/carriers/${carrier.code}`} className="ui button primary">
						Number of minutes of delay for this carrier
					</Link>
				</div>
			);
		});
	}

	componentDidMount() {
		this.getCarriers();
	}

	render() {
		return (
			<div className="ui list">
				{this.renderCarriers()}
			</div>
		);
	}

}

export default CarriersAll;
