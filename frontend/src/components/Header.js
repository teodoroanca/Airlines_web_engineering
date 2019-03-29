import React from 'react';
import {Link} from 'react-router-dom';

const Header = () => {
	return (
		<div className="ui one item menu">
			<Link to="/" className="item">
				Airlines
			</Link>
		</div>
	);
}

export default Header;