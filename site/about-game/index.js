
const toggleBtn = document.getElementById('theme-toggle');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

function setTheme(mode) {
    document.body.classList.remove('light', 'dark');
    document.body.classList.add(mode);
    toggleBtn.textContent = mode !== 'dark' ? '☀️' : '🌙';
    localStorage.setItem('theme', mode);
}

setTheme(localStorage.getItem('theme') || (prefersDark.matches ? 'dark' : 'light'));

toggleBtn.addEventListener('click', () => {
    const current = document.body.classList.contains('dark') ? 'dark' : 'light';
    setTheme(current === 'dark' ? 'light' : 'dark');
});

prefersDark.addEventListener('change', e => {
    setTheme(e.matches ? 'dark' : 'light');
});

const list = [
    { title: "Go to app", url: "https://www.takbuff.com", },
    { title: "Sepak takraw", url: "/about-game" },
];
const list1 = [
    {
        "title": "GitHub Repo",
        "url": "https://github.com/aburv/tsts",
    },
    {
        "title": "Contribute",
        "url": "https://github.com/aburv/tsts/blob/main/CONTRIBUTING.md",
        "external": true
    },
    {
        "title": "Report a Bug",
        "url": "https://github.com/aburv/tsts/issues/new?template=bug_report.md",
        "external": true
    },
    {
        "title": "Request a Feature",
        "url": "https://github.com/aburv/tsts/issues/new?template=feature_request.md",
        "external": true
    },
    {
        "title": "Code of Conduct",
        "url": "https://github.com/aburv/tsts/blob/main/CODE_OF_CONDUCT.md",
        "external": true
    }
];
const list2 = [
    { title: "Newsletter", url: "/newsletters" },
    { title: "Blog", url: "/blogs" },
    { title: "FAQ", url: "/faq" },
    { title: "Support", url: "/support" },
    { title: "Contact", url: "/contact" },
];
const list3 = [
    { title: "Privacy Policy", url: "/privacy" },
    { title: "Terms of Use", url: "/terms" },
];

function populateList(listId, items) {
    const ul = document.getElementById(listId);
    items.forEach(item => {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.href = item.url;
        a.textContent = item.title;

        const isExternal = /^https?:\/\//.test(item.url);
        if (isExternal) {
            a.target = "_blank";
            a.rel = "noopener noreferrer";
        }

        li.appendChild(a);
        ul.appendChild(li);
    });
}

populateList("list", list);
populateList("list1", list1);
populateList("list2", list2);
populateList("list3", list3);

document.getElementById("year").textContent = new Date().getFullYear();

document.getElementById("scrollTopBtn").addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
});

const rallyContent = [
    { number: '01', title: 'Receive', description: 'Take the serve and keep the rally alive.' },
    { number: '02', title: 'Set', description: 'Shape the ball into the perfect window for your striker.' },
    { number: '03', title: 'Strike', description: 'Finish the point with speed, shape, and a fearless kick.' }
];
const rallySteps = document.querySelectorAll('.rally-step');
const stepNumber = document.getElementById('step-number');
const stepTitle = document.getElementById('step-title');
const stepDescription = document.getElementById('step-description');

rallySteps.forEach(step => step.addEventListener('click', () => {
    const content = rallyContent[Number(step.dataset.step)];
    rallySteps.forEach(item => {
        item.classList.toggle('is-active', item === step);
        item.setAttribute('aria-selected', item === step ? 'true' : 'false');
    });
    stepNumber.textContent = content.number;
    stepTitle.textContent = content.title;
    stepDescription.textContent = content.description;
}));

const ruleContent = {
    scoring: ['01', 'Every rally counts.', 'Rally point scoring means someone scores on every play. A set goes to 21 points, but you must win by two. At 20–20, the set continues until one side leads by two, capped at 25.'],
    faults: ['02', 'Keep it off the net.', 'A fault happens when the ball lands outside the lines, touches the net, or a player uses an arm or hand. Each fault gives the other side a point.'],
    roles: ['03', 'Three players, one rhythm.', 'The tekong serves from the back. The feeder creates the opening. The striker attacks. The best teams make those three roles feel like one moving idea.']
};
const rulePanel = document.getElementById('rule-panel');
document.querySelectorAll('.rule-tab').forEach(tab => tab.addEventListener('click', () => {
    const [index, title, copy] = ruleContent[tab.dataset.rule];
    document.querySelectorAll('.rule-tab').forEach(item => {
        item.classList.toggle('is-active', item === tab);
        item.setAttribute('aria-selected', item === tab ? 'true' : 'false');
    });
    rulePanel.innerHTML = `<span class="rule-index">${index}</span><h3>${title}</h3><p>${copy}</p>`;
}));

const eventContent = {
    quad: { number: '01', name: 'Quad', description: 'Four players share the court. One or more players can attack as strikers while the remaining players feed and build the rally.', roles: ['1+ strikers', 'feeders', 'fast rotations'], players: 4 },
    doubles: { number: '02', name: 'Doubles', description: 'Two players cover the full partnership: one feeder creates the opening and one striker turns it into pressure.', roles: ['1 feeder', '1 striker', 'tight teamwork'], players: 2 },
    regu: { number: '03', name: 'Regu', description: 'The classic three-player formation: The tekong serves by staying inside the center circle while the other players position themselves inside the semi-circle, a feeder sets the ball, and a striker attacks.', roles: ['tekong', 'feeder', 'striker'], players: 3 }
};
const eventNumber = document.getElementById('event-number');
const eventName = document.getElementById('event-name');
const eventDescription = document.getElementById('event-description');
const eventRoles = document.getElementById('event-roles');
const playerDots = document.getElementById('player-dots');
document.querySelectorAll('.event-card').forEach(card => card.addEventListener('click', () => {
    const event = eventContent[card.dataset.event];
    document.querySelectorAll('.event-card').forEach(item => {
        item.classList.toggle('is-active', item === card);
        item.setAttribute('aria-selected', item === card ? 'true' : 'false');
    });
    eventNumber.textContent = event.number;
    eventName.textContent = event.name;
    eventDescription.textContent = event.description;
    eventRoles.innerHTML = event.roles.map(role => `<span>${role}</span>`).join('');
    playerDots.setAttribute('aria-label', `${event.players} players`);
    playerDots.innerHTML = '<i></i>'.repeat(event.players);
}));

document.querySelectorAll('.quiz-options button').forEach(option => option.addEventListener('click', () => {
    const feedback = document.querySelector('.quiz-feedback');
    document.querySelectorAll('.quiz-options button').forEach(item => item.classList.remove('is-selected'));
    option.classList.add('is-selected');
    feedback.textContent = option.dataset.answer === 'correct' ? 'Correct. The hands stay out of the game.' : 'Almost. Players can use their head, chest, thigh, and feet.';
    feedback.style.color = option.dataset.answer === 'correct' ? 'var(--teal)' : 'var(--coral)';
}));
