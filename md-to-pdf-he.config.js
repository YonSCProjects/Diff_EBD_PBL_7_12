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
      <div style="width: 100%; font-size: 9pt; color: #999; text-align: center; padding: 0 20mm;" id="footer-content">
        <span class="pageNumber"></span> / <span class="totalPages"></span>
      </div>
      <script>
        (function(){
          var pn = document.querySelector('.pageNumber');
          var fc = document.getElementById('footer-content');
          if (pn && fc && pn.textContent.trim() === '1') {
            fc.style.visibility = 'hidden';
          }
        })();
      </script>
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

    h1, h2, h3, h4, h5, h6 {
      page-break-after: avoid;
      break-after: avoid-page;
      page-break-inside: avoid;
      break-inside: avoid;
    }

    p, li {
      orphans: 3;
      widows: 3;
    }

    /* Belt-and-braces: forbid a page break between a heading and its first
     * following block element. Chromium honors this more reliably than
     * page-break-after: avoid alone. */
    h2 + p, h2 + ul, h2 + ol, h2 + table, h2 + blockquote,
    h3 + p, h3 + ul, h3 + ol, h3 + table, h3 + blockquote,
    h4 + p, h4 + ul, h4 + ol, h4 + table, h4 + blockquote {
      page-break-before: avoid;
      break-before: avoid-page;
    }

    /* Keep a table's lead-in sentence on the same page as the table
     * (Chicago §3.51, APA-7 §7.8). Covers direct lead-ins and lead-ins
     * separated from the table by one blockquote/paragraph/list. */
    p:has(+ table), ul:has(+ table), ol:has(+ table),
    blockquote:has(+ table),
    p:has(+ blockquote + table), p:has(+ p + table),
    p:has(+ ul + table), p:has(+ ol + table),
    blockquote:has(+ p + table), blockquote:has(+ blockquote + table) {
      page-break-after: avoid;
      break-after: avoid-page;
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

    /* But italic Hebrew paragraphs should stay RTL.
     * unicode-bidi: plaintext lets each text run determine direction
     * from its first strong character — handles mixed Hebrew + Latin
     * citation fragments without manual LRM markers. */
    p > em:only-child {
      direction: rtl;
      unicode-bidi: plaintext;
      display: block;
    }

    /* APA-7 hanging indent for references (RTL mirror) */
    .references p {
      padding-right: 2em;
      text-indent: -2em;
      text-align: right;
      margin: 4pt 0;
    }

    /* Defensive: explicit page break for appendix h1s */
    h1.appendix, h1[id^="נספח"] {
      page-break-before: always;
    }

    /* Table cell wrapping — prevent long model numbers from forcing column overflow */
    td {
      word-break: normal;
      overflow-wrap: anywhere;
    }
  `,

  launch_options: {
    args: ['--no-sandbox'],
  },
};
