Attribute VB_Name = "Module1"
Sub StandardFormating()
Attribute StandardFormating.VB_ProcData.VB_Invoke_Func = " \n14"
    ' Insert rows and columns
    Range("A1").EntireColumn.Insert
    Columns("A:A").Select
    Selection.ColumnWidth = 1.25
    For i = 1 To 3
        Range("A1").EntireRow.Insert
    Next i
    
    ' Format all cells
    Cells.Select
    Range("B1").Activate
    With Selection.Font
        .Name = "Arial"
        .Strikethrough = False
        .Bold = False
        .Size = 9
        .Superscript = False
        .Subscript = False
        .OutlineFont = False
        .Shadow = False
        .Underline = xlUnderlineStyleNone
        .ColorIndex = xlAutomatic
        .TintAndShade = 0
        .ThemeFont = xlThemeFontNone
    End With
    With Selection.Interior
        .Pattern = xlSolid
        .PatternColorIndex = xlAutomatic
        .ThemeColor = xlThemeColorDark1
        .TintAndShade = 0
        .PatternTintAndShade = 0
    End With
    
    ' Format B1
    Range("B1").Select
    With Selection.Font
        .Name = "Arial"
        .Strikethrough = False
        .Bold = True
        .Size = 14
        .Superscript = False
        .Subscript = False
        .OutlineFont = False
        .Shadow = False
        .Underline = xlUnderlineStyleNone
        .Color = -10477568
        .TintAndShade = 0
        .ThemeFont = xlThemeFontNone
    End With
    
    Selection.Formula = _
        "=MID(CELL(""filename"", A1),FIND(""]"",CELL(""filename"", A1))+1,255)"
End Sub

Sub A1Save()
    'Declare variables and data types
    Dim sht As Worksheet
     
    'Don't show any changes the macro does on the screen to make the macro faster.
    Application.ScreenUpdating = False
    
    For Each sht In ActiveWorkbook.Worksheets
        'Check if worksheet is not hidden
        If sht.Visible Then
            'Activate sheet
            sht.Activate
            'Select cell A1 in active worksheet
            Range("A1").Select
            'Zoom to first cell
            ActiveWindow.ScrollRow = 1
            ActiveWindow.ScrollColumn = 1
        End If
    Next sht
    'Go back to the worksheet when this event started
    Worksheets(1).Activate
    'Show all changes made to the workbook
    Application.ScreenUpdating = True
    
    ActiveWorkbook.Save
End Sub

Sub FormatCols()
'
' FormatCols Macro
'
    Dim colName As String
    For Each cel In Application.Selection
        ' Replace underscores and Proper Case
        colName = StrConv(Replace(cel.Value, "_", " "), vbProperCase)
        colName = CapitalizeSubString(colName, "Id")
        colName = CapitalizeSubString(colName, "Dma")
        ' Reassignment
        cel.Value = colName
    Next cel
End Sub

Function CapitalizeSubString(s As String, t As String) As String
    ' Beginning
    If StrComp(Left(s, Len(t)), t) = 0 Then
        s = UCase(t) & Right(s, Len(s) - Len(t))
    End If
    ' Middle
    s = Replace(s, " " & t & " ", " " & UCase(t) & " ")
    ' End
    If StrComp(Right(s, Len(t) + 1), " " & t) = 0 Then
        s = Left(s, Len(s) - Len(t)) & UCase(t)
    End If
    ' Full String Match
    If StrComp(s, t) = 0 Then
        s = UCase(t)
    End If
    CapitalizeSubString = s
End Function

Sub AddHeaderSheet()
    'Don't show any changes the macro does on the screen to make the macro faster.
    Application.ScreenUpdating = False
    
    Dim ws As Worksheet
    Set ws = Sheets.Add()
    ws.Activate
    Cells.Select
    With Selection.Interior
        .Pattern = xlSolid
        .PatternColorIndex = xlAutomatic
        .ThemeColor = xlThemeColorDark1
        .TintAndShade = 0
        .PatternTintAndShade = 0
    End With
    With Selection.Font
        .Name = "Arial"
        .Size = 9
        .Strikethrough = False
        .Superscript = False
        .Subscript = False
        .OutlineFont = False
        .Shadow = False
        .Underline = xlUnderlineStyleNone
        .Color = -10477568
        .TintAndShade = 0
        .ThemeFont = xlThemeFontNone
    End With
    Range("A16").Select
    With Selection.Font
        .Name = "Arial"
        .Size = 36
        .Bold = True
    End With
    ActiveCell.FormulaR1C1 = _
        "=MID(CELL(""filename"",R[-15]C),FIND(""]"",CELL(""filename"",R[-15]C))+1,255)"
    
    'Format and Name Sheet
    ActiveSheet.Tab.Color = RGB(0, 32, 96)
    ws.Name = InputBox("Please enter a sheet name") & " -->"
    
    'Show all changes made to the workbook
    Application.ScreenUpdating = True
    
End Sub
