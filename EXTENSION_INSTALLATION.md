# Installing the L-ZIP VS Code Extension

The L-ZIP VS Code extension provides status bar controls and token estimation for your L-ZIP workflows.

## 📦 Installation Methods

### Method 1: From VS Code Marketplace (Recommended)
*Coming soon* - Extension will be published to the official VS Code marketplace.

### Method 2: Direct Installation (Current)

#### Windows
```powershell
# Copy extension to VS Code extensions folder
$source = "path\to\L-ZIP\vscode-extension"
$dest = "$env:USERPROFILE\.vscode\extensions\ezixen.lzip-vscode-0.0.1"
Remove-Item -Path $dest -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item -Path $source -Destination $dest -Recurse -Force
```

#### macOS & Linux
```bash
# Copy extension to VS Code extensions folder
cd ~/.vscode/extensions
rm -rf ezixen.lzip-vscode-0.0.1
cp -r /path/to/L-ZIP/vscode-extension ezixen.lzip-vscode-0.0.1
```

### Method 3: From VSIX File

1. Navigate to the L-ZIP repository:
   ```bash
   cd L-ZIP/vscode-extension
   ```

2. Install vsce (VS Code extension tool):
   ```bash
   npm install -g @vscode/vsce
   ```

3. Package the extension:
   ```bash
   vsce package
   ```

4. In VS Code:
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
   - Type: "Extensions: Install from VSIX"
   - Select the `.vsix` file created above

## ✅ Verify Installation

After installation:

1. **Restart VS Code** completely
2. **Look at the bottom right of the status bar** - you should see:
   - `✓ L-ZIP MCP` - Current status indicator
   - `🧪 L-ZIP Estimator` - Token calculator button
3. **Test the extension:**
   - Click "🧪 L-ZIP Estimator"
   - Paste a prompt
   - See token savings calculated

## ⚙️ Configuration

Configure the extension in VS Code settings (`Ctrl+,` or `Cmd+,`):

```json
{
  "lzip.pythonPath": "python",
  "lzip.estimatorDefaultText": " Insert prompt to get an estimate of the token difference."
}
```

| Setting | Description | Default |
|---------|-------------|---------|
| `lzip.pythonPath` | Path to Python executable | `"python"` |
| `lzip.estimatorDefaultText` | Placeholder text in estimator | `" Insert prompt..."` |

## 🎯 Features

### Status Bar Buttons

- **L-ZIP MCP Toggle** (`✓ L-ZIP MCP`)
  - Click to enable/disable MCP status
  - Persists across sessions
  - Tooltip shows current state

- **L-ZIP Estimator** (`🧪 L-ZIP Estimator`)
  - Click to open token calculator
  - Enter any prompt to estimate compression
  - See original tokens vs L-ZIP tokens
  - View percentage savings
  - Copy compressed version to clipboard
  - Hover tooltip shows last calculation

### Token Estimator

When you click the estimator button:

1. **Input Box** appears with default text
2. **Paste or type your prompt**
3. **Results shown in Output Panel:**
   - Original prompt
   - L-ZIP translation
   - Token count comparison
   - Percentage saved
4. **One-click copy** of the compressed prompt

## 🔧 Troubleshooting

### Buttons Not Showing?
- Restart VS Code completely
- Check the status bar is visible (View → Appearance → Show Status Bar)
- Open Output panel to see extension errors

### Python Not Found?
- Ensure Python 3.8+ is installed
- Update `lzip.pythonPath` setting if Python is not in PATH
- Test: Open terminal and run `python --version`

### Compression Not Working?
- Verify L-ZIP is available in parent folder
- Check browser console (F12) for JavaScript errors
- Review Output panel for Python errors

### Extension Won't Activate?
- Clear VS Code cache: `rm -rf ~/.vscode/extensions/extz-*`
- Reinstall the extension
- Check Output → Extension Host for errors

## 📚 Usage Tips

### Quick Workflow
1. Prepare a verbose prompt
2. Click 🧪 L-ZIP Estimator
3. Paste your prompt
4. Review the L-ZIP translation
5. Click "Copy L-ZIP Translation" button
6. Paste into ChatGPT, Claude, Gemini, etc.
7. Get faster, more focused responses

### Token Savings Example
- **Original:** "Please write a Python function that validates email addresses with proper error handling and comprehensive test coverage"
- **L-ZIP:** `ACT:Dev [Lang:Python] OBJ:Email_Validator OUT:Function+Tests+ErrorHandling`
- **Savings:** 65% token reduction

## 🆘 Getting Help

- **Issues:** https://github.com/ezixen/L-ZIP/issues
- **Documentation:** https://github.com/ezixen/L-ZIP#readme
- **Examples:** See `examples.py` in main repository

## 📝 License

MIT License - Part of the L-ZIP project

---

**Need help?** Check the main [L-ZIP README](../README.md) for comprehensive documentation.
