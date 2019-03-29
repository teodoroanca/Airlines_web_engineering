import React from 'react';

const DescriptiveStatisticElement = (props) => {
	return (
		<div className="list item">
			<div className="list">

					<h4>
						Mean: {props.mean}
					</h4>
					<h4>
						Median: {props.median}
					</h4>
					<h4>
						Median: {props.standard_deviation}
					</h4>
					<br/>
					<br/>
			</div>
		</div>
	);
}

export default DescriptiveStatisticElement;