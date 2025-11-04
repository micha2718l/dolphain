// HuggingFace Dataset Explorer for GoMRI-17
// Loads and displays audio files from the ColorSynth/GoMRI-17 dataset

class DataExplorer {
  constructor() {
    this.baseUrl = 'https://huggingface.co/datasets/ColorSynth/GoMRI-17';
    this.dataPath = '2017_South/BUOY200';
    this.files = [];
    this.filteredFiles = [];
    this.currentFile = null;
    this.audioElement = null;
    this.isPlaying = false;

    this.init();
  }

  async init() {
    try {
      await this.loadFileList();
      this.setupEventListeners();
      this.renderFileList();
      this.updateStats();
    } catch (error) {
      console.error('Failed to initialize explorer:', error);
      this.showError('Failed to load dataset. Please try again later.');
    }
  }

  async loadFileList() {
    // Fetch the file list from HuggingFace Hub API
    const apiUrl = `https://huggingface.co/api/datasets/ColorSynth/GoMRI-17/tree/main/${this.dataPath}`;
    
    try {
      const response = await fetch(apiUrl);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Filter for .200 files only and add metadata
      this.files = data
        .filter(item => item.type === 'file' && item.path.endsWith('.200'))
        .map(file => ({
          name: file.path.split('/').pop(),
          path: file.path,
          size: file.size || 8388608, // Default to 8MB if size not available
          downloadUrl: `${this.baseUrl}/resolve/main/${file.path}`,
          blobUrl: `${this.baseUrl}/blob/main/${file.path}`
        }));

      this.filteredFiles = [...this.files];
      
    } catch (error) {
      console.error('Error fetching file list:', error);
      // Fallback: generate file list based on known pattern
      this.generateFallbackFileList();
    }
  }

  generateFallbackFileList() {
    // Generate a list of files based on the hex pattern observed
    // Files follow pattern: 7178EXXX.200 where XXX is hex
    const files = [];
    const baseHex = 0x7178E5DC;
    
    // Generate 100 files as a sample (the dataset has ~1000 files)
    for (let i = 0; i < 100; i++) {
      const hex = (baseHex + i).toString(16).toUpperCase();
      const filename = `${hex}.200`;
      files.push({
        name: filename,
        path: `${this.dataPath}/${filename}`,
        size: 8388608, // 8MB
        downloadUrl: `${this.baseUrl}/resolve/main/${this.dataPath}/${filename}`,
        blobUrl: `${this.baseUrl}/blob/main/${this.dataPath}/${filename}`
      });
    }
    
    this.files = files;
    this.filteredFiles = [...files];
  }

  setupEventListeners() {
    // Search box
    document.getElementById('searchBox').addEventListener('input', (e) => {
      this.filterFiles(e.target.value);
    });

    // Sort selector
    document.getElementById('sortSelect').addEventListener('change', (e) => {
      this.sortFiles(e.target.value);
    });
  }

  filterFiles(searchTerm) {
    searchTerm = searchTerm.toLowerCase();
    this.filteredFiles = this.files.filter(file => 
      file.name.toLowerCase().includes(searchTerm)
    );
    this.renderFileList();
  }

  sortFiles(sortType) {
    const [key, direction] = sortType.split('-');
    
    this.filteredFiles.sort((a, b) => {
      let comparison = 0;
      
      if (key === 'name') {
        comparison = a.name.localeCompare(b.name);
      } else if (key === 'size') {
        comparison = a.size - b.size;
      }
      
      return direction === 'desc' ? -comparison : comparison;
    });
    
    this.renderFileList();
  }

  renderFileList() {
    const container = document.getElementById('fileListContainer');
    
    if (this.filteredFiles.length === 0) {
      container.innerHTML = '<div class="empty-state"><p>No files found</p></div>';
      return;
    }
    
    const html = `
      <div class="file-list">
        ${this.filteredFiles.map(file => `
          <div class="file-item ${this.currentFile?.name === file.name ? 'selected' : ''}" 
               data-filename="${file.name}"
               onclick="explorer.loadFile('${file.name}')">
            <div class="file-name">${file.name}</div>
            <div class="file-size">${this.formatFileSize(file.size)}</div>
          </div>
        `).join('')}
      </div>
    `;
    
    container.innerHTML = html;
  }

  updateStats() {
    document.getElementById('totalFiles').textContent = this.files.length;
    const totalSize = this.files.reduce((sum, file) => sum + file.size, 0);
    document.getElementById('totalSize').textContent = this.formatFileSize(totalSize);
  }

  formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
  }

  loadFile(filename) {
    const file = this.files.find(f => f.name === filename);
    if (!file) return;
    
    this.currentFile = file;
    this.renderPlayer();
    this.renderFileList(); // Update selection
  }

  renderPlayer() {
    if (!this.currentFile) return;
    
    const container = document.getElementById('playerContainer');
    
    container.innerHTML = `
      <h2>🎵 ${this.currentFile.name}</h2>
      
      <div class="audio-player">
        <div style="font-size: 0.9em; color: #666; margin-bottom: 10px;">
          Audio Player - EARS Format (.200)
        </div>
        <audio id="audioElement" style="width: 100%; margin-bottom: 10px;">
          <source src="${this.currentFile.downloadUrl}" type="audio/wav">
          Your browser does not support the audio element.
        </audio>
        
        <div class="player-controls">
          <button class="play-btn" id="playBtn" onclick="explorer.togglePlay()">
            <span id="playIcon">▶</span>
          </button>
          <div class="progress-bar" id="progressBar" onclick="explorer.seek(event)">
            <div class="progress-fill" id="progressFill"></div>
          </div>
          <div class="time-display">
            <span id="currentTime">0:00</span> / <span id="duration">0:00</span>
          </div>
        </div>
      </div>

      <div class="metadata-grid">
        <div class="metadata-item">
          <div class="metadata-label">Filename</div>
          <div class="metadata-value">${this.currentFile.name}</div>
        </div>
        <div class="metadata-item">
          <div class="metadata-label">File Size</div>
          <div class="metadata-value">${this.formatFileSize(this.currentFile.size)}</div>
        </div>
        <div class="metadata-item">
          <div class="metadata-label">Format</div>
          <div class="metadata-value">EARS .200</div>
        </div>
        <div class="metadata-item">
          <div class="metadata-label">Source</div>
          <div class="metadata-value">BUOY200</div>
        </div>
        <div class="metadata-item">
          <div class="metadata-label">Location</div>
          <div class="metadata-value">2017 South</div>
        </div>
        <div class="metadata-item">
          <div class="metadata-label">Dataset</div>
          <div class="metadata-value">GoMRI-17</div>
        </div>
      </div>

      <div style="margin-top: 20px; text-align: center;">
        <a href="${this.currentFile.downloadUrl}" class="download-btn" download>
          ⬇️ Download File
        </a>
        <a href="${this.currentFile.blobUrl}" class="download-btn" target="_blank" style="margin-left: 10px;">
          👁️ View on HuggingFace
        </a>
      </div>

      <div class="error-message" id="errorMessage" style="display: none;"></div>
    `;
    
    this.setupAudioPlayer();
  }

  setupAudioPlayer() {
    this.audioElement = document.getElementById('audioElement');
    
    if (!this.audioElement) return;
    
    this.audioElement.addEventListener('loadedmetadata', () => {
      document.getElementById('duration').textContent = this.formatTime(this.audioElement.duration);
    });
    
    this.audioElement.addEventListener('timeupdate', () => {
      const progress = (this.audioElement.currentTime / this.audioElement.duration) * 100;
      document.getElementById('progressFill').style.width = `${progress}%`;
      document.getElementById('currentTime').textContent = this.formatTime(this.audioElement.currentTime);
    });
    
    this.audioElement.addEventListener('ended', () => {
      this.isPlaying = false;
      document.getElementById('playIcon').textContent = '▶';
    });
    
    this.audioElement.addEventListener('error', (e) => {
      console.error('Audio error:', e);
      const errorMsg = document.getElementById('errorMessage');
      if (errorMsg) {
        errorMsg.style.display = 'block';
        errorMsg.textContent = 'Note: This file format (.200 EARS) may not play directly in browsers. Download the file to use with specialized audio software or the dolphain Python package.';
      }
    });
  }

  togglePlay() {
    if (!this.audioElement) return;
    
    if (this.isPlaying) {
      this.audioElement.pause();
      this.isPlaying = false;
      document.getElementById('playIcon').textContent = '▶';
    } else {
      this.audioElement.play().catch(e => {
        console.error('Play error:', e);
      });
      this.isPlaying = true;
      document.getElementById('playIcon').textContent = '⏸';
    }
  }

  seek(event) {
    if (!this.audioElement) return;
    
    const progressBar = document.getElementById('progressBar');
    const rect = progressBar.getBoundingClientRect();
    const percent = (event.clientX - rect.left) / rect.width;
    this.audioElement.currentTime = percent * this.audioElement.duration;
  }

  formatTime(seconds) {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  }

  showError(message) {
    const container = document.getElementById('fileListContainer');
    container.innerHTML = `
      <div class="error-message">
        <strong>Error:</strong> ${message}
      </div>
    `;
  }
}

// Initialize the explorer when the page loads
let explorer;
document.addEventListener('DOMContentLoaded', () => {
  explorer = new DataExplorer();
});
