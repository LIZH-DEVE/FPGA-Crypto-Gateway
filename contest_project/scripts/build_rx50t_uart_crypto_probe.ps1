$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$tcl = Join-Path $scriptDir 'create_rx50t_uart_crypto_probe_project.tcl'

$vivadoCandidates = @(
    $env:VIVADO_BIN,
    $env:RX50T_VIVADO_BAT,
    'C:\Xilinx\Vivado\2024.1\bin\vivado.bat',
    'D:\Xilinx\Vivado\2024.1\bin\vivado.bat'
) | Where-Object { $_ }

$vivado = $null
foreach ($candidate in $vivadoCandidates) {
    if (Test-Path $candidate) {
        $vivado = $candidate
        break
    }
}

if (-not $vivado) {
    $cmd = Get-Command vivado.bat -ErrorAction SilentlyContinue
    if ($cmd) {
        $vivado = $cmd.Source
    }
}

if (-not $vivado) {
    throw 'Vivado 2024.1 not found. Set VIVADO_BIN or RX50T_VIVADO_BAT, or add vivado.bat to PATH.'
}

if (!(Test-Path $tcl)) {
    throw "Script not found: $tcl"
}

& $vivado -mode batch -source $tcl
if ($LASTEXITCODE -ne 0) {
    throw "Vivado build failed with exit code $LASTEXITCODE"
}
