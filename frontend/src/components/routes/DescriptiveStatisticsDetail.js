import React from 'react';
import calls_root from '../../api/calls_root';
import DescriptiveStatisticElement from './DescriptiveStatisticElement';

class DescriptiveStatisticsDetail extends React.Component {

	constructor(props){
		super(props);
		this.state = {
			airport1: this.props.match.params.airport1,
			airport2: this.props.match.params.airport2,
			descriptive_statistic: null,
			carrier: this.props.match.params.carrier
		}
	}


	getDescriptiveStatistic = async () => {
		let response;

		response = await calls_root.get(`/descriptive-statistics/${this.state.airport1}/second-airport/${this.state.airport2}/carriers/${this.state.carrier}`, {});
		
		this.setState({
			descriptive_statistic: response.data
		})

		console.log(this.state);
	}

	renderDescriptiveStatistic() {
		if (this.state.descriptive_statistic){
			return(
				<div>
					<DescriptiveStatisticElement mean={this.state.descriptive_statistic.mean} median={this.state.descriptive_statistic.median} standard_deviation={this.state.descriptive_statistic.standard_deviation}/>
				</div>
			)
		}
	}

	componentDidMount() {
		this.getDescriptiveStatistic();
	}

	render() {
		return (
			<div>
			{this.renderDescriptiveStatistic()}
			</div>
		);
	}
}

export default DescriptiveStatisticsDetail;