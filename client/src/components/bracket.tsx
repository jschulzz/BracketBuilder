import React, { useState, useEffect } from "react";
import { transformBracketData } from "../transformers/bracket.transformer";
import { PythonBracketData, Game } from "../types/types";
import TeamCard from "./team-card";
import { ArcherContainer } from "react-archer";
import "./bracket.css";
import { GameTree } from "./game-tree";
import axios from "axios";

const getMatchups = (data: Game, games: Game[]): Game[] => {
	games.push(data);
	if (data.winner.parent_match) {
		games = getMatchups(data.winner.parent_match, games);
	}
	if (data.loser.parent_match) {
		games = getMatchups(data.loser.parent_match, games);
	}
	return games;
};

const Bracket = () => {
	const [teamData, setTeamData] = useState(undefined);
	useEffect(() => {
		const fetchBracket = async () => {
			const teamData = await axios.get("http://localhost:5000/");
			console.log(teamData);
			setTeamData(teamData.data);
		};
		fetchBracket();
	}, []);
	const transformedData = transformBracketData(teamData);
	if (transformedData) {
		console.log(transformedData);
		const allMatchups = getMatchups(transformedData.championship, []);
		console.log(allMatchups);
		return (
			// <ArcherContainer>
			<React.Fragment>
				<div className="champion">
					{transformedData.championship && (
						<GameTree game={transformedData.championship}/>
					)}
				</div>
				{/* <div className="champion">
					{transformedData.championship.loser.parent_match && (
						<GameTree game={transformedData.championship.loser.parent_match} side="right"/>
					)}
				</div> */}
			</React.Fragment>
			// </ArcherContainer>
		);
	} else {
		return <div></div>;
	}
};

interface bracketProps {
	teamData: PythonBracketData;
}

export default Bracket;
