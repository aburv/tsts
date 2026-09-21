
function toggleFaq(element) {
    const faqItem = element.closest('.faq-item');
    faqItem.classList.toggle('active');
}

const supportForm = document.getElementById('supportForm');
const formMessage = document.getElementById('formMessage');
const formStartedAt = Date.now();

supportForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const website = document.getElementById('website').value.trim();
    if (website || Date.now() - formStartedAt < 1500) {
        formMessage.textContent = 'Unable to submit this request. Please try again.';
        formMessage.className = 'form-message error';
        return;
    }

    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const category = document.getElementById('category').value;
    const device = document.getElementById('device').value;
    const subject = document.getElementById('subject').value.trim();
    const message = document.getElementById('message').value.trim();
    const formData = {
        name,
        email,
        category,
        device_type: device,
        subject,
        message,
        is_follow: document.getElementById('updates').checked,
        timestamp: new Date().toISOString(),
    };

    const submitBtn = supportForm.querySelector('.submit-btn');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending...';
    formMessage.className = 'form-message';

    try {
        const response = await fetch('/api/support', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });

        if (!response.ok) {
            throw new Error(`Support request failed: ${response.status}`);
        }

        formMessage.textContent = `Thank you. We've received your request and will respond to ${email}.`;
        formMessage.className = 'form-message success';
        supportForm.reset();
    } catch (error) {
        console.error('Form submission error:', error);
        formMessage.textContent = 'Unable to send your request right now. Please try again later.';
        formMessage.className = 'form-message error';
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
});

const toggleBtn = document.getElementById('theme-toggle');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

function setTheme(mode) {
    document.body.classList.remove('light', 'dark');
    document.body.classList.add(mode);
    toggleBtn.textContent = mode !== 'dark' ? '☀️' : '🌙';
    localStorage.setItem('theme', mode);
}

setTheme(prefersDark.matches ? 'dark' : 'light');

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
