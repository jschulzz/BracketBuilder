import {Game, Team, PythonBracketData, PythonBracketTeam} from '../types/types'

const findTeam = (all_teams: Team[], team_name: string): Team => {
	return all_teams.filter((team: Team) => team.name === team_name)[0];
};

const pythonTeamtoTeam = (team: PythonBracketTeam): Team => {
	return {
		seed: team.seed,
		name: team.name,
		parent_match: null
	};
};

const getPreviousRound = (round: string): string => {
	return "round_of_" + Number(round.split("_")[2]) * 2;
};
const getNextRound = (round: string): string => {
	return "round_of_" + Number(round.split("_")[2]) / 2;
};

const copyTeam = (team: Team): Team => {
	return {
		seed: team.seed,
		name: team.name,
		parent_match: null
	};
};

const findParentMatch = (
	data: PythonBracketData,
	thisRound: string,
	thisTeam: Team
): Game => {
	const previousRound = getPreviousRound(thisRound);
	return {
		winner: copyTeam(thisTeam),
		loser: getOpponenetInRound(data, thisTeam, thisRound),
		likelihood: data[thisRound].filter(
			(team: PythonBracketTeam) => team.name === thisTeam.name
		)[0].matchup_chance
	};
};

const calculateParents = (
	game: Game,
	data: PythonBracketData,
	round: string
) => {
	console.log("finding parents of a Round", round, "Matchup");
	const previousRound = getPreviousRound(round);
	game.winner.parent_match = findParentMatch(data, previousRound, game.winner);
	game.loser.parent_match = findParentMatch(data, previousRound, game.loser);
	if (Number(previousRound.split("_")[2]) < 35) {
		calculateParents(game.winner.parent_match, data, previousRound);
		calculateParents(game.loser.parent_match, data, previousRound);
	}
};

const getOpponenetInRound = (
	data: PythonBracketData,
	thisTeam: Team,
	round: string
): Team => {
	const index = data[round].findIndex((team: PythonBracketTeam) => {
		return team.name === thisTeam.name;
	});
	const opponentIndex = index + (index % 2 === 0 ? 1 : -1);
	const opponent = data[round][opponentIndex];
	return pythonTeamtoTeam(opponent);
};

const didMakeToNextRound = (
	data: PythonBracketData,
	round_name: string,
    team_name: string
    
) => {
	const next_round_name = getNextRound(round_name);
	return data[next_round_name].find((team: PythonBracketTeam) => team.name === team_name);
};

export const transformBracketData = (data: PythonBracketData) => {
	let bracket: { championship: Game | null } = { championship: null };
	let all_teams: Team[] = [];
	data.round_of_64.forEach((team: any) => {
		all_teams.push(pythonTeamtoTeam(team));
	});
	const overall_winner = findTeam(all_teams, data.round_of_1[0].name);
	const runner_up = getOpponenetInRound(data, overall_winner, "round_of_2");
	bracket.championship = {
		winner: overall_winner,
		loser: runner_up,
		likelihood: data.round_of_1[0].matchup_chance
	};
	calculateParents(bracket.championship, data, "round_of_2");
	console.log(bracket);
    console.log(data);
    
};
