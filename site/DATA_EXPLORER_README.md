# Dolphin Data Explorer

An interactive web portal for browsing and exploring the GoMRI-17 dolphin acoustic dataset hosted on HuggingFace.

## Features

- **Browse Files**: Navigate through 1000+ audio files from the BUOY200 dataset
- **Search & Filter**: Find specific files quickly with real-time search
- **Audio Playback**: Listen to files directly in the browser (where supported)
- **Metadata Display**: View file information including size, format, and source
- **Download**: Direct download links to HuggingFace
- **No Installation Required**: Works entirely in the browser

## Dataset Information

- **Source**: [ColorSynth/GoMRI-17](https://huggingface.co/datasets/ColorSynth/GoMRI-17) on HuggingFace
- **Location**: 2017_South/BUOY200
- **Format**: EARS .200 files (8.39 MB each)
- **Total Size**: ~8.39 GB
- **File Count**: ~1000 files

## Usage

1. Open `data-explorer.html` in your web browser
2. Browse the file list on the left sidebar
3. Click any file to view its details and play it
4. Use the search box to find specific files
5. Sort files by name or size using the dropdown
6. Download files directly from HuggingFace

## Technical Details

### How It Works

The explorer uses the HuggingFace Hub API to:
1. Fetch the file tree from the dataset repository
2. Generate download URLs for each file
3. Stream audio directly from HuggingFace CDN
4. Provide metadata and file information

### Browser Compatibility

- **Modern Browsers**: Chrome, Firefox, Safari, Edge (latest versions)
- **Audio Playback**: EARS .200 format may have limited browser support
  - Files can be downloaded for use with specialized software
  - The dolphain Python package provides full support

### API Endpoints

```javascript
// File list API
https://huggingface.co/api/datasets/ColorSynth/GoMRI-17/tree/main/2017_South/BUOY200

// File download URL pattern
https://huggingface.co/datasets/ColorSynth/GoMRI-17/resolve/main/2017_South/BUOY200/[FILENAME].200
```

## Integration with Dolphain Site

To add the explorer to your site navigation:

1. Add link to `index.html`:
```html
<a href="data-explorer.html">📊 Data Explorer</a>
```

2. Ensure `js/data-explorer.js` is accessible

3. The explorer uses the existing `css/main.css` for base styling

## Future Enhancements

Potential improvements:
- [ ] Add waveform visualization for each file
- [ ] Implement spectrogram generation in-browser
- [ ] Add bulk download functionality
- [ ] Show processing status (chirps/clicks detected)
- [ ] Add map view showing buoy locations
- [ ] Integrate with dolphain Python API for analysis
- [ ] Add file comparison features
- [ ] Support for other buoys (BUOY210, etc.)

## File Format Notes

EARS `.200` files are a proprietary format used for underwater acoustic recordings. To fully utilize these files:

- Use the `ears_reader.py` module from this repository
- Convert to WAV using the dolphain package
- Process with the dolphain analysis pipeline

## License

Same as the dolphain project (see main README)

## Credits

- **Dataset**: ColorSynth/GoMRI-17
- **Hosting**: HuggingFace Datasets Hub
- **Platform**: Dolphain Project
