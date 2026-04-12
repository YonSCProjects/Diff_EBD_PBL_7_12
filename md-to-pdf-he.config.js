// md-to-pdf configuration for Hebrew RTL documents.
// Used for generating the Hebrew overview PDF.
// Based on md-to-pdf.config.js with RTL + Hebrew font adjustments.

module.exports = {
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

  stylesheet: [],

  css: `
    body {
      font-family: Arial, 'Segoe UI', -apple-system, 'Noto Sans Hebrew', sans-serif;
      font-size: 11pt;
      line-height: 1.7;
      color: #000;
      direction: rtl;
      text-align: right;
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
      border-right: 4pt solid #ccc;
      border-left: none;
      background: #f9f9f9;
      font-style: italic;
    }

    code {
      font-family: 'Consolas', 'Courier New', monospace;
      font-size: 10pt;
      background: #f4f4f4;
      padding: 1pt 4pt;
      border-radius: 2pt;
      direction: ltr;
      unicode-bidi: isolate;
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
      direction: ltr;
      text-align: left;
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
      text-align: right;
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
      padding-right: 24pt;
      padding-left: 0;
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

    h2, h3, h4 {
      page-break-after: avoid;
    }

    /* Title page */
    h1:first-of-type {
      font-size: 24pt;
      text-align: center;
      border-bottom: 3pt solid #000;
      padding-bottom: 10pt;
      margin-top: 40pt;
    }

    /* Evidence lines in italic — keep LTR for citations */
    em {
      direction: ltr;
      unicode-bidi: isolate;
      display: inline;
    }

    /* But italic Hebrew paragraphs should stay RTL */
    p > em:only-child {
      direction: rtl;
      unicode-bidi: normal;
      display: block;
    }
  `,

  launch_options: {
    args: ['--no-sandbox'],
  },
};
