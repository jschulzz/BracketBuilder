import React, { useEffect } from "react";
import logo from "./logo.svg";
import Bracket from "./components/bracket";
import bracketData from "./result_bracket.json";
import "./App.css";

const App: React.FC = () => {
	return (
		<div className="App">
			<Bracket teamData={bracketData} />
		</div>
	);
};

export default App;
