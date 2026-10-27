
throw "Historical archive: Office and original-material workflows are disabled by default. Read docs/archive-guide.md."
$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
$pptFile = Join-Path $taskRoot '交付文件\求职综合展示PPT\示例同学_求职综合展示_电力能源方向.pptx'
$renderDir = Join-Path $taskRoot 'PPT制作\qa\PowerPoint渲染'
$resultFile = Join-Path $taskRoot 'PPT制作\qa\PowerPoint实测.json'
$existingPowerPoint = @(Get-Process POWERPNT -ErrorAction SilentlyContinue).Count -gt 0
$powerPointApp = $null
$taskPresentation = $null
try {
    $powerPointApp = New-Object -ComObject PowerPoint.Application
    $taskPresentation = $powerPointApp.Presentations.Open($pptFile, -1, 0, 0)
    New-Item -ItemType Directory -Path $renderDir -Force | Out-Null
    $slideChecks = @()
    for ($slideNumber = 1; $slideNumber -le $taskPresentation.Slides.Count; $slideNumber++) {
        $taskSlide = $taskPresentation.Slides.Item($slideNumber)
        $outputImage = Join-Path $renderDir ('{0:D2}.png' -f $slideNumber)
        $taskSlide.Export($outputImage, 'PNG', 1672, 941)
        $slideChecks += [pscustomobject]@{ slide=$slideNumber; hidden=($taskSlide.SlideShowTransition.Hidden -eq -1); shapes=$taskSlide.Shapes.Count; exported=(Test-Path -LiteralPath $outputImage) }
    }
    [pscustomobject]@{ status='PASS'; application='Microsoft PowerPoint'; version=$powerPointApp.Version; opened_readonly=$true; slides=$taskPresentation.Slides.Count; width_points=$taskPresentation.PageSetup.SlideWidth; height_points=$taskPresentation.PageSetup.SlideHeight; checks=$slideChecks } | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $resultFile -Encoding utf8
    Write-Output ('PowerPoint PASS: {0} slides exported' -f $taskPresentation.Slides.Count)
}
catch {
    [pscustomobject]@{status='FAILED'; error=$_.Exception.Message} | ConvertTo-Json | Set-Content -LiteralPath $resultFile -Encoding utf8
    throw
}
finally {
    if ($null -ne $taskPresentation) { $taskPresentation.Close(); [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($taskPresentation) }
    if ($null -ne $powerPointApp) {
        if (-not $existingPowerPoint -and $powerPointApp.Presentations.Count -eq 0) { $powerPointApp.Quit() }
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($powerPointApp)
    }
}
