
// Footer data
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

        // Check if the link is external
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

// Set year dynamically
document.getElementById("year").textContent = new Date().getFullYear();

// Scroll to top button
document.getElementById("scrollTopBtn").addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
});
