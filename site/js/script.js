// Dolphain Landing Page JavaScript
// Fun, interactive elements for the GitHub Pages site

// Mobile Navigation Toggle
function setupMobileNav() {
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');
  const navLinks = document.querySelectorAll('.nav-link');

  if (navToggle && navMenu) {
    // Toggle menu on button click
    navToggle.addEventListener('click', () => {
      navToggle.classList.toggle('active');
      navMenu.classList.toggle('active');
    });

    // Close menu when a link is clicked
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        navToggle.classList.remove('active');
        navMenu.classList.remove('active');
      });
    });

    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
      if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
        navToggle.classList.remove('active');
        navMenu.classList.remove('active');
      }
    });
  }
}

// Generate more bubbles dynamically
function createBubbles() {
  const bubbleCount = 15;
  for (let i = 0; i < bubbleCount; i++) {
    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.style.left = Math.random() * 100 + "%";
    bubble.style.width = Math.random() * 40 + 20 + "px";
    bubble.style.height = bubble.style.width;
    bubble.style.animationDuration = Math.random() * 8 + 6 + "s";
    bubble.style.animationDelay = Math.random() * 5 + "s";
    document.body.appendChild(bubble);
  }
}

// Smooth scrolling for anchor links
function setupSmoothScrolling() {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });
}

// Fun 42 click counter (Easter egg)
function setup42Counter() {
  let clickCount = 0;
  const fortyTwo = document.querySelector(".forty-two");

  if (fortyTwo) {
    fortyTwo.addEventListener("click", function () {
      clickCount++;

      // Visual feedback
      this.style.transform = "scale(1.3) rotate(360deg)";
      setTimeout(() => {
        this.style.transform = "";
      }, 300);

      if (clickCount === 42) {
        alert(
          "🐬 Congratulations! You've clicked 42 times.\n\nThe dolphins approve!\n\nYou may now consider yourself a hoopy frood who really knows where their towel is. 🐬"
        );
        clickCount = 0;

        // Add some extra celebration
        for (let i = 0; i < 42; i++) {
          setTimeout(() => createCelebrationBubble(), i * 50);
        }
      }
    });
  }
}

// Create celebration bubble
function createCelebrationBubble() {
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.style.left = Math.random() * 100 + "%";
  bubble.style.width = "60px";
  bubble.style.height = "60px";
  bubble.style.animationDuration = "3s";
  bubble.style.background = `rgba(${Math.random() * 255}, ${
    Math.random() * 255
  }, ${Math.random() * 255}, 0.3)`;
  document.body.appendChild(bubble);

  setTimeout(() => bubble.remove(), 3000);
}

// Log a fun message to console for developers
function logDeveloperMessage() {
  console.log(`
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   🐬  Welcome to Dolphain!  🐬                            ║
    ║                                                           ║
    ║   "So long, and thanks for all the fish data"            ║
    ║                                                           ║
    ║   Interested in the code? Check out:                     ║
    ║   https://github.com/micha2718l/dolphain                 ║
    ║                                                           ║
    ║   Easter egg hint: Try clicking the "42" button...       ║
    ║   (42 times, to be precise)                              ║
    ║                                                           ║
    ║   Don't Panic! 🚀                                         ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    `);
}

// Konami code easter egg (for fun)
function setupKonamiCode() {
  const konamiCode = [
    "ArrowUp",
    "ArrowUp",
    "ArrowDown",
    "ArrowDown",
    "ArrowLeft",
    "ArrowRight",
    "ArrowLeft",
    "ArrowRight",
    "b",
    "a",
  ];
  let konamiIndex = 0;

  document.addEventListener("keydown", (e) => {
    if (e.key === konamiCode[konamiIndex]) {
      konamiIndex++;
      if (konamiIndex === konamiCode.length) {
        activateKonamiMode();
        konamiIndex = 0;
      }
    } else {
      konamiIndex = 0;
    }
  });
}

function activateKonamiMode() {
  alert(
    "🐬🎮 KONAMI MODE ACTIVATED! 🎮🐬\n\nYou've unlocked: Extra Bubbles!\n\nThe dolphins are impressed with your gaming history."
  );

  // Create a bubble storm!
  for (let i = 0; i < 100; i++) {
    setTimeout(() => createCelebrationBubble(), i * 30);
  }
}

// Initialize everything when the page loads
document.addEventListener("DOMContentLoaded", function () {
  setupMobileNav();
  createBubbles();
  setupSmoothScrolling();
  setup42Counter();
  setupKonamiCode();
  logDeveloperMessage();
});

// Log message when leaving (for developers)
window.addEventListener("beforeunload", function () {
  console.log("🐬 Thanks for visiting Dolphain! Come back soon! 🐬");
});
