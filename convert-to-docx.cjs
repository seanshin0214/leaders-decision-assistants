const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, HeadingLevel } = require('docx');

async function convertMarkdownToDocx(mdFilePath, outputPath) {
  const content = fs.readFileSync(mdFilePath, 'utf-8');
  const lines = content.split('\n');
  const children = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Skip empty lines
    if (line.trim() === '') {
      children.push(new Paragraph({ text: '' }));
      continue;
    }

    // Headings
    if (line.startsWith('# ')) {
      children.push(
        new Paragraph({
          text: line.replace(/^#\s+/, ''),
          heading: HeadingLevel.HEADING_1,
          spacing: { before: 400, after: 200 },
        })
      );
    } else if (line.startsWith('## ')) {
      children.push(
        new Paragraph({
          text: line.replace(/^##\s+/, ''),
          heading: HeadingLevel.HEADING_2,
          spacing: { before: 300, after: 150 },
        })
      );
    } else if (line.startsWith('### ')) {
      children.push(
        new Paragraph({
          text: line.replace(/^###\s+/, ''),
          heading: HeadingLevel.HEADING_3,
          spacing: { before: 240, after: 120 },
        })
      );
    } else if (line.startsWith('#### ')) {
      children.push(
        new Paragraph({
          text: line.replace(/^####\s+/, ''),
          heading: HeadingLevel.HEADING_4,
          spacing: { before: 200, after: 100 },
        })
      );
    }
    // Code blocks
    else if (line.startsWith('```')) {
      const codeLines = [];
      i++;
      while (i < lines.length && !lines[i].startsWith('```')) {
        codeLines.push(lines[i]);
        i++;
      }
      children.push(
        new Paragraph({
          children: [
            new TextRun({
              text: codeLines.join('\n'),
              font: 'Consolas',
              size: 20,
            }),
          ],
          shading: {
            fill: 'F5F5F5',
          },
          spacing: { before: 120, after: 120 },
        })
      );
    }
    // Lists
    else if (line.match(/^[\*\-]\s+/)) {
      children.push(
        new Paragraph({
          text: line.replace(/^[\*\-]\s+/, '• '),
          spacing: { before: 60, after: 60 },
        })
      );
    } else if (line.match(/^\d+\.\s+/)) {
      children.push(
        new Paragraph({
          text: line,
          spacing: { before: 60, after: 60 },
        })
      );
    }
    // Regular text
    else {
      children.push(
        new Paragraph({
          text: line,
          spacing: { before: 60, after: 60 },
        })
      );
    }
  }

  const doc = new Document({
    sections: [
      {
        properties: {},
        children: children,
      },
    ],
  });

  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
  console.log(`✓ Generated: ${outputPath}`);
}

async function main() {
  const docs = [
    { input: 'README.md', output: 'README.docx' },
    { input: 'INSTALL.md', output: 'INSTALL.docx' },
    { input: 'QUICKSTART.md', output: 'QUICKSTART.docx' },
    { input: 'SUMMARY.md', output: 'SUMMARY.docx' },
    { input: 'TECHNICAL_SPEC.md', output: 'TECHNICAL_SPEC.docx' },
  ];

  console.log('Converting Persona MCP documentation to Word format...\n');

  for (const doc of docs) {
    try {
      await convertMarkdownToDocx(doc.input, doc.output);
    } catch (error) {
      console.error(`✗ Failed to convert ${doc.input}:`, error.message);
    }
  }

  console.log('\nConversion complete!');
}

main().catch(console.error);
