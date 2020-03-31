
let nextId = 1;
const now = new Date();

export function defaultPlans() {
    let plans = [];
    for (let i = 0; i < 50; i++) {
        plans.push(plan())
    }
    return plans;
}

export function newPlan(title, date) {
    nextId++;
    return {
        id: nextId,
        title: title,
        uploaded: date,
        user: 'a user',
        summary: [],
        roadClass: 'unknown',
    }
}

function plan() {
    nextId++;
    let s = {
        id: nextId,
        title: "Plan " + nextId,
        uploaded: new Date(now.valueOf() - nextId * Math.random()),
        user: 'a user',
        summary: summary(),
        roadClass: '',
    }
    s.roadClass = [...new Set(Array.from(s.summary.map(si => si.roadClass)))].join(', ');
    return s;
}

const WORK_TYPES = ['routine', 'periodic', 'rehab'];

function summary() {
    const roadClass = randomRoadClass()
    return [].concat(...WORK_TYPES.map(workType => {
        return [].concat(...[2020, 2021, 2022, 2023, 2024].map(year => {
            return {
                roadClass: roadClass,
                year: year,
                budget: Number(20 + (Math.random() * 30).toFixed(2)),
                length: Number(200 + (Math.random() * 300).toFixed(2)),
                workType: workType
            };
        }));
    }));
}
function randomFrom(choices) {
    return choices[Math.floor(Math.random() * choices.length)];
}

const ROAD_CLASSES = ['nat', 'mun', 'rur', 'urb'];

function randomRoadClass() {
    return randomFrom(ROAD_CLASSES);
}
