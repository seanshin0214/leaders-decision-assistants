# Update Git Remote URL after GitHub Repository Rename
# Run this AFTER renaming the repository on GitHub

Write-Host "=== Updating Git Remote URL ===" -ForegroundColor Cyan
Write-Host ""

# Show current remote
Write-Host "Current remote URL:" -ForegroundColor Yellow
git remote -v

Write-Host ""
Write-Host "Updating to new repository name..." -ForegroundColor Green

# Update remote URL
git remote set-url origin https://github.com/seanshin0214/world-class-leadership-personas.git

Write-Host ""
Write-Host "New remote URL:" -ForegroundColor Yellow
git remote -v

Write-Host ""
Write-Host "=== Update Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Testing connection..." -ForegroundColor Yellow
git fetch origin

Write-Host ""
Write-Host "✅ Git remote successfully updated!" -ForegroundColor Green
Write-Host "New repository: https://github.com/seanshin0214/world-class-leadership-personas" -ForegroundColor Cyan
