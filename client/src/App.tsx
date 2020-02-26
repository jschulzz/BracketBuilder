import React from "react";
import logo from "./logo.svg";
import Bracket from "./components/bracket";
import axios from "axios";
import "./App.css";
import Sketch from "react-p5";
import { PythonBracketData } from "./types/types";

const App: React.FC = () => {
	let data: PythonBracketData = {};
	let width = 0;
	let height = 0;
	let clickZones: any[] = [];

	const setup = (p5, canvasParentRef) => {
		p5.createCanvas(1500, 800).parent(canvasParentRef); // use parent to render canvas in this ref (without that p5 render this canvas outside your component)
		width = 1500;
		height = 800;
	};
	const preload = () => {
		const fetchBracket = async () => {
			const teamData = await axios.get("http://localhost:5000/");
			// console.log(teamData);
			data = teamData.data;
		};
		fetchBracket();
	};

	const draw = p5 => {
		if (Object.entries(data).length === 0 && data.constructor === Object) {
			return;
		}
		// console.log(data);
		let r64 = data.round_of_64;
		let r32 = data.round_of_32;
		let r16 = data.round_of_16;
		let r8 = data.round_of_8;
		let r4 = data.round_of_4;
		let r2 = data.round_of_2;
		let r1 = data.round_of_1;

		Object.keys(data).forEach(t => {
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
		for (let i = 64; i >= 4; i /= 2) {
			p5.noStroke();
			p5.fill(255, 255, 255, 50);
			p5.rectMode(p5.CORNER);
			p5.rect(0, 0, x_divisions[i.toString()], height);
			p5.rect(width - x_divisions[i.toString()], 0, width, height);
		}
		makeSide(p5, r64);
		makeSide(p5, r32);
		makeSide(p5, r16);
		makeSide(p5, r8);
		makeSide(p5, r4);
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
		console.log(p5.frameRate());
		// p5.noLoop();
		// p5.saveCanvas("Opening" + "__" + getDay(), "png");
	};

	let y_map = {
		"64": { s: 25, i: 10 },
		"32": { s: 50, i: 22 },
		"16": { s: 100, i: 46 },
		"8": { s: 200, i: 94 },
		"4": { s: 400, i: 190 },
		"2": { s: 800, i: 382 }
	};

	let x_divisions = {
		"64": 50,
		"32": 190,
		"16": 330,
		"8": 470,
		"4": 590
	};

	const makeSide = (p5, arr) => {
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
			// let y_spacing = 25 * (5 - Math.log(2, arr.length));
			let y_info = y_map[arr.length.toString()];
			let y_spacing = y_info.s;
			let y_initial = y_info.i;
			// console.log(r64[i], region)
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
			// rect(x + spacing, 0, width, height);
		} else {
			// rect(0, 0, x + spacing, height);
		}
		p5.line(x, v1, x + spacing, v1);
		p5.line(x, v2, x + spacing, v2);
		p5.line(x + spacing, v1, x + spacing, v2);
		p5.line(x + spacing, (v1 + v2) / 2, x + spacing * 2, (v1 + v2) / 2);
	};

	const drawTeam = (p5, info, centerx, centery, w, s) => {
		let name =
			info.name +
			"(" +
			(info.seed + 1) +
			") - " +
			(info.matchup_chance * 100).toFixed(1) +
			"%";
		let h = 10;
		let gap = 4;
		p5.textSize(s * 12);
		w *= s;
		h *= s;
		gap *= s;
		p5.strokeWeight(2);
		p5.stroke(0);
		p5.fill(200, 255, 200);
		if (info.matchup_chance < 0.53) {
			p5.fill(255, 200, 200);
		} else if (info.matchup_chance < 0.65) {
			p5.fill(255, p5.map(info.matchup_chance, 0.53, 0.65, 200, 255), 200);
		}
		p5.rectMode(p5.RADIUS);
		p5.rect(centerx, centery, w * 0.8, h, h);
		// if (centerx == hovered.x && centery == hovered.y) {
		if (
			p5.mouseX < centerx + w * 0.8 &&
			p5.mouseX > centerx - w * 0.8 &&
			p5.mouseY > centery - h &&
			p5.mouseY < centery + h
		) {
			p5.fill(0, 90);
			p5.rect(centerx, centery, w * 0.8, h, h);
		}
		clickZones.push({
			centerx,
			centery,
			width: w * 0.8,
			height: h,
			team: info
		});
		p5.strokeWeight(0);
		p5.fill(0);
		p5.text(name, centerx, centery + gap);
	};

	const mousePressed = p5 => {
		let mousex = p5.mouseX;
		let mousey = p5.mouseY;
		for (let zone of clickZones) {
			let left = zone.centerx - zone.width;
			let top = zone.centery - zone.height;
			let right = zone.centerx + zone.width;
			let bottom = zone.centery + zone.height;

			if (mousex < right && mousex > left && mousey < bottom && mousey > top) {
				// console.log(zone.info)
			}
		}
	};

	const getDay = () => {
		var today = new Date();
		var dd = today.getDate();
		var mm = today.getMonth() + 1; //January is 0!
		var yyyy = today.getFullYear();
		let day = dd.toString();
		let month = mm.toString();

		if (dd < 10) {
			day = "0" + dd;
		}

		if (mm < 10) {
			month = "0" + mm;
		}

		return month + "/" + day + "/" + yyyy;
	};

	const sortTable = () => {
		var table, rows, switching, i, x, y, shouldSwitch;
		table = document.getElementById("table");
		switching = true;
		/* Make a loop that will continue until
  no switching has been done: */
		while (switching) {
			// Start by saying: no switching is done:
			switching = false;
			rows = table.rows;
			/* Loop through all table rows (except the
    first, which contains table headers): */
			for (i = 1; i < rows.length - 1; i++) {
				// Start by saying there should be no switching:
				shouldSwitch = false;
				/* Get the two elements you want to compare,
      one from current row and one from the next: */
				x = rows[i].getElementsByTagName("TD")[6];
				x = Number(x.innerHTML.substring(0, x.innerHTML.length - 1));
				y = rows[i + 1].getElementsByTagName("TD")[6];
				y = Number(y.innerHTML.substring(0, y.innerHTML.length - 1));
				//   console.log(x, y)
				// Check if the two rows should switch place:
				if (x > y) {
					// If so, mark as a switch and break the loop:
					shouldSwitch = true;
					break;
				}
			}
			if (shouldSwitch) {
				/* If a switch has been marked, make the switch
      and mark that a switch has been done: */
				rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
				switching = true;
			}
		}
	};

	return (
		<div className="App">
			{/* <Bracket /> */}
			<Sketch
				setup={setup}
				preload={preload}
				draw={draw}
				mousePressed={mousePressed}
			/>
		</div>
	);
};

export default App;
