const vscode = require('vscode');
const cp = require('child_process');
const path = require('path');

const MCP_STATE_KEY = 'lzip.mcpEnabled';

function activate(context) {
  console.log('L-ZIP extension is activating...');
  
  const outputChannel = vscode.window.createOutputChannel('L-ZIP Estimator');
  let estimatorVisible = false;
  let lastEstimate = null;

  const toggleStatusBar = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Right,
    100
  );
  toggleStatusBar.command = 'lzip.toggleMcp';

  const estimatorStatusBar = vscode.window.createStatusBarItem(
    vscode.StatusBarAlignment.Right,
    99
  );
  estimatorStatusBar.command = 'lzip.toggleEstimator';

  const updateStatusBar = () => {
    const enabled = context.globalState.get(MCP_STATE_KEY, true);
    toggleStatusBar.text = enabled ? '$(check) L-ZIP MCP' : '$(circle-slash) L-ZIP MCP';
    toggleStatusBar.tooltip = enabled
      ? 'L-ZIP MCP is enabled. Click to disable.'
      : 'L-ZIP MCP is disabled. Click to enable.';
    estimatorStatusBar.text = '$(beaker) L-ZIP Estimator';
    if (lastEstimate) {
      estimatorStatusBar.tooltip =
        `Tokens saved (rough): ${lastEstimate.savedTokens} ` +
        `(${lastEstimate.percentSaved}%). Click to ${
          estimatorVisible ? 'close' : 'open'
        }.`;
    } else {
      estimatorStatusBar.tooltip = estimatorVisible
        ? 'L-ZIP estimator is open. Click to close.'
        : 'Open the L-ZIP estimator.';
    }
  };

  const toggleMcp = vscode.commands.registerCommand('lzip.toggleMcp', async () => {
    const enabled = context.globalState.get(MCP_STATE_KEY, true);
    await context.globalState.update(MCP_STATE_KEY, !enabled);
    updateStatusBar();
    vscode.window.showInformationMessage(
      `L-ZIP MCP ${!enabled ? 'enabled' : 'disabled'}.`
    );
  });

  const toggleEstimator = vscode.commands.registerCommand(
    'lzip.toggleEstimator',
    async () => {
      if (estimatorVisible) {
        outputChannel.hide();
        estimatorVisible = false;
        updateStatusBar();
        return;
      }

      const config = vscode.workspace.getConfiguration('lzip');
      const defaultText = config.get(
        'estimatorDefaultText',
        ' Insert prompt to get an estimate of the token difference.'
      );

      const promptText = await vscode.window.showInputBox({
        title: 'L-ZIP Token Estimator',
        prompt: 'Paste or type a prompt to estimate token savings.',
        value: defaultText,
        valueSelection: [0, defaultText.length]
      });

      if (promptText === undefined) {
        return;
      }

      if (!promptText.trim() || promptText.trim() === defaultText.trim()) {
        vscode.window.showInformationMessage('No prompt provided.');
        return;
      }

      const workspaceRoot =
        vscode.workspace.workspaceFolders &&
        vscode.workspace.workspaceFolders.length > 0
          ? vscode.workspace.workspaceFolders[0].uri.fsPath
          : context.extensionPath;

      // If we're in the vscode-extension folder, use parent directory for lzip module
      const lzipRoot = workspaceRoot.endsWith('vscode-extension') 
        ? path.dirname(workspaceRoot) 
        : workspaceRoot;

      const pythonPath = config.get('pythonPath', 'python');

      let lzipPrompt = '';
      let errorMessage = '';

      try {
        const translation = await translatePrompt(
          promptText,
          pythonPath,
          lzipRoot
        );
        lzipPrompt = translation.lzip_prompt || '';
      } catch (error) {
        errorMessage = error && error.message ? error.message : String(error);
      }

      const originalTokens = roughTokenCount(promptText);
      const finalTokens = lzipPrompt ? roughTokenCount(lzipPrompt) : originalTokens;
      const savedTokens = originalTokens - finalTokens;
      const percentSaved =
        originalTokens > 0
          ? Math.round((savedTokens / originalTokens) * 1000) / 10
          : 0;

      outputChannel.clear();
      outputChannel.appendLine('L-ZIP Token Estimator');
      outputChannel.appendLine('='.repeat(60));
      outputChannel.appendLine('');
      
      if (lzipPrompt) {
        outputChannel.appendLine('✅ L-ZIP TRANSLATED PROMPT (Copy this to use):');
        outputChannel.appendLine('-'.repeat(60));
        outputChannel.appendLine(lzipPrompt);
        outputChannel.appendLine('-'.repeat(60));
        outputChannel.appendLine('');
        outputChannel.appendLine(`📊 Token Savings: ${savedTokens} tokens (${percentSaved}% reduction)`);
        outputChannel.appendLine(`   Original: ${originalTokens} tokens → L-ZIP: ${finalTokens} tokens`);
        outputChannel.appendLine('');
        outputChannel.appendLine('📝 Original Prompt:');
        outputChannel.appendLine(promptText);
      } else {
        outputChannel.appendLine('❌ L-ZIP Translation Failed');
        outputChannel.appendLine('');
        outputChannel.appendLine('Original Prompt:');
        outputChannel.appendLine(promptText);
        outputChannel.appendLine('');
        outputChannel.appendLine(`Original tokens (rough): ${originalTokens}`);
      }

      if (errorMessage) {
        outputChannel.appendLine('');
        outputChannel.appendLine('⚠️ Translation Error:');
        outputChannel.appendLine(errorMessage);
      }

      outputChannel.show(true);
      estimatorVisible = true;
      
      // Show info message with option to copy
      if (lzipPrompt) {
        vscode.window.showInformationMessage(
          `L-ZIP saved ${savedTokens} tokens (${percentSaved}%)`,
          'Copy L-ZIP Translation'
        ).then(selection => {
          if (selection === 'Copy L-ZIP Translation') {
            vscode.env.clipboard.writeText(lzipPrompt);
            vscode.window.showInformationMessage('L-ZIP translation copied to clipboard!');
          }
        });
      }
      
      lastEstimate = {
        savedTokens,
        percentSaved
      };
      updateStatusBar();
    }
  );

  context.subscriptions.push(
    toggleStatusBar,
    estimatorStatusBar,
    toggleMcp,
    toggleEstimator,
    outputChannel
  );

  updateStatusBar();
  toggleStatusBar.show();
  estimatorStatusBar.show();
  
  console.log('L-ZIP extension activated successfully. Status bar items should be visible.');
}

function translatePrompt(promptText, pythonPath, workspaceRoot) {
  const script = [
    'import json',
    'import sys',
    'from lzip import LZIPTranslator',
    'text = sys.stdin.read()',
    'translator = LZIPTranslator()',
    'lzip_prompt, meta = translator.translate_to_lzip(text)',
    'print(json.dumps({"lzip_prompt": lzip_prompt, "meta": meta}))'
  ].join('\n');

  return new Promise((resolve, reject) => {
    const proc = cp.spawn(pythonPath, ['-c', script], {
      cwd: workspaceRoot
    });

    let stdout = '';
    let stderr = '';

    proc.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    proc.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    proc.on('error', (error) => {
      reject(error);
    });

    proc.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(stderr || `Python exited with code ${code}.`));
        return;
      }

      try {
        const parsed = JSON.parse(stdout.trim());
        resolve(parsed);
      } catch (error) {
        reject(new Error('Failed to parse L-ZIP output.'));
      }
    });

    proc.stdin.write(promptText);
    proc.stdin.end();
  });
}

function roughTokenCount(text) {
  return Math.max(1, Math.ceil(text.length / 4));
}

function deactivate() {}

module.exports = {
  activate,
  deactivate
};
