// ✅ Disable automatic scroll restoration (most important)
if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual';
}
// ✅ Force scroll to top before leaving or reloading the page
window.addEventListener('beforeunload', () => {
    window.scrollTo(0, 0);
});

// Animation constants
const BALL_ROTATION_DEGREES = 720;
const BALL_ROTATION_DURATION = 2;
const BALL_SCALE = 0.6;
const BALL_MOVE_DURATION = 1.5;
const BALL_TOP_OFFSET = 50;
const TEXT_FADE_DURATION = 1.5;
const TEXT_FADE_DELAY = 0.3;
const TEXT_SLIDE_DISTANCE = 300;
const TEXT_SLIDE_DURATION = 2;

// Elements
const ball = document.getElementById('ball');
const introWrapper = document.getElementById('intro-wrapper');
const sideImage = document.getElementById('side-image');
const platform = document.getElementById('platforms');

const textCurrent = document.getElementById('text-current');
const textNext = document.getElementById('text-next');
const textNext1 = document.getElementById('text-next-1');

// Lock scroll initially
document.documentElement.style.overflowY = 'hidden';
document.body.style.overflowY = 'hidden';

// Timeline for intro animation
const tl = gsap.timeline({
    onComplete: () => {
        // Unlock scroll after animation
        document.documentElement.style.overflowY = 'auto';
        document.body.style.overflowY = 'auto';
        setupScrollAnimations();
    }
});

tl.to(ball, {
    rotation: BALL_ROTATION_DEGREES,
    duration: BALL_ROTATION_DURATION,
    ease: "power1.inOut"
});

tl.add(() => {
    const rect = ball.getBoundingClientRect();
    const vw = window.innerWidth;
    const targetX = (vw / 2) - (rect.left + rect.width / 2);
    const targetY = BALL_TOP_OFFSET - (rect.top + rect.height / 2);

    ball.style.position = "fixed";
    ball.style.margin = 0;
    ball.style.zIndex = 1000;

    gsap.to(ball, {
        duration: BALL_MOVE_DURATION,
        ease: "power2.inOut",
        scale: BALL_SCALE,
        x: targetX,
        y: targetY
    });
}, ">");

tl.to(introWrapper, {
    opacity: 1,
    duration: TEXT_FADE_DURATION,
    delay: TEXT_FADE_DELAY,
    ease: "power1.inOut"
});

tl.to(introWrapper, {
    x: TEXT_SLIDE_DISTANCE,
    duration: TEXT_SLIDE_DURATION,
    ease: "power2.inOut",
    onStart: () => {
        sideImage.style.visibility = "hidden";
    },
    onUpdate: function () {
        sideImage.style.visibility = "visible";
        sideImage.style.opacity = this.progress();
    }
});

// Setup scroll controlled animations for Scene 2
function setupScrollAnimations() {
    gsap.registerPlugin(ScrollTrigger);

    gsap.to(sideImage, {
        opacity: 1,
        ease: "none",
        scrollTrigger: {
            trigger: '#container',
            start: 'top top',
            end: '+=300',
            scrub: true
        }
    });

    gsap.to(textCurrent, {
        yPercent: -100,
        opacity: 0,
        ease: "none",
        scrollTrigger: {
            trigger: '#container',
            start: 'top top',
            end: '+=300',
            scrub: true
        }
    });

    gsap.to(textNext, {
        yPercent: -100,
        opacity: 1,
        ease: "none",
        scrollTrigger: {
            trigger: '#container',
            start: 'top top',
            end: '+=300',
            scrub: true
        }
    });
}

// Select all deviceLayout divs and SVG icons
const devices = document.querySelectorAll('.deviceLayout');
const svgs = document.querySelectorAll('.psvg');

// Track currently selected device
let selectedDevice = null;

function setSelected(deviceName) {
    // Remove 'enlarge' from all SVGs
    svgs.forEach(svg => svg.classList.remove('enlarge'));
    selectedDevice = null;

    // Add 'enlarge' to the SVG matching the selected device
    svgs.forEach(svg => {
        if (deviceName === 'Monitor' && svg.id === 'svg-browser') {
            svg.classList.add('enlarge');
            selectedDevice = deviceName;
        }
        else if ((deviceName === 'Mobile' || deviceName === 'Tab') &&
            (svg.id === 'svg-android' || svg.id === 'svg-ios')) {
            svg.classList.add('enlarge');
            selectedDevice = deviceName;
        }
    });
}

devices.forEach(device => {
    device.addEventListener('mouseenter', () => {
        const deviceName = device.dataset.device;
        setSelected(deviceName);
    });
    device.addEventListener('mouseleave', () => {
        setSelected(null);
    });
});

const scrollZone = document.getElementById('scrollZone');

window.addEventListener('scroll', () => {
    const zoneTop = scrollZone.offsetTop;
    const zoneHeight = scrollZone.offsetHeight;
    const scrollY = window.scrollY;

    const startScroll = zoneTop;
    const endScroll = zoneTop + zoneHeight - window.innerHeight;

    if (scrollY >= startScroll && scrollY <= endScroll) {
        sideImage.style.position = 'fixed';
        sideImage.style.top = '50%';
        sideImage.style.transform = 'translateY(-50%)';

        introWrapper.style.position = 'fixed';
        introWrapper.style.top = '';

        platform.style.position = 'fixed';
        platform.style.bottom = '0%';
        platform.style.top = '';
    } else if (scrollY > endScroll) {
        sideImage.style.position = 'absolute';
        sideImage.style.top = (zoneHeight - window.innerHeight / 2) + 'px';
        sideImage.style.transform = 'translateY(-50%)';

        introWrapper.style.position = 'absolute';
        introWrapper.style.top = (zoneHeight - window.innerHeight / 2) + 'px';

        platform.style.position = 'absolute';
        platform.style.top = (zoneHeight - 100) + 'px';
    } else {
        sideImage.style.position = 'fixed';
        sideImage.style.top = '50%';
        sideImage.style.transform = 'translateY(-50%)';

        introWrapper.style.position = 'fixed';
        introWrapper.style.top = '';

        platform.style.position = 'fixed';
        platform.style.bottom = '0%';
        platform.style.top = '';
    }
});

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
