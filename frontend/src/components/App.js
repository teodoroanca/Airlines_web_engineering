import React from 'react';
import {Router, Route, Switch} from 'react-router-dom';

import Home from './routes/Home';
import AirportsAll from './routes/AirportsAll';
import CarriersAll from './routes/CarriersAll';
import OperatingCarriers from './routes/OperatingCarriers';
import CarrierAllStatistics from './routes/CarrierAllStatistics';
import CarrierStatisticDetail from './routes/CarrierStatisticDetail';
import CarrierMinutesDelay from './routes/CarrierMinutesDelay';
import DescriptiveStatistics from './routes/DescriptiveStatistics';
import DescriptiveStatisticsDetail from './routes/DescriptiveStatisticsDetail';

import Header from './Header';
import history from '../history';

class App extends React.Component {

	render() {
		return (
			<div className="ui container">
				<Router history={history}>
					<div>
						<Header />
						<Switch>
							<Route path="/" exact component={Home} />
							<Route path="/airports/" exact component={AirportsAll} />
							<Route path="/airports/:code/operating-carriers" exact component={OperatingCarriers} />
							<Route path="/airports/:airport_code/operating-carriers/:carrier_code/statistics" exact component={CarrierAllStatistics} />
							<Route path="/airports/:airport_code/operating-carriers/:carrier_code/statistics/:year/:month" exact component={CarrierStatisticDetail} />

							<Route path="/carriers/" exact component={CarriersAll} />
							<Route path="/carriers/:carrier_code" exact component={CarrierMinutesDelay} />

							<Route path="/descriptive-statistics/" exact component={DescriptiveStatistics} />
							<Route path="/descriptive-statistics/:airport1/:airport2/:carrier" exact component={DescriptiveStatisticsDetail} />


						</Switch>
					</div>
				</Router>
			</div>
		);
	}
}

export default App;