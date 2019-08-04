Attribute VB_Name = "Cleaning"
Sub PythonList()
    Dim list_str As String
    Dim i As Integer
    
    list_str = "["
    i = 1
    For Each c In Application.Selection.Cells
        If i <> 1 Then
            list_str = list_str & ", "
        End If
        list_str = list_str & Chr(39) & c.Value & Chr(39)
        i = i + 1
    Next c
    list_str = list_str & "]"
    
    Selection.End(xlDown).Select
    ActiveCell.Offset(1, 0).Select
    Selection.Value = list_str
End Sub
