# 一键打包 Windows 便携版 release。
# 流程:检查 Python -> 安装依赖 -> 准备第三方工具 -> 清理旧产物 -> PyInstaller 打包 -> 校验并报告。
#
# 用法:
#   powershell -ExecutionPolicy Bypass -File scripts/build-release.ps1
# 可选开关:
#   -SkipDeps    跳过 pip 依赖安装(假定已装好 pyinstaller/tkinterdnd2)
#   -SkipTools   跳过第三方工具下载(要求 tools/ 下已就位,缺失则报错)
#   -Python <p>  指定 Python 解释器(默认 python)

param(
    [switch]$SkipDeps,
    [switch]$SkipTools,
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

$AppName = "音乐格式转换器"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

function Step($msg) { Write-Host "`n==> $msg" -ForegroundColor Cyan }
function Assert-ExitCode($what) {
    if ($LASTEXITCODE -ne 0) {
        throw "$what 失败(exit $LASTEXITCODE)"
    }
}

Step "检查 Python"
& $Python --version
Assert-ExitCode "Python 检查"

# 1. 安装打包依赖
if ($SkipDeps) {
    Step "跳过依赖安装(-SkipDeps)"
} else {
    Step "安装依赖(requirements.txt)"
    & $Python -m pip install -r requirements.txt
    Assert-ExitCode "pip install"
}

# 2. 准备第三方工具(ffmpeg / ffprobe / musicdecrypto)
$RequiredTools = @(
    "tools\ffmpeg\ffmpeg.exe",
    "tools\ffmpeg\ffprobe.exe",
    "tools\musicdecrypto\musicdecrypto.exe"
)
$Missing = $RequiredTools | Where-Object { -not (Test-Path (Join-Path $Root $_)) }
if ($Missing) {
    if ($SkipTools) {
        throw "缺少第三方工具:`n  $($Missing -join "`n  ")`n请先运行 scripts/setup-tools.ps1 或手动放置后重试"
    }
    Step "准备第三方工具(缺失 $($Missing.Count) 个,调用 setup-tools.ps1)"
    & (Join-Path $PSScriptRoot "setup-tools.ps1")
} else {
    Step "第三方工具已就位"
}

# 3. 确保 inputs / outputs 目录存在(随包分发,作为默认输入/输出区)
Step "准备 inputs / outputs 目录"
foreach ($d in @("inputs", "outputs")) {
    $p = Join-Path $Root $d
    New-Item -ItemType Directory -Force -Path $p | Out-Null
    $keep = Join-Path $p ".gitkeep"
    if (-not (Test-Path $keep)) { New-Item -ItemType File -Path $keep | Out-Null }
}

# 4. 关闭可能占用 dist 的旧实例,清理旧产物
Step "清理旧构建"
Get-Process -Name $AppName -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 500
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue (Join-Path $Root "build")
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue (Join-Path $Root "dist")

# 5. PyInstaller 打包(用 python -m 调用,避免 PATH 里没有 pyinstaller.exe)
Step "PyInstaller 打包"
& $Python -m PyInstaller music_converter.spec -y --clean
Assert-ExitCode "PyInstaller 打包"

# 6. 校验产物
Step "校验产物"
$DistDir = Join-Path $Root "dist\$AppName"
$Exe = Join-Path $DistDir "$AppName.exe"
if (-not (Test-Path $Exe)) { throw "未找到产物 $Exe" }
foreach ($d in @("inputs", "outputs", "_internal")) {
    if (-not (Test-Path (Join-Path $DistDir $d))) { throw "产物缺少目录:$d" }
}
$TotalMB = [math]::Round((Get-ChildItem -Path $DistDir -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB, 2)

Write-Host "`n打包完成 ✓" -ForegroundColor Green
Write-Host "产物目录: $DistDir"
Write-Host "总大小  : $TotalMB MB"

# 7. 生成两个 release zip
Step "生成 release zip"
$FullZip = Join-Path $Root "$AppName-v1.0.0-Windows-完整版.zip"
$LiteZip = Join-Path $Root "$AppName-v1.0.0-Windows-精简版.zip"

# 完整版（含 FFmpeg）
if (Test-Path $FullZip) { Remove-Item $FullZip -Force }
Compress-Archive -Path $DistDir -DestinationPath $FullZip -CompressionLevel Optimal
$fullMB = [math]::Round((Get-Item $FullZip).Length / 1MB, 2)
Write-Host "完整版: $FullZip ($fullMB MB)"

# 精简版（移除 FFmpeg 后压缩）
$LiteDir = Join-Path $Root "dist\${AppName}-lite"
Copy-Item -Recurse -Force $DistDir $LiteDir
$FfmpegDir = Join-Path $LiteDir "_internal\tools\ffmpeg"
Get-ChildItem -Path $FfmpegDir -Include *.exe,*.dll -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force
if (Test-Path $LiteZip) { Remove-Item $LiteZip -Force }
Compress-Archive -Path $LiteDir -DestinationPath $LiteZip -CompressionLevel Optimal
Remove-Item -Recurse -Force $LiteDir
$liteMB = [math]::Round((Get-Item $LiteZip).Length / 1MB, 2)
Write-Host "精简版: $LiteZip ($liteMB MB，首次启动需联网下载 FFmpeg)"

Write-Host "`n两个版本已生成 ✓" -ForegroundColor Green
