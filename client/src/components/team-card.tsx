import React, { useState } from "react";
import { Team, Game } from "../types/types";
import "./team-card.css";
import { getNextRound } from "../transformers/bracket.transformer";
import { ArcherElement } from "react-archer";
import Tag from "@atlaskit/tag";
import Avatar from "@atlaskit/avatar";
import Lozenge from "@atlaskit/lozenge";
import Drawer from "@atlaskit/drawer";
const TeamCard = ({ team }: teamCardProps) => {
	let lozengeSize = 0;
	const [drawerOpen, setDrawerOpen] = useState(false);

	const shrinkLozenge = () => {
		console.log("shrinking", team);
		const interval = setInterval(() => {
			lozengeSize -= 10;
			if (lozengeSize < 20) {
				console.log("shrinking", team);
				clearInterval(interval);
			}
		}, 50);
	};
	const growLozenge = () => {
		const interval = setInterval(() => {
			lozengeSize += 10;
			if (lozengeSize > 200) {
				clearInterval(interval);
			}
		}, 50);
	};

	const clickTeam = () => {
		setDrawerOpen(true);
		// console.log("Opening Drawer");
	};

	const closeDrawer = (...args: any) => {
		// console.log("onClose", args);
		setDrawerOpen(false);
	};

	return (
		<React.Fragment>
			<Drawer isOpen={drawerOpen || false} width="wide" onClose={closeDrawer}>
				{team.name}
			</Drawer>
			<div className={`team-name`}>
				<div className="tag">
					<div className="cover" onClick={clickTeam}>
						<Tag
							text={`${team.name} (${team.seed + 1})`}
							elemBefore={
								<div>
									<Avatar
										size="medium"
										src={team.logo_url}
										appearance="square"
										borderColor="lightgrey"
									/>
									<div className="filler" />
								</div>
							}
						/>
					</div>
				</div>
			</div>
		</React.Fragment>
	);
};

interface teamCardProps {
	team: Team;
}
export default TeamCard;
