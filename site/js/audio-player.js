// AudioPlayer class - handles audio playback and scrubbing for a single file
class AudioPlayer {
    constructor(rank, fileData) {
        this.rank = rank;
        this.fileData = fileData;
        this.currentMode = 'denoised';
        this.audioElement = null;
        this.isPlaying = false;
        this.isSeeking = false;
        this.elements = {};
    }

    init() {
        // Create audio element
        this.audioElement = new Audio();
        this.audioElement.preload = 'metadata';
        this.audioElement.autoplay = false;
        
        // Error handling
        this.audioElement.addEventListener('error', (e) => {
            console.error(`Rank ${this.rank}: Audio error:`, this.audioElement.error);
        });
        
        this.setMode(this.currentMode);
        
        // Event listeners
        this.audioElement.addEventListener('loadedmetadata', () => this.onMetadataLoaded());
        this.audioElement.addEventListener('timeupdate', () => this.onTimeUpdate());
        this.audioElement.addEventListener('ended', () => this.onEnded());
        this.audioElement.addEventListener('play', () => {
            this.isPlaying = true;
        });
        this.audioElement.addEventListener('pause', () => {
            this.isPlaying = false;
        });
    }

    setMode(mode) {
        this.currentMode = mode;
        const audioSrc = mode === 'raw' ? this.fileData.audio_raw : this.fileData.audio_denoised;
        const specSrc = mode === 'raw' ? this.fileData.spectrogram_raw : this.fileData.spectrogram_denoised;
        const wavSrc = mode === 'raw' ? this.fileData.waveform_raw : this.fileData.waveform_denoised;
        
        const currentTime = this.audioElement ? this.audioElement.currentTime : 0;
        const wasPlaying = this.isPlaying;
        
        // Pause if playing
        if (this.audioElement && this.isPlaying) {
            this.audioElement.pause();
        }
        
        // Update audio source
        this.audioElement.src = `showcase/${audioSrc}`;
        
        // Update visualizations
        if (this.elements.spectrogram) {
            this.elements.spectrogram.src = `showcase/${specSrc}`;
            this.elements.waveform.src = `showcase/${wavSrc}`;
        }
        
        // Update tab styling
        const tabs = document.querySelectorAll(`#card-${this.rank} .audio-tab`);
        if (tabs.length > 0) {
            tabs.forEach(tab => {
                tab.classList.toggle('active', tab.dataset.mode === mode);
            });
        }
        
        // Load the new audio
        this.audioElement.load();
        
        // Wait for audio to be ready before restoring position
        if (currentTime > 0 || wasPlaying) {
            this.audioElement.addEventListener('canplay', () => {
                // Restore position if we had one
                if (currentTime > 0) {
                    this.audioElement.currentTime = currentTime;
                }
                // Resume playback if it was playing
                if (wasPlaying) {
                    this.audioElement.play().catch(e => console.log('Autoplay prevented:', e));
                }
            }, { once: true });
        }
    }

    togglePlay() {
        if (this.isPlaying) {
            this.audioElement.pause();
        } else {
            this.audioElement.play().catch(e => console.log('Play prevented:', e));
        }
    }

    seekTo(percent) {
        // Wait for duration to be available
        if (!this.audioElement.duration || isNaN(this.audioElement.duration) || this.audioElement.duration === 0) {
            this.audioElement.addEventListener('loadedmetadata', () => {
                this.seekTo(percent);
            }, { once: true });
            return;
        }
        
        const targetTime = percent * this.audioElement.duration;
        
        // Check if audio is seekable
        const isSeekable = this.audioElement.seekable.length > 0 && 
                          this.audioElement.seekable.end(0) > 0;
        
        if (!isSeekable) {
            // Audio not yet buffered - pause if playing and wait
            const wasPlaying = !this.audioElement.paused;
            if (wasPlaying) {
                this.audioElement.pause();
            }
            
            // Reload to ensure proper buffering
            this.audioElement.load();
            
            // Wait for audio to become seekable
            this.audioElement.addEventListener('canplay', () => {
                const nowSeekable = this.audioElement.seekable.length > 0 && 
                                   this.audioElement.seekable.end(0) > 0;
                
                if (nowSeekable) {
                    this.seekTo(percent);
                }
            }, { once: true });
            return;
        }
        
        // Audio is seekable - perform the seek
        this.targetSeekTime = targetTime;
        this.seekRetryCount = 0;
        this.audioElement.currentTime = targetTime;
        
        // Wait for seek to complete, then play
        const seekedHandler = () => {
            const actualTime = this.audioElement.currentTime;
            
            // Check if seek was successful (within 0.5s tolerance)
            if (Math.abs(actualTime - this.targetSeekTime) > 0.5) {
                this.seekRetryCount = (this.seekRetryCount || 0) + 1;
                
                if (this.seekRetryCount > 3) {
                    console.error(`Rank ${this.rank}: Seek failed after retries`);
                    // Give up and just play from wherever we are
                    if (!this.isPlaying) {
                        this.audioElement.play().catch(e => {});
                    }
                    return;
                }
                
                // Retry the seek
                this.audioElement.currentTime = this.targetSeekTime;
                this.audioElement.addEventListener('seeked', seekedHandler, { once: true });
                return;
            }
            
            // Seek successful - start playback if not already playing
            if (!this.isPlaying) {
                this.audioElement.play().catch(e => {});
            }
        };
        
        this.audioElement.addEventListener('seeked', seekedHandler, { once: true });
    }

    onMetadataLoaded() {
        this.elements.duration.textContent = this.formatTime(this.audioElement.duration);
    }

    onTimeUpdate() {
        const percent = (this.audioElement.currentTime / this.audioElement.duration) * 100;
        
        this.elements.timeline.style.width = `${percent}%`;
        this.elements.currentTime.textContent = this.formatTime(this.audioElement.currentTime);
        
        this.elements.specPlayback.style.left = `${percent}%`;
        this.elements.wavePlayback.style.left = `${percent}%`;
    }

    onEnded() {
        this.isPlaying = false;
        this.elements.playBtn.textContent = '▶';
    }

    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
}
