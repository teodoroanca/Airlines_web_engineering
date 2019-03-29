import React from 'react';
import calls_root from '../../api/calls_root';

class CarrierStatisticDetail extends React.Component {
	
	constructor(props) {
		super(props);
		this.state = {
			statistics: null,
			airport_code: '',
			carrier_code: '',
			year: 0,
			month: 0,
			specific_flights: false
		};

	}

	getStatistics = async () => {
		
		console.log(this.props.match.params.airport_code);
		this.setState({
			airport_code:this.props.match.params.airport_code,
			carrier_code:this.props.match.params.carrier_code,
			year:this.props.match.params.year,
			month:this.props.match.params.month
		});


		const response = await calls_root.get(`/airports/${this.props.match.params.airport_code}/carriers/
			${this.props.match.params.carrier_code}/statistics?year=${this.props.match.params.year}&month=${this.props.match.params.month}`, {});
		console.log(response.data);
		this.setState({
			statistics: response.data[0]
		})
		console.log(this.state);

	}

	renderStatistics() {
		const statistics = this.state.statistics;

		if (statistics){
			return (
				
					<div>

						<div className="list">
						      <div className="item">
						      	<h5>Flights</h5>
						      	
						      	<form onSubmit={() => {}}>
							      	<div className="ui slider checkbox">
									  <input type="checkbox" name="specific_flights" checked={this.state.specific_flights} onChange={(e) => this.setState({specific_flights: !this.state.specific_flights})}/>
									  <label>Specific</label>
									</div>  
								</form>
									
									{console.log(this.state.specific_flights)}
							      	<div className="list">
							      		<div className="item">Cancelled:{statistics.flights.cancelled}</div>
							      		<div className="item">On time:{statistics.flights.on_time}</div>
							      		{!this.state.specific_flights && <div className="item">Total:{statistics.flights.total}</div>}
							      		<div className="item">Delayed:{statistics.flights.delayed}</div>
							      		{!this.state.specific_flights && <div className="item">Diverted:{statistics.flights.diverted}</div>}
							      	</div>
							    
						      </div>

						      <div className="item">
						      	<h5>Number of delays</h5>
						      	<div className="list">
						      		<div className="item">Late aircraft:{statistics.number_of_delays.late_aircraft}</div>
						      		<div className="item">Weather:{statistics.number_of_delays.weather}</div>
						      		<div className="item">Security:{statistics.number_of_delays.security}</div>
						      		<div className="item">National aviation system:{statistics.number_of_delays.national_aviation_system}</div>
						      		<div className="item">Carrier:{statistics.number_of_delays.carrier}</div>
						      	</div>
						      </div>

						      <div className="item">
						      	<h5>Minutes delayed</h5>
						      	<div className="list">
						      		<div className="item">Late aircraft:{statistics.minutes_delayed.late_aircraft}</div>
						      		<div className="item">Weather:{statistics.minutes_delayed.weather}</div>
						      		<div className="item">Carrier:{statistics.number_of_delays.carrier}</div>
						      		<div className="item">Security:{statistics.minutes_delayed.security}</div>
						      		<div className="item">Total:{statistics.minutes_delayed.total}</div>
						      		<div className="item">National aviation system:{statistics.minutes_delayed.national_aviation_system}</div>
						      		
						      	</div>
						      </div>
						      

					    </div>

						

						  <br/>
						  <br/>
					</div>
			);
		}
		else {
			return(
				<div>
					Loading...
				</div>
			)
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
				<h2>
					For year {this.state.year}, month {this.state.month}
				</h2>

				<div className="ui bulleted list">
					{this.renderStatistics()}
				</div>

			</div>
		);
	}

}

export default CarrierStatisticDetail;
