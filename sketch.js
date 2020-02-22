let data;
let logo;

// TODO: revisit this, seems very clunky and non-intuitive
// Maybe even redo this in React? 
// If I want to make it interactive (i.e. the user can override matchups), i'd have to make API calls to the server to re-calculate matchups
// it's not worth precalculating all matchups

let x_divisions = {
    "64": 50,
    "32": 190,
    "16": 330,
    "8": 470,
    "4": 590
};
function preload() {
    data = loadJSON("client/src/result_bracket.json");
    logo = loadImage("images/logo.png");
    console.log(data);
}
function setup() {
    let c = createCanvas(1500, 800);
    c.parent("sketch-holder");
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
        } else {
            var row = table.insertRow(t);
            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);
            var cell5 = row.insertCell(4);
            var cell6 = row.insertCell(5);
            var cell7 = row.insertCell(6);
            let odds_64 = data[t]["round_of_64"];
            let odds_32 = data[t]["round_of_32"] * odds_64;
            let odds_16 = data[t]["round_of_16"] * odds_32;
            let odds_8 = data[t]["round_of_8"] * odds_16;
            let odds_4 = data[t]["round_of_4"] * odds_8;
            let odds_2 = data[t]["round_of_2"] * odds_4;
            cell1.innerHTML = t;
            cell2.innerHTML = (100 * odds_64).toFixed(1) + "%";
            cell3.innerHTML = (100 * odds_32).toFixed(1) + "%";
            cell4.innerHTML = (100 * odds_16).toFixed(1) + "%";
            cell5.innerHTML = (100 * odds_8).toFixed(1) + "%";
            cell6.innerHTML = (100 * odds_4).toFixed(1) + "%";
            cell7.innerHTML = (100 * odds_2).toFixed(1) + "%";
        }
    });

    sortTable();

    background(200);
    textAlign(CENTER);
    imageMode(CENTER);
    rectMode(RADIUS);

    image(logo, width / 2, 100, 300, 120);
    strokeWeight(2);
    for (let i = 64; i >= 4; i /= 2) {
        console.log(i)
        noStroke();
        fill(255, 255, 255, 50);
        rectMode(CORNER);
        rect(0, 0, x_divisions[i.toString()], height);
        rect(width - x_divisions[i.toString()], 0, width, height);
    }
    makeSide(r64);
    makeSide(r32);
    makeSide(r16);
    makeSide(r8);
    makeSide(r4);
    team(
        r2[0],
        width / 2 - 50,
        height / 2 - 100,
        textWidth(r2[0].name) + 50,
        1.5
    );
    team(
        r2[1],
        width / 2 + 50,
        height / 2 + 100,
        textWidth(r2[1].name) + 50,
        1.5
    );
    team(r1[0], width / 2, height / 2, textWidth(r1[0].name) + 50, 2.2);

    // makeSide(r2, 750)
    // textSize(20);
    // text(data.method, width / 2, 700);
    noLoop();
    saveCanvas(c, "Opening" + "__" + getDay(), "png");
}
function draw() { }

let y_map = {
    "64": { s: 25, i: 10 },
    "32": { s: 50, i: 22 },
    "16": { s: 100, i: 46 },
    "8": { s: 200, i: 94 },
    "4": { s: 400, i: 190 },
    "2": { s: 800, i: 382 }
};

function makeSide(arr) {
    startx = x_divisions[arr.length.toString()];
    maxW = 0;
    for (let i = 0; i < arr.length; i++) {
        if (textWidth(arr[i].name) > maxW) {
            maxW = textWidth(arr[i].name);
            console.log(arr[i].name);
        }
    }
    for (let i = 0; i < arr.length; i++) {
        let region = Math.floor(i / (arr.length / 2));
        let gap = 3;
        let y_spacing = 25 * (5 - Math.log(2, arr.length));
        y_info = y_map[arr.length.toString()];
        y_spacing = y_info.s;
        y_initial = y_info.i;
        // console.log(r64[i], region)
        if (region == 0) {
            let centerx = startx + gap;
            let centery = i * y_spacing + y_initial + gap;
            if (i % 2 == 0 && arr.length > 4) {
                bracket(centery, centery + y_spacing + 4, centerx + maxW * 0.8);
            }
            team(arr[i], centerx, centery, maxW + 20);
        } else {
            centerx = width - startx - gap;
            centery = (i - arr.length / 2) * y_spacing + y_initial + gap;
            if (i % 2 == 0 && arr.length > 4) {
                bracket(centery, centery + y_spacing + 4, centerx - maxW * 0.8, true);
            }
            team(arr[i], centerx, centery, maxW + 20);
        }
    }
}

function bracket(y1, y2, x, reverse) {
    strokeWeight(2);
    stroke(0);
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
    line(x, v1, x + spacing, v1);
    line(x, v2, x + spacing, v2);
    line(x + spacing, v1, x + spacing, v2);
    line(x + spacing, (v1 + v2) / 2, x + spacing * 2, (v1 + v2) / 2);
}

function team(info, centerx, centery, w, s) {
    // let w = w;
    name =
        info.name +
        "(" +
        (info.seed + 1) +
        ") - " +
        (info.overall_chance * 100).toFixed(1) +
        "%";
    let h = 10;
    let gap = 4;
    if (s) {
        textSize(s * 12);
        w *= s;
        h *= s;
        gap *= s;
    }
    strokeWeight(2);
    stroke(0);
    fill(200, 255, 200);
    if (info.matchup_chance < 0.53) {
        fill(255, 200, 200);
    } else if (info.matchup_chance < 0.65) {
        fill(255, map(info.matchup_chance, 0.53, 0.65, 200, 255), 200);
    }
    rectMode(RADIUS);
    rect(centerx, centery, w * 0.8, h, h);
    strokeWeight(0);
    fill(0);
    text(name, centerx, centery + gap);
}

function getDay() {
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1; //January is 0!
    var yyyy = today.getFullYear();

    if (dd < 10) {
        dd = "0" + dd;
    }

    if (mm < 10) {
        mm = "0" + mm;
    }

    return mm + "/" + dd + "/" + yyyy;
}

function sortTable() {
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
}
