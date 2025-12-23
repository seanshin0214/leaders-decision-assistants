const fs = require('fs');
const path = require('path');

const SOURCE_DIR = 'C:\\Users\\Sean K. S. Shin\\.persona';
const DEST_DIR = path.join(__dirname, 'community');

// Category mapping
const getCategoryFromFilename = (filename) => {
  if (filename.includes('innovation') || filename.includes('ai-expert')) return 'Innovation & Technology';
  if (filename.includes('academic') || filename.includes('tutor') || filename.includes('teacher')) return 'Education & Learning';
  if (filename.includes('business') || filename.includes('strategy') || filename.includes('consultant')) return 'Business & Professional';
  if (filename.includes('policy')) return 'Policy & Analysis';
  if (filename.includes('designer') || filename.includes('creative')) return 'Design & Creative';
  if (filename.includes('developer') || filename.includes('programming')) return 'Programming';
  return 'Professional Services';
};

const files = fs.readdirSync(SOURCE_DIR).filter(f => f.endsWith('.txt'));

console.log(`Found ${files.length} persona files`);

files.forEach(file => {
  const sourcePath = path.join(SOURCE_DIR, file);
  const destPath = path.join(DEST_DIR, file);

  const content = fs.readFileSync(sourcePath, 'utf-8');
  const personaName = file.replace('.txt', '').replace(/^\d+-/, '');
  const category = getCategoryFromFilename(file);

  const metadata = `# Persona: ${personaName}
# Author: @seanshin0214
# Category: ${category}
# Version: 1.0
# License: MIT (Free for all, revenue sharing if commercialized)

${content}`;

  fs.writeFileSync(destPath, metadata, 'utf-8');
  console.log(`✅ ${file}`);
});

console.log(`\n🎉 Imported ${files.length} personas!`);
