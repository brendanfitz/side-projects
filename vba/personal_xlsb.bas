Attribute VB_Name = "Module1"
Sub FormatCols()
'
' FormatCols Macro
'
    For Each cel In Application.Selection
        cel.Value = StrConv(Replace(cel.Value, "_", " "), vbProperCase)
    Next cel
End Sub

Sub AddHeaderSheet()
'
' format_header_sheet Macro
'

'
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
    ActiveSheet.Tab.Color = RGB(0, 32, 96)
    ws.Name = InputBox("Please enter a sheet name")
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
