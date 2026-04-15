// Build w5_three_leds_and_button_pulldown.fzz by merging Step4 (3 LEDs) + Step3 button section,
// with button shifted +5 columns to avoid LED3/button pin conflict.
// Usage: node fritzing_steps/_build_w5.js
const fs = require('fs');
const path = require('path');
const JSZip = require('jszip');

const ROOT = path.resolve(__dirname, '..');
const STEP3 = path.join(__dirname, 'Step3_AddButton_Pin2.fzz');
const STEP4 = path.join(__dirname, 'Step4_ThreeLEDs_Chase.fzz');
const OUT_STEP = path.join(__dirname, 'Step5_ThreeLEDs_AddButton.fzz');
const OUT_W5 = path.join(ROOT, 'Arduino_Projects/Project_1_Light_Signals/images/fritzing/w5_three_leds_and_button_pulldown.fzz');

// pin-number remap for button section (Step3 → shifted w5 layout)
const PIN_MAP = { '22': '27', '24': '29', '28': '31' };
// modelIndex remap for Step3's button-section instances
const MI_MAP = {
  '9000012': '9000020', // SW1
  '9000013': '9000021', // Rpulldown
  '9000015': '9000022', // wire btn→D2
  '9000016': '9000023', // wire Wrail→btn
  '9000017': '9000024', // wire pulldown→Yrail
  '9000018': '9000025', // wire Arduino5V→Wrail(pin3W)
};

function remapPins(xml) {
  return xml.replace(/pin(22|24|28)([A-Z])/g, (_, n, col) => 'pin' + PIN_MAP[n] + col);
}
function remapMI(xml) {
  return xml.replace(/modelIndex="(9000012|9000013|9000015|9000016|9000017|9000018)"/g, (_, mi) => 'modelIndex="' + MI_MAP[mi] + '"');
}
function remapPartIDSuffix(xml) {
  // Button & pulldown x-coords shift by +45 px (5 cols * 9 px).
  // Only adjust the specific known x values.
  return xml
    // SW1 body x
    .replace(/x="248\.7"/g, 'x="293.7"')
    // Rpulldown x
    .replace(/x="270\.6"/g, 'x="315.6"');
}

function extractInstance(xml, predicate) {
  // Find <instance ...> ... </instance> block matching predicate (string on open tag).
  const re = /<instance[^>]*>[\s\S]*?<\/instance>/g;
  const hits = [];
  let m;
  while ((m = re.exec(xml)) !== null) {
    if (predicate(m[0])) hits.push(m[0]);
  }
  return hits;
}

(async () => {
  const step3Zip = await JSZip.loadAsync(fs.readFileSync(STEP3));
  const step4Zip = await JSZip.loadAsync(fs.readFileSync(STEP4));
  const step3Name = Object.keys(step3Zip.files).find(n => n.endsWith('.fz'));
  const step4Name = Object.keys(step4Zip.files).find(n => n.endsWith('.fz'));
  const step3Xml = await step3Zip.file(step3Name).async('string');
  const step4Xml = await step4Zip.file(step4Name).async('string');

  // 1. Extract button parts + wires from Step3
  const partsToLift = extractInstance(step3Xml, s => {
    // Only match the instance's OWN modelIndex (on the opening tag).
    const m = s.match(/^<instance[^>]*modelIndex="([0-9]+)"/);
    if (!m) return false;
    return ['9000012','9000013','9000015','9000016','9000017','9000018'].includes(m[1]);
  });
  console.log('lifted', partsToLift.length, 'instances from Step3');

  // 2. Transform each: remap pins, modelIndices, x-coords
  const transformed = partsToLift.map(s => remapPartIDSuffix(remapMI(remapPins(s))));

  // 3. Build new <connector>…</connector> entries for the Breadboard's breadboardView/connectors,
  //    lifted & remapped from Step3's breadboard section.
  const bbConnectorBlockRe = /<breadboardView layer="breadboard"[\s\S]*?<\/breadboardView>/g;
  // Pull Step3's breadboard instance block first
  const step3BreadboardMatch = step3Xml.match(/<instance moduleIdRef="0152b316[\s\S]*?<\/instance>/);
  if (!step3BreadboardMatch) throw new Error('Step3 breadboard instance not found');
  const step3BB = step3BreadboardMatch[0];
  // Extract all connector entries that reference the button-section pins
  const pinConnectorRe = /<connector connectorId="pin(22|24|28)[A-Z]"[\s\S]*?<\/connector>/g;
  const pinConnectors = step3BB.match(pinConnectorRe) || [];
  const pin3WConnector = (step3BB.match(/<connector connectorId="pin3W"[\s\S]*?<\/connector>/) || [])[0];
  console.log('lifted', pinConnectors.length, 'breadboard pin connectors (22/24/28) +',
              pin3WConnector ? '1 pin3W' : '0 pin3W');
  const remappedPinConnectors = pinConnectors.map(s => remapMI(remapPins(s)));
  // pin3W stays as pin3W, only the connect modelIndex needs remap (→ 9000025)
  const remappedPin3W = pin3WConnector ? remapMI(pin3WConnector) : '';

  // 4. Splice these into Step4's breadboard instance.
  const step4BreadboardMatch = step4Xml.match(/<instance moduleIdRef="0152b316[\s\S]*?<\/instance>/);
  if (!step4BreadboardMatch) throw new Error('Step4 breadboard instance not found');
  const step4BB = step4BreadboardMatch[0];
  // Insert before </connectors> inside breadboardView
  const addConnectors = [...remappedPinConnectors, ...(remappedPin3W ? [remappedPin3W] : [])].join('\n                        ');
  const newBB = step4BB.replace(
    /(<\/connectors>\s*<\/breadboardView>)/,
    `                        ${addConnectors}\n                    $1`
  );

  // 5. Replace breadboard block in Step4 with the augmented one and append new instances.
  let outXml = step4Xml.replace(step4BB, newBB);
  // Append instances before </instances>
  const newInstancesBlock = '\n        ' + transformed.join('\n        ') + '\n';
  outXml = outXml.replace(/(\s*)<\/instances>/, `${newInstancesBlock}$1</instances>`);

  // 6. Write .fzz
  async function writeFzz(file, xml, innerName) {
    const outZip = new JSZip();
    outZip.file(innerName, xml);
    const buf = await outZip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' });
    fs.writeFileSync(file, buf);
    console.log('wrote', file, '(' + buf.length + ' bytes)');
  }
  await writeFzz(OUT_STEP, outXml, 'Step5_ThreeLEDs_AddButton.fz');
  await writeFzz(OUT_W5, outXml, 'w5_three_leds_and_button_pulldown.fz');
})();
