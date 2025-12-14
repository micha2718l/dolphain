import matplotlib.pyplot as plt
import numpy as np
import os

# Brand Colors from style.css
COLORS = {
    "deep": "#0a1828",
    "mid": "#178ca4",
    "light": "#3ab0c8",
    "cyan": "#00d4ff",
    "foam": "#e8f4f8",
    "coral": "#ff6b6b",
}

OUTPUT_DIR = "outputs/social_assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def setup_plot():
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
    ax.set_facecolor(COLORS["deep"])
    fig.patch.set_facecolor(COLORS["deep"])
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis("off")
    return fig, ax


def save_plot(fig, name):
    path = os.path.join(OUTPUT_DIR, f"{name}.png")
    plt.savefig(path, bbox_inches="tight", pad_inches=0, facecolor=COLORS["deep"])
    print(f"Saved {path}")
    plt.close(fig)


def generate_chirp_wave():
    """A stylized chirp signal representing a dolphin whistle"""
    fig, ax = setup_plot()

    t = np.linspace(-np.pi, np.pi, 1000)

    # Create a wave packet
    envelope = np.exp(-(t**2) * 2)

    # Multiple lines for "glowing" effect
    lines = [
        (0.0, COLORS["cyan"], 3.0, 1.0),
        (0.05, COLORS["mid"], 2.0, 0.6),
        (-0.05, COLORS["mid"], 2.0, 0.6),
        (0.1, COLORS["deep"], 1.0, 0.3),  # Shadow
    ]

    for offset, color, lw, alpha in lines:
        # Chirp frequency increases with time
        carrier = np.sin(10 * t + 2 * t**2)
        y = envelope * carrier * 0.6 + offset
        x = t / np.pi
        ax.plot(x, y, color=color, linewidth=lw, alpha=alpha)

    # Add some "bubbles" or data points
    num_dots = 20
    dot_x = np.random.uniform(-0.8, 0.8, num_dots)
    dot_y = np.random.uniform(-0.8, 0.8, num_dots)
    sizes = np.random.uniform(10, 50, num_dots)
    alphas = np.random.uniform(0.2, 0.8, num_dots)

    ax.scatter(dot_x, dot_y, s=sizes, c=COLORS["foam"], alpha=alphas, edgecolors="none")

    save_plot(fig, "profile_chirp_wave")


def generate_fin_spectrogram():
    """A dolphin fin shape made of spectrogram-like lines"""
    fig, ax = setup_plot()

    # Draw horizontal lines of varying length to form a fin shape
    y_levels = np.linspace(-0.6, 0.6, 40)

    for i, y in enumerate(y_levels):
        # Normalized height 0 to 1
        h = (y + 0.6) / 1.2

        # Fin shape math approximation
        # Base width is wide, tapers to top
        # Curves backward

        curve_back = 0.3 * (h**2)  # Curve to the right as we go up
        width = 0.6 * (1 - h) * (1 + 0.5 * h)  # Taper

        x_center = curve_back - 0.2
        x_start = x_center - width / 2
        x_end = x_center + width / 2

        # Draw a "signal" on this line
        x_points = np.linspace(x_start, x_end, 100)

        # Frequency increases with height (spectrogram style)
        freq = 10 + 40 * h
        signal = 0.02 * np.sin(freq * x_points * 2 * np.pi)

        # Color gradient from bottom (deep) to top (cyan)
        if h > 0.5:
            c = COLORS["cyan"]
        else:
            c = COLORS["mid"]

        ax.plot(
            x_points, np.full_like(x_points, y) + signal, color=c, lw=1.5, alpha=0.8
        )

    save_plot(fig, "profile_fin_spectrogram")


