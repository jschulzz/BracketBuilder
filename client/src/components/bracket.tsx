import React from "react";
import { transformBracketData } from "../transformers/bracket.transformer";
import {PythonBracketData} from '../types/types'
import TeamCard from "./team-card";

const Bracket = ({ teamData }:bracketProps) => {
	const transformedData = transformBracketData(teamData)

	return <div>BRACKET!</div>;
};

interface bracketProps {
    teamData: PythonBracketData,
}

export default Bracket;
