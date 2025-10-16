// Showcase initialization and UI management
const players = {};

function setupVizScrubbing(rank, type) {
  const container = document.getElementById(`${type}-${rank}`);
  const hoverLine = document.getElementById(`${type}-hover-${rank}`);

  container.addEventListener("mouseenter", () => {
    hoverLine.style.display = "block";
  });

  container.addEventListener("mousemove", (e) => {
    const rect = container.getBoundingClientRect();
    const percent = ((e.clientX - rect.left) / rect.width) * 100;
    hoverLine.style.left = `${percent}%`;
  });

  container.addEventListener("mouseleave", () => {
    hoverLine.style.display = "none";
  });

  container.addEventListener("click", (e) => {
    e.stopPropagation();
    e.preventDefault();
    const rect = container.getBoundingClientRect();
    const percent = (e.clientX - rect.left) / rect.width;
    players[rank].seekTo(percent);
  });
}

function handleTimelineClick(event, rank) {
  const timeline = event.currentTarget;
  const rect = timeline.getBoundingClientRect();
  const percent = (event.clientX - rect.left) / rect.width;
  players[rank].seekTo(percent);
}

// Load and display files
fetch("showcase/showcase_data.json")
  .then((r) => r.json())
  .then((data) => {
    const container = document.getElementById("files-container");

    // Populate stats
    const statsContainer = document.getElementById("showcase-stats");
    if (statsContainer && data.files.length > 0) {
      const totalChirps = data.files.reduce(
        (sum, f) => sum + (f.chirps || 0),
        0
      );
      const totalClicks = data.files.reduce(
        (sum, f) => sum + (f.clicks || 0),
        0
      );
      const avgScore = (
        data.files.reduce((sum, f) => sum + f.score, 0) / data.files.length
      ).toFixed(1);

      statsContainer.innerHTML = `
        <div class="stat-item">
          <span class="stat-number">${data.files.length}</span>
          <span class="stat-label">Recordings</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">${totalChirps}</span>
          <span class="stat-label">Total Chirps</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">${totalClicks}</span>
          <span class="stat-label">Total Clicks</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">${avgScore}</span>
          <span class="stat-label">Avg Score</span>
        </div>
      `;
    }

    data.files.forEach((file) => {
      const card = document.createElement("div");
      card.className = "file-card";
      card.id = `card-${file.rank}`;

      card.innerHTML = `
                <div class="file-header">
                    <div class="file-title">${file.filename}</div>
                    <div class="file-rank">Rank #${file.rank}</div>
                </div>
                
                <div class="file-metadata">
                    <div class="metadata-item">
                        <span class="metadata-label">Interestingness Score</span>
                        <span class="metadata-value highlight">${file.score.toFixed(
                          1
                        )}</span>
                    </div>
                    <div class="metadata-item">
                        <span class="metadata-label">Chirps Detected</span>
                        <span class="metadata-value">${file.chirps || 0}</span>
                    </div>
                    <div class="metadata-item">
                        <span class="metadata-label">Click Trains</span>
                        <span class="metadata-value">${
                          file.click_trains || 0
                        }</span>
                    </div>
                    <div class="metadata-item">
                        <span class="metadata-label">Total Clicks</span>
                        <span class="metadata-value">${file.clicks || 0}</span>
                    </div>
                </div>
                
                <div class="audio-tabs">
                    <div class="audio-tab active" data-mode="denoised" onclick="players[${
                      file.rank
                    }].setMode('denoised')">
                        ✨ Denoised
                    </div>
                    <div class="audio-tab" data-mode="raw" onclick="players[${
                      file.rank
                    }].setMode('raw')">
                        🎵 Raw
                    </div>
                </div>
                
                <div class="viz-container" id="spec-${file.rank}">
                    <img class="viz-image" src="showcase/${
                      file.spectrogram_denoised
                    }" alt="Spectrogram">
                    <div class="hover-line" id="spec-hover-${file.rank}"></div>
                    <div class="playback-line" id="spec-playback-${
                      file.rank
                    }"></div>
                </div>
                
                <div class="viz-container" id="wave-${file.rank}">
                    <img class="viz-image" src="showcase/${
                      file.waveform_denoised
                    }" alt="Waveform">
                    <div class="hover-line" id="wave-hover-${file.rank}"></div>
                    <div class="playback-line" id="wave-playback-${
                      file.rank
                    }"></div>
                </div>
                
                <div class="player-controls">
                    <button class="play-btn" id="play-${file.rank}">▶</button>
                    <span class="time" id="current-${file.rank}">0:00</span>
                    <div class="timeline" id="timeline-container-${
                      file.rank
                    }" onclick="handleTimelineClick(event, ${file.rank})">
                        <div class="timeline-progress" id="timeline-${
                          file.rank
                        }"></div>
                    </div>
                    <span class="time" id="duration-${file.rank}">0:00</span>
                </div>
                
                <div style="margin-top: 15px; display: flex; gap: 20px; flex-wrap: wrap;">
                    <div>🎺 Chirps: <strong>${
                      file.stats.chirp_count
                    }</strong></div>
                    <div>🔊 Clicks: <strong>${
                      file.stats.total_clicks
                    }</strong></div>
                    <div>⏱️ Duration: <strong>${file.stats.duration.toFixed(
                      1
                    )}s</strong></div>
                </div>
            `;

      container.appendChild(card);

      // Create player
      const player = new AudioPlayer(file.rank, file);
      players[file.rank] = player;

      // Store DOM element references
      player.elements = {
        playBtn: document.getElementById(`play-${file.rank}`),
        currentTime: document.getElementById(`current-${file.rank}`),
        duration: document.getElementById(`duration-${file.rank}`),
        timeline: document.getElementById(`timeline-${file.rank}`),
        spectrogram: card.querySelector(`#spec-${file.rank} img`),
        waveform: card.querySelector(`#wave-${file.rank} img`),
        specPlayback: document.getElementById(`spec-playback-${file.rank}`),
        wavePlayback: document.getElementById(`wave-playback-${file.rank}`),
        specHover: document.getElementById(`spec-hover-${file.rank}`),
        waveHover: document.getElementById(`wave-hover-${file.rank}`),
      };

      // Initialize player
      player.init();

      // Setup viz scrubbing
      setupVizScrubbing(file.rank, "spec");
      setupVizScrubbing(file.rank, "wave");

      // Add play button click handler with delay to prevent accidental clicks during page load
      let buttonClickEnabled = false;
      setTimeout(() => (buttonClickEnabled = true), 500);

      player.elements.playBtn.addEventListener("click", (e) => {
        if (!buttonClickEnabled) {
          e.stopPropagation();
          e.preventDefault();
          return;
        }
        player.togglePlay();
      });

      // Update play button on play/pause
      player.audioElement.addEventListener("play", () => {
        player.elements.playBtn.textContent = "⏸";
      });
      player.audioElement.addEventListener("pause", () => {
        player.elements.playBtn.textContent = "▶";
      });
    });
  })
  .catch((err) => {
    document.getElementById("files-container").innerHTML = `
            <div style="color: red; padding: 20px; text-align: center;">
                Error loading showcase data: ${err.message}
            </div>
        `;
  });
