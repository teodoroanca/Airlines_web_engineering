import React from 'react';
import calls_root from '../../api/calls_root';
import { Link } from 'react-router-dom';

class OperatingCarriers extends React.Component {
	
	constructor(props) {
		super(props);
		this.state = {
			carriers: [],
		}
	}

	getCarriers = async (code) => {
		const response = await calls_root.get(`/airports/${code}/carriers`, {

		});
		this.setState({
			carriers: response.data
		})

		// console.log(this.state.carriers);

	}

	renderCarriers() {
		return this.state.carriers.map( carrier => {
			const { code } = this.props.match.params;
			return (
				<div className="item" key={carrier.code}>
					<div style={{ fontWeight: 'bold' }}>
						{carrier.code}
					</div>
					  {carrier.name}
					  <br/>

					  <Link to={`/airports/${code}/operating-carriers/${carrier.code}/statistics`} className="ui button primary">
						Statistics
					 </Link>

					  <br/>
					  <br/>
				</div>


				



			);
		});
	}

	componentDidMount() {

		const { code } = this.props.match.params;

		this.getCarriers(code);
	}

	render() {
		return (
			<div>
				<h1>
					All the carriers operating at aiport:  {this.props.match.params.code}
				</h1>
				<div className="ui list">
					{this.renderCarriers()}
				</div>
			</div>
		);
	}

}

export default OperatingCarriers;
