import React from 'react';
import calls_root from '../../api/calls_root';
import { Link } from 'react-router-dom';

class CarrierAllStatistics extends React.Component {
	
	constructor(props) {
		super(props);
		this.state = {
			statistics: null,
			airport_code: '',
			carrier_code: ''
		};

	}

	getStatistics = async () => {
		
		console.log(this.props.match.params.airport_code);
		this.setState({
			airport_code:this.props.match.params.airport_code,
			carrier_code:this.props.match.params.carrier_code
		});


		const response = await calls_root.get(`/airports/${this.props.match.params.airport_code}/carriers/${this.props.match.params.carrier_code}/statistics`, {});
		this.setState({
			statistics: response.data
		})
		console.log(this.state);

	}

	renderStatistics() {

		if (this.state.statistics){
			return this.state.statistics.map( statistic => {
				return (
					<div  className="item" key={statistic.time}>
					
						<div >
							<div style={{ fontWeight: 'bold' }}>
								<h3>Time: {statistic.time}</h3>
							</div>

							<div className="list">
							      <div className="item">
							      	<h5>Flights</h5>
							      	<div className="list">
							      		<div className="item">Cancelled:{statistic.flights.cancelled}</div>
							      		<div className="item">On time:{statistic.flights.on_time}</div>
							      		<div className="item">Total:{statistic.flights.total}</div>
							      		<div className="item">Delayed:{statistic.flights.delayed}</div>
							      		<div className="item">Diverted:{statistic.flights.diverted}</div>
							      	</div>
							      </div>

							      <div className="item">
							      	<h5>Number of delays</h5>
							      	<div className="list">
							      		<div className="item">Late aircraft:{statistic.number_of_delays.late_aircraft}</div>
							      		<div className="item">Weather:{statistic.number_of_delays.weather}</div>
							      		<div className="item">Security:{statistic.number_of_delays.security}</div>
							      		<div className="item">National aviation system:{statistic.number_of_delays.national_aviation_system}</div>
							      		<div className="item">Carrier:{statistic.number_of_delays.carrier}</div>
							      	</div>
							      </div>

							      <div className="item">
							      	<h5>Minutes delayed</h5>
							      	<div className="list">
							      		<div className="item">Late aircraft:{statistic.minutes_delayed.late_aircraft}</div>
							      		<div className="item">Weather:{statistic.minutes_delayed.weather}</div>
							      		<div className="item">Carrier:{statistic.number_of_delays.carrier}</div>
							      		<div className="item">Security:{statistic.minutes_delayed.security}</div>
							      		<div className="item">Total:{statistic.minutes_delayed.total}</div>
							      		<div className="item">National aviation system:{statistic.minutes_delayed.national_aviation_system}</div>
							      		
							      	</div>
							      </div>
							      

						    </div>

							 <Link to={`/airports/${this.state.airport_code}/operating-carriers/${this.state.carrier_code}/statistics/${statistic.time}`} className="ui button primary">
								Detail page
							</Link>

							  <br/>
							  <br/>
						</div>
					</div>
				);
			});
		}
		else {
			return(
				<div>
					Loading...
				</div>
			);
		}
	}

	componentDidMount() {
		this.getStatistics();
	}

	render() {

		return (
			<div>
				<h1>
					Statistics for carrier {this.state.carrier_code} at airport {this.state.airport_code}
				</h1>
				<div className="ui bulleted list">
					{this.renderStatistics()}
				</div>
			</div>
		);
	}

}

export default CarrierAllStatistics;
