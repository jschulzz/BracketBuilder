import React from "react";
import { Team, Game } from "../types/types";
import "./team-card.css";
import { getNextRound } from "../transformers/bracket.transformer";
import { ArcherElement } from "react-archer";
import Tag from "@atlaskit/tag";
const TeamCard = ({ team }: teamCardProps) => {
	// console.log(team.name)

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
	console.log(team);
	const [firstTeam, secondTeam] = getTeamOrder(team.parent_match);
	const firstClasses = `${
		firstTeam && firstTeam.name === team.name ? "winner" : "loser"
	} `;
	const secondClasses = `${
		secondTeam && secondTeam.name === team.name ? "winner" : "loser"
	} `;
	// const firstClasses = `${firstTeam.name}-${team.parent_match.round} ${
	// 	firstTeam.name === team.name ? "winner" : "loser"
	// } `;
	// const secondClasses = `${secondTeam.name}-${team.parent_match.round} ${
	// 	secondTeam.name === team.name ? "winner" : "loser"
	// } `;
	return (
		<React.Fragment>
			{team.parent_match && (
				<div>
					<div className={firstClasses}>
						<TeamCard team={firstTeam} />
					</div>
				</div>
			)}
			<div className={`team-name`}>
				<ArcherElement
					id={`${team.name}-${
						team.parent_match
							? getNextRound(team.parent_match.round)
							: "round_of_64"
					}`}
					relations={
						team.parent_match
							? [
									{
										targetId: `${team.parent_match.winner.name}-${
											team.parent_match.round
										}`,
										sourceAnchor: "left",
										targetAnchor: "right"
									},
									{
										targetId: `${team.parent_match.loser.name}-${
											team.parent_match.round
										}`,
										sourceAnchor: "left",
										targetAnchor: "right"
									}
							  ]
							: []
					}
				>
					<Tag text={`${team.name} (${team.seed})`} />
				</ArcherElement>
			</div>
			{team.parent_match && (
				<div>
					<div className={secondClasses}>
						<TeamCard team={secondTeam} />
					</div>
				</div>
			)}
		</React.Fragment>
	);
};

interface teamCardProps {
	team: Team;
}
export default TeamCard;
