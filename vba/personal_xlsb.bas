Attribute VB_Name = "Module1"
Sub StandardFormating()
Attribute StandardFormating.VB_ProcData.VB_Invoke_Func = " \n14"
'
' Standard Formating Macro
'

'
    Range("A1").EntireColumn.Insert
    For I = 1 To 2
        Range("A1").EntireRow.Insert
    Next I
    Cells.Select
    Range("B1").Activate
    With Selection.Font
        .Name = "Arial"
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
    With Selection.Font
        .Name = "Arial"
        .Bold = True
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
    With Selection.Interior
        .Pattern = xlSolid
        .PatternColorIndex = xlAutomatic
        .ThemeColor = xlThemeColorDark1
        .TintAndShade = 0
        .PatternTintAndShade = 0
    End With
    With Selection.Font
        .Color = -10477568
        .TintAndShade = 0
    End With
    Columns("A:A").Select
    Selection.ColumnWidth = 1.25
    Range("B1").Select
    With Selection.Font
        .Name = "Arial"
        .Size = 12
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
