# Upgrade All Personas to World-Class+
# Version 2.3.0

Write-Host "=== World-Class+ Upgrade Started ===" -ForegroundColor Cyan
Write-Host "Upgrading all 142 personas to World-Class+ standard" -ForegroundColor Cyan
Write-Host ""

$communityDir = ".\community"
$personaDir = "$env:USERPROFILE\.persona"
$upgraded = 0
$alreadyPlus = 0
$errors = 0

# World-Class+ Standard Introduction Template
$worldClassPlusIntro = @"
You are a World-Class+ {ROLE} with extensive experience and deep expertise in your field.

You bring world-class standards, best practices, and proven methodologies to every task. Your approach combines theoretical knowledge with practical, real-world experience.

As a World-Class+ professional, you:
- ✅ Apply evidence-based practices from authoritative sources
- ✅ Challenge assumptions with disruptive questions
- ✅ Integrate cross-disciplinary insights
- ✅ Maintain ethical standards and inclusive practices
- ✅ Drive continuous improvement and innovation

---
"@

Write-Host "Processing persona files..." -ForegroundColor Yellow

Get-ChildItem $communityDir -Filter "*.txt" | ForEach-Object {
    $file = $_.FullName
    $fileName = $_.Name
    $content = Get-Content $file -Raw -Encoding UTF8
    
    # Check if already World-Class+
    if ($content -match "World-Class\+") {
        Write-Host "  ⏭️  SKIP: $fileName (already World-Class+)" -ForegroundColor Gray
        $alreadyPlus++
        return
    }
    
    try {
        # Extract role name from first line
        $firstLine = ($content -split "`n")[0]
        $roleName = ""
        
        if ($firstLine -match "You are a (.+?) with") {
            $roleName = $matches[1]
        } elseif ($firstLine -match "World-Class (.+?) Expert") {
            $roleName = $matches[1]
        } else {
            # Extract from filename
            $roleName = ($fileName -replace '\d+-', '' -replace '\.txt$', '' -replace '-', ' ')
            $roleName = (Get-Culture).TextInfo.ToTitleCase($roleName)
        }
        
        # Upgrade pattern 1: "World-Class ... Expert" → "World-Class+"
        $newContent = $content -replace "You are a World-Class (.+?) Expert", "You are a World-Class+ `$1"
        
        # Upgrade pattern 2: "World-Class Expert" → "World-Class+"
        $newContent = $newContent -replace "World-Class Expert", "World-Class+"
        
        # Add World-Class+ intro if not present
        if ($newContent -notmatch "As a World-Class\+ professional") {
            # Find the first "---" and insert before it
            if ($newContent -match "(.*?)(---.*)" -and $newContent -notmatch "World-Class\+.*?---") {
                $beforeDash = $matches[1]
                $afterDash = $matches[2]
                
                # Create role-specific intro
                $roleIntro = $worldClassPlusIntro -replace "\{ROLE\}", $roleName
                
                $newContent = $beforeDash.TrimEnd() + "`n`n" + $roleIntro + $afterDash
            }
        }
        
        # Add World-Class+ badge in content
        $newContent = $newContent -replace "# Persona:", "# Persona: (World-Class+)`n# Original:"
        
        # Save updated content
        Set-Content -Path $file -Value $newContent -Encoding UTF8 -NoNewline
        
        Write-Host "  ✅ UPGRADED: $fileName → World-Class+" -ForegroundColor Green
        $upgraded++
        
    } catch {
        Write-Host "  ❌ ERROR: $fileName - $($_.Exception.Message)" -ForegroundColor Red
        $errors++
    }
}

Write-Host ""
Write-Host "=== Upgrade Summary ===" -ForegroundColor Cyan
Write-Host "✅ UPGRADED: $upgraded personas" -ForegroundColor Green
Write-Host "⏭️  ALREADY World-Class+: $alreadyPlus personas" -ForegroundColor Yellow
Write-Host "❌ ERRORS: $errors personas" -ForegroundColor Red

# Copy to ~/.persona
Write-Host "`nCopying to ~/.persona..." -ForegroundColor Yellow
Copy-Item "$communityDir\*.txt" -Destination $personaDir -Force
Write-Host "✅ Copied to $personaDir" -ForegroundColor Green

# Count final state
$totalPersonas = (Get-ChildItem $communityDir -Filter "*.txt").Count
$worldClassPlusCount = 0

Get-ChildItem $communityDir -Filter "*.txt" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    if ($content -match "World-Class\+") {
        $worldClassPlusCount++
    }
}

Write-Host ""
Write-Host "=== Final Status ===" -ForegroundColor Cyan
Write-Host "Total Personas: $totalPersonas" -ForegroundColor White
Write-Host "World-Class+ Personas: $worldClassPlusCount" -ForegroundColor Green
Write-Host "Percentage: $([math]::Round(($worldClassPlusCount / $totalPersonas) * 100, 1))%" -ForegroundColor Green

Write-Host ""
Write-Host "=== World-Class+ Upgrade Completed! ===" -ForegroundColor Green
