import * as vscode from 'vscode';
import { exec } from 'child_process';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
  let disposable = vscode.commands.registerCommand('ai-task-agent.runAgent', async () => {
    const task = await vscode.window.showInputBox({
      prompt: 'What task would you like the AI Agent to do?'
    });

    if (!task) {
      vscode.window.showWarningMessage('No task entered.');
      return;
    }

    // Get the workspace folder (handle multiple folders if necessary)
    const workspaceFolder = vscode.workspace.workspaceFolders ? vscode.workspace.workspaceFolders[0].uri.fsPath : '';

    if (!workspaceFolder) {
      vscode.window.showErrorMessage('No workspace folder found.');
      return;
    }

    const terminal = vscode.window.createTerminal('AI Agent');
    const scriptPath = path.join(workspaceFolder, 'agent.py');

    terminal.sendText(`python3 ${scriptPath} "${task}"`);
    terminal.show();
  });

  context.subscriptions.push(disposable);
}

export function deactivate() {}
