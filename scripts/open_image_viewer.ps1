param(
  [Parameter(Mandatory=$true)]
  [string]$ImagePath
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$viewer = Join-Path $root 'tools_image_viewer.html'
$chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

$resolved = (Resolve-Path -LiteralPath $ImagePath).Path
$src = ([Uri]$resolved).AbsoluteUri
$url = ([Uri]$viewer).AbsoluteUri + '?src=' + [Uri]::EscapeDataString($src)

if (Test-Path -LiteralPath $chrome) {
  Start-Process -FilePath $chrome -ArgumentList @('--new-window', $url)
} elseif (Test-Path -LiteralPath $edge) {
  Start-Process -FilePath $edge -ArgumentList @('--new-window', $url)
} else {
  Start-Process $url
}

Write-Output $url