def generate_fin_spectrogram_v2():
    """A dolphin fin shape with rich colors and hidden interference patterns"""
    fig, ax = setup_plot()

    # Higher density
    y_levels = np.linspace(-0.65, 0.65, 70)

    import matplotlib.colors as mcolors

    # Custom ocean gradient
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "ocean_rich", [COLORS["deep"], COLORS["mid"], COLORS["cyan"], COLORS["foam"]]
    )

    for i, y in enumerate(y_levels):
        h = (y + 0.65) / 1.3

        # Fin shape
        curve_back = 0.3 * (h**2)
        width = 0.6 * (1 - h) * (1 + 0.5 * h)
        x_center = curve_back - 0.2
        x_start = x_center - width / 2
        x_end = x_center + width / 2

        x_points = np.linspace(x_start, x_end, 300)

        # Base carrier frequency
        freq = 20 + 60 * h

        # Hidden Pattern: A "pulse" ring at the center
        r = np.sqrt((x_points - 0.0) ** 2 + (y - 0.0) ** 2)
        pulse = np.exp(-10 * (r - 0.3) ** 2)  # Ring at r=0.3

        # Combine
        # Phase modulation by the pulse creates a distortion in the waves
        signal = 0.015 * np.sin(freq * x_points * 2 * np.pi + 5 * pulse)

        # Plot base line
        base_color = cmap(h)
        ax.plot(
            x_points,
            np.full_like(x_points, y) + signal,
            color=base_color,
            lw=1.2,
            alpha=0.8,
        )

        # Overlay highlights where the pulse is strong
        mask = pulse > 0.5
        if np.any(mask):
            # Use coral for the "hidden" ring
            ax.plot(
                x_points[mask],
                np.full_like(x_points[mask], y) + signal[mask],
                color=COLORS["coral"],
                lw=1.5,
                alpha=0.8,
            )

    save_plot(fig, "profile_fin_spectrogram_v2")


def generate_chirp_spiral():
    """A spiral chirp signal"""
    fig, ax = setup_plot()

    theta = np.linspace(0, 8 * np.pi, 1000)
    r = np.linspace(0.1, 0.9, 1000)

    # Modulate radius with a chirp
    chirp = 0.1 * np.sin(10 * theta) * (r**2)

    x = (r + chirp) * np.cos(theta)
    y = (r + chirp) * np.sin(theta)

    # Glow effect
    ax.plot(x, y, color=COLORS["cyan"], lw=4, alpha=0.3)
    ax.plot(x, y, color=COLORS["light"], lw=2, alpha=0.8)
    ax.plot(x, y, color=COLORS["foam"], lw=0.5, alpha=1.0)

    save_plot(fig, "profile_chirp_spiral")


def generate_chirp_pod():
    """Multiple overlapping chirps representing a pod"""
    fig, ax = setup_plot()

    t = np.linspace(-np.pi, np.pi, 1000)
    envelope = np.exp(-(t**2) * 2)

    offsets = [0.2, 0.0, -0.2]
    colors = [COLORS["light"], COLORS["cyan"], COLORS["mid"]]
    freqs = [8, 10, 12]

    for i, offset in enumerate(offsets):
        carrier = np.sin(freqs[i] * t + 2 * t**2)
        y = envelope * carrier * 0.5 + offset
        x = t / np.pi

        ax.plot(x, y, color=colors[i], lw=2, alpha=0.8)

        # Add some "sparkles" on peaks
        peaks = np.where((y[1:-1] > y[:-2]) & (y[1:-1] > y[2:]))[0] + 1
        if len(peaks) > 0:
            # Pick random peaks
            selected = np.random.choice(peaks, 3)
            ax.scatter(
                x[selected],
                y[selected],
                color=COLORS["foam"],
                s=20,
                alpha=0.9,
                zorder=10,
            )

    save_plot(fig, "profile_chirp_pod")


