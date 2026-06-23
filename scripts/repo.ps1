param(
    [Parameter(Position = 0)]
    [ValidateSet("bootstrap", "inventory", "migrate-plan", "validate", "test", "quality-gate", "m1-readiness", "status")]
    [string]$Command = "status",

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$RemainingArgs
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$SafeRepoRoot = ($RepoRoot.Path -replace "\\", "/")

function Test-PythonCandidate {
    param(
        [string]$Executable,
        [string[]]$PrefixArgs = @()
    )
    try {
        & $Executable @PrefixArgs "--version" *> $null
        if ($LASTEXITCODE -eq 0) {
            return [pscustomobject]@{
                Executable = $Executable
                PrefixArgs = $PrefixArgs
            }
        }
    }
    catch {
        return $null
    }
    return $null
}

function Resolve-HarnessPython {
    if ($env:LOXFS_HARNESS_PYTHON) {
        $candidate = Test-PythonCandidate -Executable $env:LOXFS_HARNESS_PYTHON
        if ($candidate) {
            return $candidate
        }
        Write-Error "LOXFS_HARNESS_PYTHON is set but is not executable."
    }

    $candidate = Test-PythonCandidate -Executable "py" -PrefixArgs @("-3")
    if ($candidate) {
        return $candidate
    }

    $candidate = Test-PythonCandidate -Executable "python"
    if ($candidate) {
        return $candidate
    }

    Write-Error "No Python interpreter found. Set LOXFS_HARNESS_PYTHON, install py -3, or make python available on PATH."
}

function Invoke-HarnessPython {
    param(
        [string[]]$PythonCommand
    )
    $python = Resolve-HarnessPython
    $prefix = @($python.PrefixArgs)
    & $python.Executable @prefix @PythonCommand
    exit $LASTEXITCODE
}

function Invoke-SafeGit {
    param(
        [string[]]$GitArgs
    )
    & git "-c" "safe.directory=$SafeRepoRoot" @GitArgs
}

switch ($Command) {
    "status" {
        Write-Output "repo_root=$($RepoRoot.Path)"
        Write-Output "local_root_env=$($env:LOXFS_CMD_SIG_LOCAL_ROOT)"
        Write-Output "python_env=$($env:LOXFS_HARNESS_PYTHON)"
        $statusCode = 0
        Invoke-SafeGit @("rev-parse", "--show-toplevel")
        if ($LASTEXITCODE -ne 0) { $statusCode = $LASTEXITCODE }
        Invoke-SafeGit @("status", "--short")
        if ($LASTEXITCODE -ne 0) { $statusCode = $LASTEXITCODE }
        Invoke-SafeGit @("remote", "-v")
        if ($LASTEXITCODE -ne 0) { $statusCode = $LASTEXITCODE }
        exit $statusCode
    }
    "bootstrap" {
        Invoke-HarnessPython -PythonCommand (@("-B", (Join-Path $ScriptDir "bootstrap_local_workspace.py"), "--root", $RepoRoot.Path) + $RemainingArgs)
    }
    "inventory" {
        Invoke-HarnessPython -PythonCommand (@("-B", (Join-Path $ScriptDir "inventory_local_artifacts.py"), "--root", $RepoRoot.Path) + $RemainingArgs)
    }
    "migrate-plan" {
        Invoke-HarnessPython -PythonCommand (@("-B", (Join-Path $ScriptDir "migrate_local_workspace.py"), "--root", $RepoRoot.Path) + $RemainingArgs)
    }
    "validate" {
        Invoke-HarnessPython -PythonCommand (@("-B", (Join-Path $ScriptDir "validate_repo.py"), "--root", $RepoRoot.Path) + $RemainingArgs)
    }
    "test" {
        Invoke-HarnessPython -PythonCommand (@("-B", "-m", "unittest", "discover", "-s", (Join-Path $RepoRoot.Path "tests"), "-p", "test_*.py") + $RemainingArgs)
    }
    "quality-gate" {
        Invoke-HarnessPython -PythonCommand (@("-B", (Join-Path $ScriptDir "quality_gate.py"), "--root", $RepoRoot.Path) + $RemainingArgs)
    }
    "m1-readiness" {
        Invoke-HarnessPython -PythonCommand (@("-B", (Join-Path $ScriptDir "m1_readiness.py"), "--root", $RepoRoot.Path) + $RemainingArgs)
    }
}
