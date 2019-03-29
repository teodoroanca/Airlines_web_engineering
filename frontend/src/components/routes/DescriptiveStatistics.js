import React from 'react';
import calls_root from '../../api/calls_root';
import { Link } from 'react-router-dom';

import DescriptiveStatisticElement from './DescriptiveStatisticElement';

class DescriptiveStatistics extends React.Component {

	constructor(props){
		super(props);
		this.state = {
			airports: null,
			airport1: "",
			airport2: "",
			descriptive_statistics: null,
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

	componentDidMount() {
		this.getAirports();
	}

	renderAirports() {
		if(this.state.airports){
			return this.state.airports.map( airport => {
				return (
					<option className="item" key={airport.code}>
							{airport.code}
					</option>
				);
			});
		}
	}


	getDescriptiveStatistics = async (airport1, airport2) => {

		let response;

		response = await calls_root.get(`/descriptive-statistics/${airport1}/second-airport/${airport2}/carriers`, {});
		
		this.setState({
			descriptive_statistics: response.data
		})

		console.log(this.state);

	}


	handleSubmit = (event) => {
	  	event.preventDefault();
	    console.log('Your airport1 is: ' + this.state.airport1);
	    console.log('Your airport2 is: ' + this.state.airport2);


	    this.getDescriptiveStatistics(this.state.airport1, this.state.airport2)


	  }

	renderDescriptiveStatistics() {
		if(this.state.descriptive_statistics){
			console.log(this.descriptive_statistics);
			return this.state.descriptive_statistics.map( element => {
				return(
					<div key={element.carrier}>

						<Link to={`/descriptive-statistics/${this.state.airport1}/${this.state.airport2}/${element.carrier}`} className="ui button primary">
							Carrier: {element.carrier}
						</Link>


						<DescriptiveStatisticElement carrier={element.carrier} mean={element.mean} median={element.median} standard_deviation={element.standard_deviation}/>
					</div>
				);



			});
		}
		else{
			return(
				<div>
					Pick 2 airports...
				</div>
			)
		}
	}

	renderBar() {
		return(
			<form onSubmit={this.handleSubmit}>
			        <label>
			          Pick first airport:
			          <select value={this.state.airport1} onChange={(e) => {this.setState({airport1: e.target.value})}}>
			            <option value="">Any airport</option>
			            {this.renderAirports()}
			          </select>
			        </label>

			        <br/>
			        <br/>
			        <br/>

			        <label>
			          Pick second airport:
			          <select value={this.state.airport2} onChange={(e) => {this.setState({airport2: e.target.value})}}>
			            <option value="">Any airport</option>
			            {this.renderAirports()}
			          </select>
			        </label>

			        <br/>
			        <br/>
			        <input type="submit" value="Filter" />

			</form>
		);
	}

	render() {
		return(
			<div className="ui bulleted list">
				{this.renderBar()}
				{this.renderDescriptiveStatistics()}
			</div>
		);
	}

}

export default DescriptiveStatistics;

