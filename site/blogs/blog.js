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
    setTheme(document.body.classList.contains('dark') ? 'light' : 'dark');
});
prefersDark.addEventListener('change', event => {
    if (!localStorage.getItem('theme')) setTheme(event.matches ? 'dark' : 'light');
});

const footerLists = {
    list: [
        { title: 'Go to app', url: 'https://www.takbuff.com' },
        { title: 'Sepak takraw', url: '../../about-game' }
    ],
    list1: [
        { title: 'GitHub Repo', url: 'https://github.com/aburv/tsts' },
        { title: 'Contribute', url: 'https://github.com/aburv/tsts/blob/main/CONTRIBUTING.md' },
        { title: 'Report a Bug', url: 'https://github.com/aburv/tsts/issues/new?template=bug_report.md' },
        { title: 'Request a Feature', url: 'https://github.com/aburv/tsts/issues/new?template=feature_request.md' },
        { title: 'Code of Conduct', url: 'https://github.com/aburv/tsts/blob/main/CODE_OF_CONDUCT.md' }
    ],
    list2: [
        { title: 'Newsletter', url: '../../newsletters' },
        { title: 'Blog', url: '../../blogs' },
        { title: 'FAQ', url: '../../faq' },
        { title: 'Support', url: '../../support' },
        { title: 'Contact', url: '../../contact' }
    ],
    list3: [
        { title: 'Privacy Policy', url: '../../privacy' },
        { title: 'Terms of Use', url: '../../terms' }
    ]
};

Object.entries(footerLists).forEach(([listId, items]) => {
    const list = document.getElementById(listId);
    items.forEach(item => {
        const link = document.createElement('a');
        link.href = item.url;
        link.textContent = item.title;
        if (/^https?:\/\//.test(item.url)) {
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
        }
        const itemElement = document.createElement('li');
        itemElement.appendChild(link);
        list.appendChild(itemElement);
    });
});

document.getElementById('year').textContent = new Date().getFullYear();
document.getElementById('scrollTopBtn').addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
