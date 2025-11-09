Set WshShell = CreateObject("WScript.Shell")
scriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
batchFile = scriptDir & "\start_app.bat"
WshShell.Run "cmd /c """ & batchFile & """", 0, False
