# L-ZIP VS Code Extension

**Logic-based Zero-redundancy Information Prompting for VS Code**

Compress your AI prompts by 40-70% while preserving meaning. Save tokens, reduce costs, and get faster responses from AI models.

## 🎯 Features

### Status Bar Integration
- **L-ZIP Toggle** - Enable/disable MCP integration
- **L-ZIP Translator** - Translate prompts to L-ZIP format

### Smart Prompt Compression
- **Context-aware compression** - Removes filler words intelligently
- **Symbol replacements** - Converts verbose phrases to compact operators
- **Number abbreviations** - `5000` → `5k`, `1000000` → `1M`
- **Time compression** - `30 minutes` → `30m`, `2 hours` → `2h`
- **Tech term shortcuts** - `image` → `img`, `database` → `db`
- **Extended operators** - IMAGE, CODE, CONTENT specific tags

### Copy & Paste Ready
- Paste your prompt into the translator
- Get instant L-ZIP translation
- One-click copy of translated prompts
- Visual comparison of original vs translated
- Real-time token count and savings percentage
- Use the result directly in your AI of choice

## 📊 Example

**Original (644 tokens):**
```
Make a picture for me in high as possible quality, nice realistic looks, 
but still happy, kind, fantasy style please. Theme is a Weekend Magic Festival...
```

**L-ZIP (450 tokens - 30% saved):**
```
STYLE:Realistic MOOD:Happy LIGHTING:Sunny QUALITY:4K RATIO:16:9 
Make a picture in high quality, nice realistic looks, happy, kind, fantasy style. 
Theme is Weekend Magic Festival...
```

## 🚀 Installation

### Option 1: Install from VS Code Extensions (Recommended)
1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search for `L-ZIP`
4. Click **Install**
5. Restart VS Code

### Option 2: Install from File
1. Download the extension from the [GitHub repository](https://github.com/ezixen/L-ZIP)
2. Navigate to `vscode-extension/` folder
3. Package it:
   ```bash
   cd vscode-extension
   npx vsce package
   ```
4. In VS Code: `Ctrl+Shift+P` → "Extensions: Install from VSIX"
5. Select the `.vsix` file

### Option 3: Manual Installation (Development)
1. Clone the L-ZIP repository:
   ```bash
   git clone https://github.com/ezixen/L-ZIP.git
   cd L-ZIP/vscode-extension
   ```
2. Copy to VS Code extensions folder:
   - **Windows:** `%USERPROFILE%\.vscode\extensions\ezixen.lzip-vscode-0.0.1\`
   - **macOS:** `~/.vscode/extensions/ezixen.lzip-vscode-0.0.1/`
   - **Linux:** `~/.vscode/extensions/ezixen.lzip-vscode-0.0.1/`
3. Restart VS Code

## 🚀 Quick Start

1. Install the extension (see above)
2. Restart VS Code
3. Look for status bar buttons at the bottom right:
   - **✓ L-ZIP** - Toggle MCP enable/disable
   - **📋 L-ZIP Translator** - Open translator
4. Click **📋 L-ZIP Translator** to open
5. Paste your prompt in the input box
6. Copy the L-ZIP translation with one click
7. Paste into ChatGPT, Claude, Gemini, or any AI

## 📋 Requirements

- **Python 3.8+** installed and accessible
- **L-ZIP Python module** (automatically found in parent directory)

## ⚙️ Extension Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `lzip.pythonPath` | Python executable path | `"python"` |
| `lzip.translatorDefaultText` | Placeholder text for translator | `"Paste prompt here..."` |

## 🎨 Usage Tips

### For Image Generation
The extension auto-detects image-specific keywords:
- Detects quality: `4k`, `8k`, `high quality` → `QUALITY:4K`
- Detects style: `realistic`, `anime`, `oil painting` → `STYLE:Realistic`
- Detects mood: `happy`, `dark`, `cheerful` → `MOOD:Happy`
- Detects aspect ratios: `16:9`, `1:1` → `RATIO:16:9`

### For Code Requests
Removes politeness without losing meaning:
- ❌ Removes: `please`, `kindly`, `for me`, `if you can`
- ✅ Keeps: All technical requirements and constraints

### For Analysis Tasks
Compresses sequential steps:
- `and then` → `|`
- `as well as` → `+`
- `leads to` → `=>`

## 🔧 Development

### Debug the Extension
1. Open the `vscode-extension` folder in VS Code
2. Press `F5` to launch Extension Development Host
3. Test the status bar buttons in the new window
4. Changes auto-reload with the watch task

### Build from Source
```bash
cd vscode-extension
npm install  # If you add dependencies later
# No build step needed - pure JavaScript
```

### Project Structure
```
vscode-extension/
├── src/
│   └── extension.js       # Main extension code
├── .vscode/
│   ├── launch.json        # Debug configuration
│   └── tasks.json         # Build tasks
├── package.json           # Extension manifest
├── README.md              # This file
└── SMART_COMPRESSION.md   # Future ML enhancement plan
```

## 🐛 Troubleshooting

**Extension not activating:**
- Extension activates on startup (`onStartupFinished`)
- Check Output panel → "Extension Host" for errors

**Status bar buttons not showing:**
- Reload the Extension Development Host window (`Ctrl+R`)
- Check if other extensions are hiding the status bar

**Python module not found:**
- Extension looks for `lzip.py` in parent directory
- Ensure your workspace includes the parent L-ZIP folder
- Check Python path in settings: `lzip.pythonPath`

**Compression not working:**
- Verify Python is installed: `python --version`
- Check if `lzip.py` exists in parent folder
- See error details in the Estimator output panel

## 📝 Version History

### v0.0.1 (Current)
- ✅ Status bar MCP toggle
- ✅ Token estimator with copy button
- ✅ Context-aware compression (40-70% token reduction)
- ✅ Extended operators (IMAGE, CODE, CONTENT)
- ✅ Symbol replacements with word boundaries
- ✅ Number and time abbreviations
- ✅ Safe filler word removal

### Planned (v0.1.0)
- 🔄 ML-based context understanding (SmolLM-135M)
- 🔄 Custom compression rules per workspace
- 🔄 Batch processing multiple prompts
- 🔄 Direct language model API integration

## 📄 License

MIT License - See parent project LICENSE file

## 🤝 Contributing

This extension is part of the L-ZIP project by [ezixen](https://github.com/ezixen).

To contribute:
1. Review the main L-ZIP documentation in parent directory
2. Fork the repository
3. Make your changes
4. Test thoroughly with F5 debugging
5. Submit a pull request

## 🔗 Related

- [L-ZIP Main Project](../README.md)
- [L-ZIP Best Practices](../BEST_PRACTICES.md)
- [MCP Integration Guide](../MCP_INTEGRATION.md)

---

**Made with ❤️ by ezixen** | Reducing AI's carbon footprint, one token at a time.
