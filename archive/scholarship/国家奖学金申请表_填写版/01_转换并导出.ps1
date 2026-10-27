[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$SourcePath,
    [Parameter(Mandatory=$true)][string]$OutputPath
)
throw "Historical archive: Office and original-material workflows are disabled by default. Read docs/archive-guide.md."

$ErrorActionPreference = 'Stop'
$source = $SourcePath
$outputDir = $OutputPath
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
$docx = Join-Path $outputDir '原表转换.docx'
$pdf = Join-Path $outputDir '原表预览.pdf'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($source, $false, $true)
    $doc.SaveAs2($docx, 16)
    $doc.ExportAsFixedFormat($pdf, 17)
    Write-Output ("Pages=" + $doc.ComputeStatistics(2))
    Write-Output ("Tables=" + $doc.Tables.Count)
    Write-Output ("Paragraphs=" + $doc.Paragraphs.Count)
    $doc.Close($false)
}
finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
Write-Output $docx
Write-Output $pdf
