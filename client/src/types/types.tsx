export interface Game {
	winner: Team;
	loser: Team;
	likelihood: number;
	round: string;
	game_index: number;
}
export interface Team {
	seed: number;
	name: string;
	parent_match: Game | null;
	logo_url?: string;
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
