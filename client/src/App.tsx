import React, { useEffect } from "react";
import logo from "./logo.svg";
import Bracket from "./components/bracket";
import data from "./result_bracket.json";
import "./App.css";

const App: React.FC = () => {
	return (
		<div className="App">
			<Bracket teamData={data} />
		</div>
	);
};

export default App;
