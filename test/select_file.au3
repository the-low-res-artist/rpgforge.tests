; Autoit3 script to select an explorer window, activate it, wait for it to be ready, fill the file field and press ENTER

; Functions
Func GetCmdLineParam($cmdline, $index)
    If $index + 1 > UBound($cmdline) Then Return ""
    Return $cmdline[$index + 1]
EndFunc

; arguments
Global $winTitle = ""
Global $filePath = ""

For $i = 1 To $CMDLINE[0]
    Switch $CMDLINE[$i]
        Case "--winTitle"
            $winTitle = GetCmdLineParam($CMDLINE, $i)
        Case "--filePath"
            $filePath = GetCmdLineParam($CMDLINE, $i)
    EndSwitch
Next

; Activate the file dialog window by its title and wait for the file dialog to be active
WinActivate($winTitle)
WinWaitActive($winTitle)

; Sleep 1 sec
Sleep(1000)

; Set the file path in the file name input field
ControlSetText($winTitle, "", "Edit1", $filePath)
Send("{ENTER}")