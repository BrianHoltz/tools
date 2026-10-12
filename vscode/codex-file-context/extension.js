const vscode = require('vscode');

function activate(context) {
  context.subscriptions.push(vscode.commands.registerCommand(
    'brianholtz.addActiveFileToCodex', async () => {
      // Custom Markdown editors have a tab URI but no activeTextEditor.
      // Prefer the active tab to avoid attaching a stale text editor's file.
      const tab = vscode.window.tabGroups.activeTabGroup.activeTab;
      const input = tab?.input;
      const uri = input instanceof vscode.TabInputText ||
        input instanceof vscode.TabInputCustom ? input.uri : undefined;
      if (!uri || uri.scheme !== 'file') {
        await vscode.window.showInformationMessage(
          'Focus a file tab before adding it to Codex.');
        return;
      }
      try {
        await vscode.commands.executeCommand('chatgpt.addFileToThread', uri);
      } catch (error) {
        await vscode.window.showErrorMessage(
          `Could not add the file to Codex: ${error.message}`);
      }
    }
  ));
}

module.exports = { activate };
