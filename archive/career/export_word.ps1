
throw "Historical archive: Office and original-material workflows are disabled by default. Read docs/archive-guide.md."
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$deliverableDir = Join-Path $projectRoot '交付文件'
$wordInstance = New-Object -ComObject Word.Application
$wordInstance.Visible = $false
$wordInstance.DisplayAlerts = 0
$wordInstance.AutomationSecurity = 3
$report = @()
try {
    foreach ($file in (Get-ChildItem -LiteralPath $deliverableDir -Filter '*.docx' | Sort-Object Name)) {
        $doc = $null
        try {
            $doc = $wordInstance.Documents.Open($file.FullName, $false, $true, $false)
            $doc.Repaginate()
            $pages = $doc.ComputeStatistics(2)
            $targetPdf = [System.IO.Path]::ChangeExtension($file.FullName, '.pdf')
            $doc.ExportAsFixedFormat($targetPdf, 17)
            $report += [pscustomobject]@{name=$file.Name; pages=$pages; pdf=$targetPdf}
            Write-Output ($file.Name + ' pages=' + $pages)
        } finally {
            if ($null -ne $doc) { $doc.Close(0); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($doc) }
        }
    }
} finally {
    $wordInstance.Quit(0)
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($wordInstance)
}
$report | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'Word导出结果.json') -Encoding utf8
