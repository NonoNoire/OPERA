# OPERA lightweight Git sync helper
# Run this script from the repository root.

Write-Host "OPERA sync helper"
Write-Host "1. Pulling latest changes..."
git pull

Write-Host "2. Current repository status:"
git status

Write-Host ""
Write-Host "After reviewing the status, run:"
Write-Host "git add ."
Write-Host "git commit -m 'Update OPERA vault'"
Write-Host "git push"
