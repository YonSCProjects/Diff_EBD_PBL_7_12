// md-to-pdf configuration for the Arduino PBL Program build pipeline.
// Used by build_outputs.bat via: npx md-to-pdf --config-file md-to-pdf.config.js
//
// Produces A4 PDF with clean typography suitable for Ministry submission.

module.exports = {
  // Page layout
  pdf_options: {
    format: 'A4',
    margin: {
      top: '25mm',
      right: '20mm',
      bottom: '25mm',
      left: '20mm',
    },
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: `
      <div style="width: 100%; font-size: 9pt; color: #999; text-align: center; padding: 0 20mm;">
        <span class="pageNumber"></span> / <span class="totalPages"></span>
      </div>
    `,
  },

  // Stylesheet for the rendered HTML/PDF
  stylesheet: [],

  // Custom CSS applied to the document
  css: `
    body {
      font-family: 'Segoe UI', Arial, -apple-system, 'Noto Sans', sans-serif;
      font-size: 11pt;
      line-height: 1.6;
      color: #000;
    }

    h1 {
      font-size: 22pt;
      margin-top: 28pt;
      margin-bottom: 10pt;
      border-bottom: 2pt solid #000;
      padding-bottom: 6pt;
    }

    h2 {
      font-size: 16pt;
      margin-top: 22pt;
      margin-bottom: 8pt;
      border-bottom: 1pt solid #ccc;
      padding-bottom: 4pt;
    }

    h3 {
      font-size: 13pt;
      margin-top: 16pt;
      margin-bottom: 6pt;
    }

    h4 {
      font-size: 11pt;
      margin-top: 12pt;
      margin-bottom: 4pt;
    }

    p {
      margin: 6pt 0;
      text-align: justify;
    }

    blockquote {
      margin: 10pt 0;
      padding: 8pt 16pt;
      border-left: 4pt solid #ccc;
      background: #f9f9f9;
      font-style: italic;
    }

    code {
      font-family: 'Consolas', 'Courier New', monospace;
      font-size: 10pt;
      background: #f4f4f4;
      padding: 1pt 4pt;
      border-radius: 2pt;
    }

    pre {
      background: #f4f4f4;
      border: 1pt solid #ddd;
      padding: 10pt 14pt;
      font-family: 'Consolas', 'Courier New', monospace;
      font-size: 9pt;
      line-height: 1.4;
      overflow-x: auto;
      page-break-inside: avoid;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      margin: 10pt 0;
      font-size: 10pt;
      page-break-inside: avoid;
    }

    th, td {
      border: 1pt solid #000;
      padding: 6pt 8pt;
      text-align: left;
      vertical-align: top;
    }

    th {
      background: #eee;
      font-weight: bold;
    }

    hr {
      border: none;
      border-top: 1pt solid #ccc;
      margin: 20pt 0;
    }

    ul, ol {
      margin: 6pt 0;
      padding-left: 24pt;
    }

    li {
      margin: 3pt 0;
    }

    /* Page break before major sections */
    h1 {
      page-break-before: always;
    }

    h1:first-of-type {
      page-break-before: avoid;
    }

    /* Keep headings with their content */
    h2, h3, h4 {
      page-break-after: avoid;
    }

    /* Emphasize the title page */
    h1:first-of-type {
      font-size: 26pt;
      text-align: center;
      border-bottom: 3pt solid #000;
      padding-bottom: 10pt;
      margin-top: 40pt;
    }
  `,

  // Launch options for Chromium
  launch_options: {
    args: ['--no-sandbox'],
  },
};
