import React from "react";
import { transformBracketData } from "../transformers/bracket.transformer";
import { PythonBracketData, Game } from "../types/types";
import TeamCard from "./team-card";
import { ArcherContainer } from "react-archer";
import "./bracket.css";
import { GameTree } from "./game-tree";

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

const Bracket = ({ teamData }: bracketProps) => {
	const transformedData = transformBracketData(teamData);
	console.log(transformedData);
	const allMatchups = getMatchups(transformedData.championship, []);
	console.log(allMatchups);
	return (
		<ArcherContainer>
			{/* <div className="champion">
				<TeamCard team={transformedData.championship.winner} />;
			</div> */}
			<div className="champion">
				{/* <TeamCard team={transformedData.championship.winner} />; */}
				<GameTree game={transformedData.championship} />
			</div>
		</ArcherContainer>
	);
};

interface bracketProps {
	teamData: PythonBracketData;
}

export default Bracket;