def generate_fin_dots():
    """A dolphin fin shape made of data points"""
    fig, ax = setup_plot()

    num_points = 2000

    # Rejection sampling for fin shape
    points_x = []
    points_y = []

    while len(points_x) < num_points:
        x = np.random.uniform(-0.6, 0.6)
        y = np.random.uniform(-0.6, 0.6)

        # Normalized height 0 to 1
        h = (y + 0.6) / 1.2

        if 0 <= h <= 1:
            curve_back = 0.3 * (h**2)
            width = 0.6 * (1 - h) * (1 + 0.5 * h)
            x_center = curve_back - 0.2

            if abs(x - x_center) < width / 2:
                points_x.append(x)
                points_y.append(y)

    # Color based on height
    colors = []
    sizes = []
    for y in points_y:
        h = (y + 0.6) / 1.2
        if h > 0.7:
            colors.append(COLORS["cyan"])
            sizes.append(4)
        elif h > 0.4:
            colors.append(COLORS["light"])
            sizes.append(3)
        else:
            colors.append(COLORS["mid"])
            sizes.append(2)

    ax.scatter(points_x, points_y, c=colors, s=sizes, alpha=0.8, edgecolors="none")

    # Add a "eye" or highlight
    ax.scatter([0.1], [0.1], c=COLORS["foam"], s=50, alpha=1.0, marker="+")

    save_plot(fig, "profile_fin_dots")


def generate_fin_neon():
    """A neon outline fin"""
    fig, ax = setup_plot()

    y = np.linspace(-0.6, 0.6, 200)
    h = (y + 0.6) / 1.2

    curve_back = 0.3 * (h**2)
    width = 0.6 * (1 - h) * (1 + 0.5 * h)
    x_center = curve_back - 0.2

    x_left = x_center - width / 2
    x_right = x_center + width / 2

    # Draw outline
    ax.plot(x_left, y, color=COLORS["cyan"], lw=3, alpha=0.8)
    ax.plot(x_right, y, color=COLORS["cyan"], lw=3, alpha=0.8)

    # Close top
    ax.plot(
        [x_left[-1], x_right[-1]], [y[-1], y[-1]], color=COLORS["cyan"], lw=3, alpha=0.8
    )
    # Close bottom
    ax.plot(
        [x_left[0], x_right[0]], [y[0], y[0]], color=COLORS["cyan"], lw=3, alpha=0.8
    )

    # Fill with faint grid
    for i in range(0, 200, 10):
        ax.plot(
            [x_left[i], x_right[i]], [y[i], y[i]], color=COLORS["mid"], lw=1, alpha=0.3
        )

    save_plot(fig, "profile_fin_neon")


def generate_minimal_logo():
    """A minimal geometric logo"""
    fig, ax = setup_plot()

    # Draw a circle representing the "lens" or "scope"
    circle = plt.Circle((0, 0), 0.8, color=COLORS["mid"], fill=False, lw=2, alpha=0.5)
    ax.add_artist(circle)

    # Draw a stylized "D" that looks like a wave
    t = np.linspace(0, 1, 100)

    # Vertical bar of D (curved slightly)
    x_bar = -0.2 + 0.05 * np.sin(np.pi * t)
    y_bar = -0.4 + 0.8 * t
    ax.plot(x_bar, y_bar, color=COLORS["cyan"], lw=8, solid_capstyle="round")

    # Curve of D
    theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
    r = 0.4
    x_curve = -0.2 + r * np.cos(theta) * 1.5
    y_curve = r * np.sin(theta)

    # Make the curve a wave
    wave_offset = 0.05 * np.sin(20 * theta)

    ax.plot(
        x_curve + wave_offset,
        y_curve,
        color=COLORS["cyan"],
        lw=6,
        solid_capstyle="round",
    )

    # Add a "spark" or data point
    ax.scatter([0.1], [0.1], s=200, c=COLORS["foam"], zorder=10)

    save_plot(fig, "profile_minimal_d")


if __name__ == "__main__":
    print("Generating profile pictures...")
    generate_fin_spectrogram_v2()
    print("Done!")
