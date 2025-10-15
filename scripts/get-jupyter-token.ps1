# Secure Jupyter Token Recovery - PowerShell Script
# Safely retrieves Jupyter token from .env file without logging to history

param(
    [string]$EnvFile = ".env",
    [switch]$ShowUrls = $false,
    [switch]$Quiet = $false
)

function Get-JupyterToken {
    param([string]$EnvPath)
    
    if (-not (Test-Path $EnvPath)) {
        Write-Host "❌ Error: .env file not found at $EnvPath" -ForegroundColor Red
        return $null
    }
    
    try {
        $content = Get-Content $EnvPath -ErrorAction Stop
        
        foreach ($line in $content) {
            $line = $line.Trim()
            
            # Skip comments and empty lines
            if ($line -match '^\s*#' -or $line -eq '') {
                continue
            }
            
            # Look for JUPYTER_TOKEN
            if ($line -match '^JUPYTER_TOKEN=(.+)$') {
                $token = $matches[1].Trim()
                
                # Remove quotes if present
                $token = $token -replace '^["'']|["'']$', ''
                
                # Validate token
                if ($token -eq '' -or $token -eq 'your-secure-token-here' -or $token -eq 'change-me') {
                    Write-Host "⚠️  Warning: Jupyter token appears to be a placeholder" -ForegroundColor Yellow
                    return $null
                }
                
                return $token
            }
        }
        
        Write-Host "❌ Error: JUPYTER_TOKEN not found in .env file" -ForegroundColor Red
        return $null
        
    } catch {
        Write-Host "❌ Error reading .env file: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}
}

function Show-JupyterUrls {
    param([string]$Token)
    
    if (-not $Token) { return }
    
    Write-Host ""
    Write-Host "🚀 Jupyter Lab Access Information:" -ForegroundColor Cyan
    Write-Host ("=" * 50) -ForegroundColor Gray
    Write-Host "🌐 Jupyter Lab:     http://localhost:8888/lab?token=$Token" -ForegroundColor Green
    Write-Host "📓 Classic Notebook: http://localhost:8888/tree?token=$Token" -ForegroundColor Green
    Write-Host "🔑 Token Only:       $Token" -ForegroundColor Yellow
    Write-Host ("=" * 50) -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "💡 Security Tips:" -ForegroundColor Cyan
    Write-Host "• Copy the URL before the terminal scrolls" -ForegroundColor White
    Write-Host "• Don't share the token in screenshots or logs" -ForegroundColor White
    Write-Host "• Consider using 'docker compose logs jupyter' for auto-generated URLs" -ForegroundColor White
}

function Main {
    if (-not $Quiet) {
        Write-Host "🔐 Secure Jupyter Token Recovery" -ForegroundColor Cyan
        Write-Host ("=" * 32) -ForegroundColor Gray
    }
    
    # Get token securely
    $token = Get-JupyterToken -EnvPath $EnvFile
    
    if ($token) {
        if (-not $Quiet) {
            Write-Host "✅ Token retrieved successfully" -ForegroundColor Green
        }
        
        if ($ShowUrls) {
            Show-JupyterUrls -Token $token
        } else {
            if (-not $Quiet) {
                $response = Read-Host "`n❓ Display Jupyter URLs? (y/N)"
                if ($response -match '^[yY]') {
                    Show-JupyterUrls -Token $token
                } else {
                    Write-Host "`n🔑 Token: $token" -ForegroundColor Yellow
                    Write-Host "💡 Use this token to access Jupyter Lab at http://localhost:8888" -ForegroundColor Cyan
                }
            } else {
                # Quiet mode - just output the token
                Write-Output $token
            }
        }
    } else {
        if (-not $Quiet) {
            Write-Host "`n❌ Failed to retrieve Jupyter token" -ForegroundColor Red
            Write-Host "`n🔧 Troubleshooting:" -ForegroundColor Cyan
            Write-Host "1. Ensure .env file exists in the current directory" -ForegroundColor White
            Write-Host "2. Check that JUPYTER_TOKEN is set in .env file" -ForegroundColor White
            Write-Host "3. Verify the token is not a placeholder value" -ForegroundColor White
        }
        exit 1
    }
}

# Run main function
Main