export interface Game {
	winner: Team;
	loser: Team;
	likelihood: number;
}
export interface Team {
	seed: number;
	name: string;
	parent_match: Game | null;
}
export interface PythonBracketData {
	[round: string]: PythonBracketTeam[];
}
export interface PythonBracketTeam {
	matchup_chance: number;
	overall_chance: number;
	seed: number;
	name: string;
}
