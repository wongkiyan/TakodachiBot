Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' 取得 VBS 檔案路徑並定位到專案根目錄
vbsFullName = WScript.ScriptFullName
vbsDirectory = fso.GetParentFolderName(vbsFullName)
projectRoot = fso.GetParentFolderName(vbsDirectory)

WshShell.CurrentDirectory = projectRoot

' 🌟 核心修正：直接呼叫 uv run，並用點號模組模式啟動
' /k 參數會讓 CMD 視窗在執行完或崩潰時留著不關閉
cmdCommand = "cmd.exe /k ""uv run python -m takodachi_bot.takodachi"""

' 最後參數為 1，代表強制顯示黑色 CMD 視窗
WshShell.Run cmdCommand, 1, False