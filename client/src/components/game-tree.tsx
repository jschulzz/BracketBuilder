import React from "react";
import { Game, Team } from "../types/types";
import TeamCard from "./team-card";
import "./game-tree.css";
import { ArcherElement } from "react-archer";
import { getPreviousRound } from "../transformers/bracket.transformer";

export const GameTree = ({ game }: gameTreeProps) => {
	const getTeamOrder = (match: Game | null): Team[] => {
		if (match) {
			if (match.winner.parent_match && match.loser.parent_match) {
				if (
					match.winner.parent_match.game_index <
					match.loser.parent_match.game_index
				) {
					return [match.winner, match.loser];
				}
				return [match.loser, match.winner];
			}
			return [match.winner, match.loser].sort((t: Team) => t.seed);
		}
		return [];
	};
	const [firstTeam, secondTeam] = getTeamOrder(game);

	// console.log(game);
	return (
		<React.Fragment>
			{firstTeam.parent_match && secondTeam.parent_match ? (
				<div className="game-holder">
					<div className="parent upper">
						<GameTree game={firstTeam.parent_match} />
					</div>
					<div className="child">
						<TeamCard team={game.winner} />
					</div>
					<div className="parent lower">
						<GameTree game={secondTeam.parent_match} />
					</div>
				</div>
			) : (
				<div className="game-holder">
					<div className="parent upper first-round">
						<TeamCard team={firstTeam} />
					</div>
					<div className="child">
						<TeamCard team={game.winner} />
					</div>
					<div className="parent lower first-round">
						<TeamCard team={secondTeam} />
					</div>
				</div>
			)}
		</React.Fragment>
	);
};

interface gameTreeProps {
	game: Game;
}
