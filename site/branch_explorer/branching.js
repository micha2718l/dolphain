'use strict';

(function () {
  const TREE_SOURCE = 'branching_data.json';

  const detailPanel = document.getElementById('detail-panel');
  const detailTitle = document.querySelector('#detail-panel h2 span.title');
  const detailDescription = detailPanel.querySelector('.detail-description');
  const detailMeta = detailPanel.querySelector('.detail-meta');
  const detailStats = detailPanel.querySelector('.stats-grid');
  const detailAudio = detailPanel.querySelector('.audio-stack');
  const detailLinks = detailPanel.querySelector('.media-links');

  function renderError(message) {
    detailTitle.textContent = 'Data unavailable';
    detailDescription.textContent = message;
  }

  function formatNumber(value, decimals) {
    if (value === null || value === undefined || Number.isNaN(value)) {
      return '—';
    }
    if (typeof value !== 'number') {
      return value;
    }
    return value.toFixed(decimals ?? 0);
  }

  function createStatCard(label, value, decimals = 0) {
    const card = document.createElement('div');
    card.className = 'stat-card';

    const labelSpan = document.createElement('span');
    labelSpan.textContent = label;

    const valueStrong = document.createElement('strong');
    const formatted = formatNumber(value, decimals);
    valueStrong.textContent = typeof formatted === 'number' ? formatted : formatted;

    card.appendChild(labelSpan);
    card.appendChild(valueStrong);
    return card;
  }

  function updateDetails(d) {
    const data = d.data;

    detailTitle.textContent = data.name || 'Dolphin Branch Explorer';

    const description =
      data.description || (data.meta && data.meta.description) || 'Follow a branch to dive deeper into the pod.';
    detailDescription.textContent = description;

    detailMeta.innerHTML = '';
    const metaTags = [];

    if (data.meta && data.meta.emoji) {
      metaTags.push(`${data.meta.emoji} ${data.meta.label || ''}`.trim());
    }

    if (data.meta && typeof data.meta.count === 'number') {
      metaTags.push(`${data.meta.count} clips`);
    }

    if (data.type && data.type !== 'root') {
      metaTags.push(`${data.type.toUpperCase()} NODE`);
    }

    metaTags
      .filter(Boolean)
      .forEach((tag) => {
        const chip = document.createElement('div');
        chip.className = 'meta-chip';
        chip.textContent = tag;
        detailMeta.appendChild(chip);
      });

    detailStats.innerHTML = '';

    const statsEntries = [];

    if (data.meta) {
      const { avg_whistles_per_minute, avg_coverage_percent, avg_freq_span_khz, avg_whistle_count } = data.meta;
      if (avg_whistles_per_minute !== undefined) {
        statsEntries.push(['Avg whistles/min', avg_whistles_per_minute, 1]);
      }
      if (avg_freq_span_khz !== undefined) {
        statsEntries.push(['Avg range (kHz)', avg_freq_span_khz, 2]);
      }
      if (avg_coverage_percent !== undefined) {
        statsEntries.push(['Avg coverage %', avg_coverage_percent, 1]);
      }
      if (avg_whistle_count !== undefined) {
        statsEntries.push(['Avg whistle count', avg_whistle_count, 1]);
      }
    }

    if (data.stats) {
      const { whistles_per_minute, coverage, freq_range_khz, whistle_count, duration_s } = data.stats;
      statsEntries.push(['Whistles/min', whistles_per_minute, 1]);
      statsEntries.push(['Coverage %', coverage, 1]);
      statsEntries.push(['Freq span kHz', freq_range_khz, 2]);
      statsEntries.push(['Whistle count', whistle_count, 0]);
      statsEntries.push(['Duration (s)', duration_s, 1]);
    }

    const uniqueEntries = new Map();
    statsEntries.forEach(([label, value, decimals]) => {
      if (value === undefined || value === null) {
        return;
      }
      if (!uniqueEntries.has(label)) {
        uniqueEntries.set(label, [value, decimals]);
      }
    });

    for (const [label, [value, decimals]] of uniqueEntries.entries()) {
      detailStats.appendChild(createStatCard(label, value, decimals));
    }

    detailAudio.innerHTML = '';
    detailLinks.innerHTML = '';

    if (data.media && (data.media.audio_raw || data.media.audio_denoised)) {
      const intro = document.createElement('p');
      intro.className = 'detail-description';
      intro.textContent = 'Play the pod in real time:';
      detailAudio.appendChild(intro);
    }

    if (data.media && data.media.audio_raw) {
      const figureRaw = document.createElement('figure');
      const captionRaw = document.createElement('figcaption');
      captionRaw.textContent = 'Raw ocean mix';
      const audioRaw = document.createElement('audio');
      audioRaw.controls = true;
      audioRaw.src = data.media.audio_raw;
      audioRaw.preload = 'none';
      figureRaw.appendChild(captionRaw);
      figureRaw.appendChild(audioRaw);
      detailAudio.appendChild(figureRaw);
    }

    if (data.media && data.media.audio_denoised) {
      const figureClean = document.createElement('figure');
      const captionClean = document.createElement('figcaption');
      captionClean.textContent = 'Denoised spotlight';
      const audioClean = document.createElement('audio');
      audioClean.controls = true;
      audioClean.src = data.media.audio_denoised;
      audioClean.preload = 'none';
      figureClean.appendChild(captionClean);
      figureClean.appendChild(audioClean);
      detailAudio.appendChild(figureClean);
    }

    if (data.media && (data.media.spectrogram || data.media.waveform)) {
      if (data.media.spectrogram) {
        const link = document.createElement('a');
        link.className = 'media-link';
        link.href = data.media.spectrogram;
        link.target = '_blank';
        link.rel = 'noopener';
        link.textContent = 'Open spectrogram';
        detailLinks.appendChild(link);
      }

      if (data.media.waveform) {
        const link = document.createElement('a');
        link.className = 'media-link';
        link.href = data.media.waveform;
        link.target = '_blank';
        link.rel = 'noopener';
        link.textContent = 'Open waveform';
        detailLinks.appendChild(link);
      }
    }
  }

  function renderTree(data) {
    const width = 1000;
    const radius = width / 2;

    const root = d3
      .hierarchy(data)
      .sum((d) => (d.type === 'record' ? 1 : 0))
      .sort((a, b) => (a.data.meta?.avg_whistles_per_minute || 0) - (b.data.meta?.avg_whistles_per_minute || 0));

    const tree = d3.cluster().size([2 * Math.PI, radius - 140]);
    tree(root);

    const svg = d3
      .select('#branch-tree')
      .attr('viewBox', [-width / 2, -width / 2, width, width])
      .attr('role', 'presentation');

    const linkGenerator = d3.linkRadial().angle((d) => d.x).radius((d) => d.y);

    const links = svg
      .append('g')
      .selectAll('path')
      .data(root.links())
      .join('path')
      .attr('class', 'link')
      .attr('d', linkGenerator);

    const nodes = svg
      .append('g')
      .selectAll('g')
      .data(root.descendants())
      .join('g')
      .attr('class', (d) => `node ${d.data.type || 'root'}`)
      .attr('transform', (d) => `rotate(${(d.x * 180) / Math.PI - 90}) translate(${d.y},0)`)
      .on('click', function (event, d) {
        event.stopPropagation();
        focusNode(d);
      });

    nodes.append('circle').attr('r', 6);

    nodes
      .append('text')
      .attr('dy', '0.31em')
      .attr('x', (d) => (d.x < Math.PI ? 12 : -12))
      .attr('text-anchor', (d) => (d.x < Math.PI ? 'start' : 'end'))
      .attr('transform', (d) => (d.x >= Math.PI ? 'rotate(180)' : null))
      .text((d) => d.data.name);

    function focusNode(node) {
      const ancestors = new Set(node.ancestors());

      nodes.classed('active', (d) => ancestors.has(d));
      links.classed('active', (link) => ancestors.has(link.target));

      updateDetails(node);
    }

    // Focus root by default
    focusNode(root);

    // Allow clicking outside the tree to reset focus
    d3.select('#tree-container').on('click', () => {
      focusNode(root);
    });
  }

  async function init() {
    try {
      const response = await fetch(TREE_SOURCE, { cache: 'no-store' });
      if (!response.ok) {
        throw new Error(`Failed to load ${TREE_SOURCE} (${response.status})`);
      }
      const data = await response.json();
      renderTree(data);
    } catch (err) {
      console.error(err);
      renderError('Unable to load branching tree data. Run the generator script to create it.');
    }
  }

  document.addEventListener('DOMContentLoaded', init);
})();
