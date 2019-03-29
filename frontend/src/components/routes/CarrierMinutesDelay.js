import React from 'react';
import calls_root from '../../api/calls_root';
import MonthYearPicker from 'react-month-year-picker';


class CarrierMinutesDelay extends React.Component {

	constructor(props){
		super(props);
		this.state = {
			delays: null,
			carrier_code: null,
			airport: "",
			month: 6,
			year: 2003,
			pick_date: false,
			airports: null
		}
	}

	 handleChange(event) {
	    this.setState({airport: event.target.value});
	  }

	  handleSubmit = (event) => {
	  	event.preventDefault();
	    console.log('Your airport is: ' + this.state.airport);
	    console.log('Your year is: ' + this.state.year);
	    console.log('Your month is: ' + this.state.month);


	    this.getDelays(this.state.airport, this.state.year, this.state.month);


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

	renderFilterBar() {

		

			return(
				<form onSubmit={this.handleSubmit}>
			        <label>
			          Pick an airport:
			          <select value={this.state.airport} onChange={(e) => {this.setState({airport: e.target.value})}}>
			            <option value={null}>Any airport</option>
			            {this.renderAirports()}
			          </select>
			        </label>

			        <br/>
					<div className="ui slider checkbox">
						<input type="checkbox" name="pick_date" checked={this.state.pick_date} onChange={(e) => this.setState({pick_date: !this.state.pick_date})}/>
						<label>Pick date?</label>
					</div> 

			        {this.state.pick_date && <div className="edit">
                    	 <MonthYearPicker
				          selectedMonth={this.state.month}
				          selectedYear={this.state.year}
				          minYear={2003}
				          maxYear={2018}
				          onChangeYear={year => this.setState({ year: year })}
				          onChangeMonth={month => this.setState({ month: month })}
        					/>
				        <h3>Selected month: {this.state.month}</h3>
				        <h3>Selected year: {this.state.year}</h3>
	                </div>}


	                <br/>
			        <input type="submit" value="Filter" />
			      </form>
			);

	}

	renderDelays() {
		if (this.state.delays){
			return this.state.delays.map( delay => {
				return(
					<div  className="item" key={`${delay.time}/${delay.airport}`}>
						
						<div>
							<div style={{ fontWeight: 'bold' }}>
								<h3>Time: {delay.time}     Time: {delay.airport}</h3>
							</div>

							

							<div className="list">
							      		<div className="item">Late aircraft:{delay.late_aircraft}</div>
							      		<div className="item">Weather:{delay.weather}</div>
							      		<div className="item">Carrier:{delay.carrier}</div>
							      		<div className="item">Security:{delay.security}</div>
							      		<div className="item">Total:{delay.total}</div>
							      		<div className="item">National aviation system:{delay.national_aviation_system}</div>
							      		
							</div>

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

	getDelays = async (airport=null, year=null, month=null, first=false) => {
		// console.log(this.props.match.params.carrier_code);
		this.setState({
			carrier_code:this.props.match.params.carrier_code
		});


		console.log(airport);
		console.log(year);
		console.log(month);
		console.log(first);
		console.log(this.state.pick_date);

		let response;

		if (first===true){
			response = await calls_root.get(`/carriers/${this.props.match.params.carrier_code}/delays-minutes`, {});
		}
		else{

			if(airport && this.state.pick_date){
				response = await calls_root.get(`/carriers/${this.props.match.params.carrier_code}/delays-minutes?airport=${airport}&year=${year}&month=${month}`, {});
			}
			
			if( airport && !this.state.pick_date){
				response = await calls_root.get(`/carriers/${this.props.match.params.carrier_code}/delays-minutes?airport=${airport}`, {});
			}
			
			if( airport==="" && this.state.pick_date){
				response = await calls_root.get(`/carriers/${this.props.match.params.carrier_code}/delays-minutes?year=${year}&month=${month}`, {});
			}

		}

	
		this.setState({
			delays: response.data
		})
		console.log(response);
	}

	componentDidMount() {
		this.getDelays(null, null, null, true);
		this.getAirports();
	}

	render() {
		return(
			<div>
				<h1>
					Statistics for carrier {this.state.carrier_code}
				</h1>
				<div className="ui bulleted list">
					{this.renderFilterBar()}
					 {this.renderDelays()}
				</div>
			</div>
		);
	}

}
export default CarrierMinutesDelay;