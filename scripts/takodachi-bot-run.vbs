Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

vbsFullName = WScript.ScriptFullName
vbsDirectory = fso.GetParentFolderName(vbsFullName)
projectRoot = fso.GetParentFolderName(vbsDirectory)

WshShell.CurrentDirectory = projectRoot

' 🌟 核心修正：使用 /c 參數（執行完就關閉 CMD 容器），並直接呼叫 uv
' 也可以直接寫成 "cmd.exe /c ""uv run bot""" (如果你 pyproject.toml 有設定的話)
cmdCommand = "cmd.exe /c ""uv run python -m takodachi_bot.takodachi"""

' 🟢 最後參數改為 0，代表徹底隱藏 CMD 視窗，實現完全無痛背景執行！
WshShell.Run cmdCommand, 0, False