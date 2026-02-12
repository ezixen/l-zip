# L-ZIP Browser Extension Installation

## Firefox Installation

### Method 1: Temporary (Testing)
1. Open Firefox
2. Type `about:debugging` in address bar
3. Click "This Firefox" in sidebar
4. Click "Load Temporary Add-on..."
5. Navigate to `d:\Dev\L-ZIP\browser-extension`
6. Select `manifest.json`
7. Extension active until Firefox restarts

### Method 2: Permanent (Unsigned)
1. Download: `d:\Dev\L-ZIP\L-ZIP-Firefox.xpi`
2. Type `about:config` in Firefox
3. Set `xpinstall.signatures.required` to `false`
4. Type `about:addons`
5. Click gear icon → "Install Add-on From File..."
6. Select `L-ZIP-Firefox.xpi`
7. Click "Add" when warned about verification

## Chrome Installation

### Method 1: Load Unpacked (Recommended for Development)
1. Open Chrome
2. Type `chrome://extensions/` in address bar
3. Enable "Developer mode" (top right toggle)
4. Click "Load unpacked"
5. Navigate to `d:\Dev\L-ZIP\browser-extension`
6. Select the folder
7. Extension installed and active

### Method 2: From ZIP (Alternative)
1. Download: `d:\Dev\L-ZIP\L-ZIP-Chrome.zip`
2. Extract to a permanent location (e.g., `C:\Extensions\L-ZIP`)
3. Follow Method 1 steps, but select the extracted folder

## Features

- **Auto-enabled on AI sites**: ChatGPT, Claude, Gemini, Copilot, Grok, GitHub Copilot, Meta AI
- **Manual toggle**: Click extension icon for other sites
- **Automatic compression**: Press Enter to auto-translate to L-ZIP
- **28% average compression**: Reduces token usage while preserving meaning

## Usage

1. Visit any AI website
2. Extension auto-enables on known AI sites (check icon)
3. Type your prompt in the input box
4. Press **Enter** (the extension auto-translates before sending)
5. For manual translation: Click extension icon → "Translate Current Input"

## Extension Icon

The green L-ZIP logo appears in your browser toolbar. Click it to:
- Toggle on/off for current tab
- Manually translate current input
- View status (auto-enabled on AI sites or manual toggle)

## Troubleshooting

**Firefox says "corrupt or invalid"**
- Use temporary loading via `about:debugging` instead
- Extension is unsigned (normal for development)

**Chrome won't load**
- Make sure "Developer mode" is enabled
- Extract .zip to a permanent folder (not Downloads)
- Reload extension after code changes

**Not translating**
- Check extension icon - should show "enabled"
- Press Enter (not Shift+Enter) to trigger translation
- For non-AI sites, click icon to manually enable
