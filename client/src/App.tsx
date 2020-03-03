import React, { useEffect, useState } from "react";
// import logo from "./logo.svg";
import "./App.css";
import P5Wrapper from "react-p5-wrapper";
import {
	PythonBracketData,
	PythonBracketTeam,
	PythonTeamData,
	Assignment
} from "./types/types";
import { Bar } from "react-chartjs-2";
import hexToRgba from "hex-to-rgba";
import isEqual from "lodash/isEqual";
import Modal, { ModalTransition } from "@atlaskit/modal-dialog";
import Button, { ButtonGroup } from "@atlaskit/button";

const App: React.FC = () => {
	const [teamData, setTeamData] = useState<PythonBracketData>({});
	const [dataRecieved, setDataRecieved] = useState(false);
	const [selectedTeam, setSelectedTeam] = useState<
		PythonBracketTeam | undefined
	>(undefined);
	const [compareData, setCompareData] = useState<any>(undefined);
	const [assignedMatches, setAssignedMatches] = useState<Assignment[]>([]);

	const getTeam = async team_name => {
		const res = await fetch("http://localhost:5000/team/" + team_name);
		return res.json().then(data => {
			return data;
		});
	};
	const fetchData = async () => {
		if (!dataRecieved) {
			const res = await fetch("http://localhost:5000/");
			res.json().then(data => {
				setTeamData(data);
				console.log(teamData);
				setDataRecieved(true);
			});
		}
	};

	useEffect(() => {
		fetchData();
	});

	function assignMatch(info: PythonBracketTeam) {
		let newAssignedMatches = assignedMatches;
		const thisAssignment: Assignment = {
			match: [info.name, info.opponent].sort(),
			winner: info.name
		};
		const refreshedAssignments = assignedMatches.filter(
			assignment =>
				!isEqual(assignment.match.sort(), thisAssignment.match.sort())
		);
		refreshedAssignments.push({
			match: [info.name, info.opponent],
			winner: info.name
		});
		console.log(refreshedAssignments);
		fetch("http://localhost:5000/challenge", {
			method: "post",
			body: JSON.stringify(refreshedAssignments)
		});
		console.log(refreshedAssignments);
		setAssignedMatches(refreshedAssignments);
		setDataRecieved(false);
	}

	const sketch = p5 => {
		let width = 0;
		let height = 0;
		p5.setup = () => {
			p5.createCanvas(1500, 800);
			width = 1500;
			height = 800;
		};

		p5.y_map = {
			"64": { s: 25, i: 10 },
			"32": { s: 50, i: 22 },
			"16": { s: 100, i: 46 },
			"8": { s: 200, i: 94 },
			"4": { s: 400, i: 190 },
			"2": { s: 800, i: 382 }
		};

		p5.draw = () => {
			const x_divisions = {
				"64": 50,
				"32": 190,
				"16": 330,
				"8": 470,
				"4": 590
			};
			// background zones
			for (let i = 64; i >= 4; i /= 2) {
				p5.noStroke();
				p5.fill(255, 255, 255, 50);
				p5.rectMode(p5.CORNER);
				p5.rect(0, 0, x_divisions[i.toString()], height);
				p5.rect(width - x_divisions[i.toString()], 0, width, height);
			}
			if (dataRecieved) {
				let r64 = teamData.round_of_64;
				let r32 = teamData.round_of_32;
				let r16 = teamData.round_of_16;
				let r8 = teamData.round_of_8;
				let r4 = teamData.round_of_4;
				let r2 = teamData.round_of_2;
				let r1 = teamData.round_of_1;

				Object.keys(teamData).forEach(t => {
					if (
						[
							"round_of_64",
							"round_of_32",
							"round_of_16",
							"round_of_8",
							"round_of_4",
							"round_of_2",
							"round_of_1",
							"method"
						].includes(t)
					) {
						return;
					}
				});

				p5.background(200);
				p5.textAlign(p5.CENTER);
				p5.imageMode(p5.CENTER);
				p5.rectMode(p5.RADIUS);

				// p5.image(logo, width / 2, 100, 300, 120);
				p5.strokeWeight(2);

				makeSide(p5, x_divisions, r64);
				makeSide(p5, x_divisions, r32);
				makeSide(p5, x_divisions, r16);
				makeSide(p5, x_divisions, r8);
				makeSide(p5, x_divisions, r4);
				drawTeam(
					p5,
					r2[0],
					width / 2 - 50,
					height / 2 - 100,
					p5.textWidth(r2[0].name) + 50,
					1.5
				);
				drawTeam(
					p5,
					r2[1],
					width / 2 + 50,
					height / 2 + 100,
					p5.textWidth(r2[1].name) + 50,
					1.5
				);
				drawTeam(
					p5,
					r1[0],
					width / 2,
					height / 2,
					p5.textWidth(r1[0].name) + 50,
					2.2
				);
			}
		};

		const makeSide = (p5, x_divisions, arr) => {
			let startx = x_divisions[arr.length.toString()];
			let maxW = 0;
			p5.textSize(12);
			for (let i = 0; i < arr.length; i++) {
				if (p5.textWidth(arr[i].name) > maxW) {
					maxW = p5.textWidth(arr[i].name);
				}
			}
			for (let i = 0; i < arr.length; i++) {
				let region = Math.floor(i / (arr.length / 2));
				let gap = 3;
				let y_info = p5.y_map[arr.length.toString()];
				let y_spacing = y_info.s;
				let y_initial = y_info.i;
				if (region === 0) {
					let centerx = startx + gap;
					let centery = i * y_spacing + y_initial + gap;
					if (i % 2 === 0 && arr.length > 4) {
						bracket(
							p5,
							centery,
							centery + y_spacing + 4,
							centerx + maxW * 0.8,
							undefined
						);
					}
					drawTeam(p5, arr[i], centerx, centery, maxW + 20, 1);
				} else {
					let centerx = width - startx - gap;
					let centery = (i - arr.length / 2) * y_spacing + y_initial + gap;
					if (i % 2 === 0 && arr.length > 4) {
						bracket(
							p5,
							centery,
							centery + y_spacing + 4,
							centerx - maxW * 0.8,
							true
						);
					}
					drawTeam(p5, arr[i], centerx, centery, maxW + 20, 1);
				}
			}
		};

		const bracket = (p5, y1, y2, x, reverse) => {
			p5.strokeWeight(2);
			p5.stroke(0);
			let y_spacing = -3;
			let v1 = y1 + y_spacing;
			let v2 = y2 + y_spacing;
			let spacing = 20;
			if (reverse) {
				spacing = -spacing;
			}
			p5.line(x, v1, x + spacing, v1);
			p5.line(x, v2, x + spacing, v2);
			p5.line(x + spacing, v1, x + spacing, v2);
			p5.line(x + spacing, (v1 + v2) / 2, x + spacing * 2, (v1 + v2) / 2);
		};

		const drawTeam = (p5, info, centerx, centery, w, s) => {
			info.drawerOpen = false;
			let name = info.name + "(" + (info.seed + 1) + ")";

			let h = 10;
			let gap = 4;
			p5.textSize(s * 12);
			w *= s;
			h *= s;
			gap *= s;
			p5.fill(0, 30);
			p5.strokeWeight(0);
			p5.rect(centerx, centery + 3, w * 0.8 + 1, h, h * 0.25);
			p5.strokeWeight(1);
			p5.stroke(0, 100);
			p5.fill(200, 255, 200);
			if (info.matchup_chance < 0.53) {
				p5.fill(255, 200, 200);
			} else if (info.matchup_chance < 0.65) {
				p5.fill(255, p5.map(info.matchup_chance, 0.53, 0.65, 200, 255), 200);
			}
			p5.rectMode(p5.RADIUS);
			p5.rect(centerx, centery, w * 0.8, h, h * 0.25);
			if (
				!selectedTeam &&
				p5.mouseX < centerx + w * 0.8 &&
				p5.mouseX > centerx - w * 0.8 &&
				p5.mouseY > centery - h &&
				p5.mouseY < centery + h
			) {
				p5.fill(0, 90);
				p5.rect(centerx, centery, w * 0.8, h, h * 0.25);
				const infobox_text =
					"Chance to get here: " +
					(info.overall_chance * 100).toFixed(0) +
					"%\nChance to win previous match: " +
					(info.matchup_chance * 100).toFixed(0) +
					"%";
				const infobox_width = 200 * s;
				const infobox_height = 40 * s;
				const infobox_y = p5.mouseY - infobox_height;
				const infobox_x = p5.mouseX;
				const margin = 5 * s;
				p5.textAlign(p5.LEFT);
				p5.rectMode(p5.CORNER);
				p5.rect(infobox_x, infobox_y, infobox_width, infobox_height, h * 0.25);
				p5.fill(255, 200);
				p5.strokeWeight(0);
				p5.text(infobox_text, infobox_x + margin, infobox_y + 3 * margin);
				p5.textAlign(p5.CENTER);
				p5.rectMode(p5.CENTER);
				if (p5.mouseIsPressed) {
					// assignMatch(info);
					setSelectedTeam(info);
					getTeam(info.name).then((home_data: PythonTeamData) => {
						getTeam(info.opponent).then((away_data: PythonTeamData) => {
							console.log(home_data);
							console.log(away_data);
							setCompareData({
								labels: ["SOS", "Off. Eff.", "Def. Eff.", "FG %"],
								datasets: [
									{
										label: info.name,
										backgroundColor: hexToRgba(home_data.main_color, 0.6),
										borderColor: hexToRgba(home_data.main_color, 1),
										borderWidth: 1,
										data: [
											home_data.sos,
											home_data.offensive,
											home_data.defensive,
											home_data.fg_pct * 100
										]
									},
									{
										label: info.opponent,
										backgroundColor: hexToRgba(away_data.main_color, 0.6),
										borderColor: hexToRgba(away_data.main_color, 1),
										borderWidth: 1,
										data: [
											away_data.sos,
											away_data.offensive,
											away_data.defensive,
											away_data.fg_pct * 100
										]
									}
								]
							});
						});
					});
				}
			}
			p5.strokeWeight(0);
			p5.fill(0);
			p5.text(name, centerx, centery + gap);
		};
	};

	return (
		<div className="App">
			{selectedTeam && compareData && (
				<ModalTransition>
					<Modal
						actions={[
							{ text: `Set ${selectedTeam.name} to winner` },
							{ text: `Set ${selectedTeam.opponent} to winner` }
						]}
						heading={`${selectedTeam.name} vs ${selectedTeam.opponent}`}
						onClose={() => setSelectedTeam(undefined)}
					>
						<Bar data={compareData} width={800} height={400}></Bar>
					</Modal>
				</ModalTransition>
			)}
			<P5Wrapper sketch={sketch} bracket={teamData} />
			{assignedMatches.map(assignment => {
				return (
					<div>
						<h1>{assignment.match}</h1>
						<h2>{assignment.winner}</h2>
					</div>
				);
			})}
		</div>
	);
};

export default App;
