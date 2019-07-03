import React from "react";
import { Team, Game } from "../types/types";
import "./team-card.css";
import { getNextRound } from "../transformers/bracket.transformer";
import { ArcherElement } from "react-archer";
import Tag from "@atlaskit/tag";
import Avatar from "@atlaskit/avatar";
const TeamCard = ({ team }: teamCardProps) => {

    const showTag = false;

	return (
		<React.Fragment>
			<div
				className={`team-name`}
				onMouseEnter={() => console.log("mousign over", team)}
			>
				<Tag
					onClick={() => console.log("mousign over", team)}
					text={`${team.name} (${team.seed}) - ${
						team.parent_match ? team.parent_match.likelihood : ""
					}`}
					elemBefore={
						<Avatar
							onMouseEnter={() => console.log("mousign over", team)}
							src={team.logo_url}
							appearance="square"
							borderColor="lightgrey"
						/>
					}
				/>
			</div>
		</React.Fragment>
	);
};

interface teamCardProps {
	team: Team;
}
export default TeamCard;
