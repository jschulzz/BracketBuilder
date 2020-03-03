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
	opponent: string;
	name: string;
	winner: string;
}

export interface Assignment {
	match: string[];
	winner: string;
}

export interface Player {
	name: string;
	started: number;
	minutes: number;
	fga: number;
	fg: number;
	fg2a: number;
	fg2: number;
	fg3a: number;
	fg3: number;
	fta: number;
	ft: number;
	orb: number;
	drb: number;
	ast: number;
	stl: number;
	blk: number;
	tov: number;
	pf: number;
	pts: number;
}
export interface PythonTeamData {
	g: number;
	mp: number;
	fg: number;
	fga: number;
	fg_pct: number;
	fg2: number;
	fg2a: number;
	fg2_pct: number;
	fg3: number;
	fg3a: number;
	fg3_pct: number;
	ft: number;
	fta: number;
	ft_pct: number;
	orb: number;
	drb: number;
	trb: number;
	ast: number;
	stl: number;
	blk: number;
	tov: number;
	pf: number;
	pts: number;
	pts_per_g: number;
	players: Player[];
	weights: number[];
	heights: number[];
	jersey_nums: number[];
	hometowns: string[];
	player_pts: number[];
	offensive: number;
	defensive: number;
	sos: number;
	points_scored: number;
	points_against: number;
	logo_url: string;
	main_color: string;
	wins: Object;
}
