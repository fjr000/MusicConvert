$ErrorActionPreference = "Stop"

# 下载并准备本项目运行/打包所需的第三方命令行工具。
# 临时文件写入 .tmp-tools/，最终只覆盖 tools/ffmpeg/ 与 tools/musicdecrypto/ 下的目标 exe。

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$TempDir = Join-Path $Root ".tmp-tools"
$FfmpegDir = Join-Path $Root "tools\ffmpeg"
$MusicDir = Join-Path $Root "tools\musicdecrypto"
$FfmpegZip = Join-Path $TempDir "ffmpeg.zip"
$MusicArchive = Join-Path $TempDir "musicdecrypto.archive"

$FfmpegUrl = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-lgpl.zip"
$MusicReleaseApi = "https://api.github.com/repos/davidxuang/MusicDecrypto/releases/tags/v2.4.2"

New-Item -ItemType Directory -Force -Path $TempDir, $FfmpegDir, $MusicDir | Out-Null

function Download-File($Url, $OutFile) {
    Write-Host "下载 $Url"
    Invoke-WebRequest -Uri $Url -OutFile $OutFile
}

function Expand-ToolArchive($Archive, $Destination) {
    if ($Archive -match "(?i)\.zip$") {
        Expand-Archive -Force -Path $Archive -DestinationPath $Destination
        return
    }

    $TarPath = Join-Path $env:WINDIR "System32\tar.exe"
    if (-not (Test-Path $TarPath)) {
        $Tar = Get-Command tar -ErrorAction SilentlyContinue
        if (-not $Tar) {
            throw "无法解压 $Archive，请安装 tar/7-Zip 后重试，或手动放置目标 exe"
        }
        $TarPath = $Tar.Source
    }

    & $TarPath -xf $Archive -C $Destination
    if ($LASTEXITCODE -ne 0) {
        throw "解压 $Archive 失败，请手动放置目标 exe"
    }
}

function Copy-First($SourceRoot, $Name, $TargetDir) {
    $File = Get-ChildItem -Path $SourceRoot -Recurse -File -Filter $Name | Select-Object -First 1
    if (-not $File) {
        throw "未在 $SourceRoot 中找到 $Name"
    }

    $Target = Join-Path $TargetDir $Name
    Copy-Item -Force -Path $File.FullName -Destination $Target
    Write-Host "已准备 $Target"
}

Download-File $FfmpegUrl $FfmpegZip
$FfmpegExtractDir = Join-Path $TempDir "ffmpeg"
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $FfmpegExtractDir
Expand-ToolArchive $FfmpegZip $FfmpegExtractDir
Copy-First $FfmpegExtractDir "ffmpeg.exe" $FfmpegDir
Copy-First $FfmpegExtractDir "ffprobe.exe" $FfmpegDir

Write-Host "查询 MusicDecrypto v2.4.2 发布资产"
$Release = Invoke-RestMethod -Uri $MusicReleaseApi -Headers @{ "User-Agent" = "MusicConvert-setup-tools" }
$Asset = $Release.assets |
    Where-Object { $_.name -match "(?i)(win|windows)" -and $_.name -match "(?i)(x64|amd64)" -and $_.name -notmatch "(?i)arm64" -and $_.name -match "(?i)(cli|command)" -and $_.name -match "(?i)\.(zip|7z)$" } |
    Select-Object -First 1

if (-not $Asset) {
    throw "未找到 MusicDecrypto Windows x64 CLI 压缩包，请查看 https://github.com/davidxuang/MusicDecrypto/releases/tag/v2.4.2 后手动放置 tools/musicdecrypto/musicdecrypto.exe"
}

Download-File $Asset.browser_download_url $MusicArchive
$MusicExtractDir = Join-Path $TempDir "musicdecrypto"
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue $MusicExtractDir
Expand-ToolArchive $MusicArchive $MusicExtractDir
Copy-First $MusicExtractDir "musicdecrypto.exe" $MusicDir

Write-Host "工具准备完成。"
