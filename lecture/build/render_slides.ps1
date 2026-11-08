# Render every slide of a .pptx to PNG using the installed Microsoft PowerPoint (COM).
# Usage:
#   powershell -ExecutionPolicy Bypass -File render_slides.ps1 -Deck <deck.pptx> -OutDir <dir> [-Width 1600] [-Slides "1,3,5"] [-Pdf]
# Output: <OutDir>\slide-01.png, slide-02.png, ... (and <OutDir>\<deck>.pdf with -Pdf)
param(
  [Parameter(Mandatory = $true)][string]$Deck,
  [Parameter(Mandatory = $true)][string]$OutDir,
  [int]$Width = 1600,
  [string]$Slides = "",
  [switch]$Pdf
)
$ErrorActionPreference = "Stop"
$deckPath = (Resolve-Path $Deck).Path
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$outPath = (Resolve-Path $OutDir).Path

$ppt = New-Object -ComObject PowerPoint.Application
try {
  # Open(FileName, ReadOnly, Untitled, WithWindow)
  $pres = $ppt.Presentations.Open($deckPath, -1, 0, 0)
  $ratio = $pres.PageSetup.SlideHeight / $pres.PageSetup.SlideWidth
  $height = [int]([math]::Round($Width * $ratio))
  $wanted = @()
  if ($Slides -ne "") { $wanted = $Slides.Split(",") | ForEach-Object { [int]$_.Trim() } }
  $n = $pres.Slides.Count
  for ($i = 1; $i -le $n; $i++) {
    if ($wanted.Count -gt 0 -and -not ($wanted -contains $i)) { continue }
    $file = Join-Path $outPath ("slide-{0:D2}.png" -f $i)
    $pres.Slides.Item($i).Export($file, "PNG", $Width, $height)
    Write-Output $file
  }
  if ($Pdf) {
    $pdfFile = Join-Path $outPath ([IO.Path]::GetFileNameWithoutExtension($deckPath) + ".pdf")
    $pres.SaveAs($pdfFile, 32)  # ppSaveAsPDF
    Write-Output $pdfFile
  }
  $pres.Close()
}
finally {
  $ppt.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
}
