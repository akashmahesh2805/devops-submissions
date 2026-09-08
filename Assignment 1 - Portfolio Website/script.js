const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');
const backToTop = document.querySelector('.back-to-top');
const sections = document.querySelectorAll('main section[id]');
const navigationLinks = document.querySelectorAll('.nav-links a');

menuToggle.addEventListener('click', () => {
  const isOpen = navLinks.classList.toggle('open');
  menuToggle.setAttribute('aria-expanded', String(isOpen));
  menuToggle.setAttribute('aria-label', isOpen ? 'Close navigation menu' : 'Open navigation menu');
});

navigationLinks.forEach((link) => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.setAttribute('aria-label', 'Open navigation menu');
  });
});

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll('.reveal').forEach((element) => revealObserver.observe(element));

const updateNavigation = () => {
  let currentSection = 'home';
  sections.forEach((section) => {
    if (window.scrollY >= section.offsetTop - 180) currentSection = section.id;
  });
  navigationLinks.forEach((link) => {
    link.classList.toggle('active', link.getAttribute('href') === `#${currentSection}`);
  });
  backToTop.classList.toggle('visible', window.scrollY > 600);
};

window.addEventListener('scroll', updateNavigation, { passive: true });
backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
updateNavigation();
