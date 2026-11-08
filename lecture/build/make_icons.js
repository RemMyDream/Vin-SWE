// Render react-icons (Tabler set) to PNG files for the deck.
// Usage: node make_icons.js            -> writes assets/icons/<name>-<color>.png
// Add icons in ICONS below; colours in COLORS. Re-run after editing.
const path = require("path");
const fs = require("fs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const tb = require("react-icons/tb");

const COLORS = {
  white: "#FFFFFF",
  navy: "#114984",
  red: "#CA1F27",
  ink: "#1F2937",
  slate: "#536376",
  green: "#1E7B4F",
  amber: "#B7791F",
};

// name -> candidate Tabler component names (first one that exists wins)
const ICONS = {
  robot: ["TbRobot"],
  user: ["TbUser"],
  users: ["TbUsers"],
  spy: ["TbSpy", "TbUserX"],
  github: ["TbBrandGithub"],
  issue: ["TbMessageReport", "TbMessageCircle"],
  pr: ["TbGitPullRequest"],
  branch: ["TbGitBranch"],
  commit: ["TbGitCommit"],
  file: ["TbFileText"],
  filecode: ["TbFileCode"],
  folder: ["TbFolder"],
  key: ["TbKey"],
  lock: ["TbLock"],
  unlock: ["TbLockOpen"],
  shield: ["TbShieldCheck"],
  shieldx: ["TbShieldX"],
  database: ["TbDatabase"],
  dbx: ["TbDatabaseOff", "TbDatabaseX"],
  world: ["TbWorld"],
  www: ["TbWorldWww"],
  server: ["TbServer"],
  plug: ["TbPlug"],
  api: ["TbApi"],
  terminal: ["TbTerminal2"],
  code: ["TbCode"],
  mail: ["TbMail"],
  ticket: ["TbTicket"],
  alert: ["TbAlertTriangle", "TbAlertTriangleFilled"],
  bolt: ["TbBolt"],
  clock: ["TbClock"],
  eye: ["TbEye"],
  eyeoff: ["TbEyeOff"],
  trash: ["TbTrash"],
  cloud: ["TbCloud"],
  send: ["TbSend"],
  package: ["TbPackage"],
  settings: ["TbSettings"],
  hierarchy: ["TbHierarchy2", "TbHierarchy"],
  affiliate: ["TbAffiliate"],
  bug: ["TbBug"],
  virus: ["TbVirus"],
  list: ["TbListCheck"],
  hand: ["TbHandStop"],
  log: ["TbClipboardList"],
  fingerprint: ["TbFingerprint"],
  target: ["TbTargetArrow"],
  network: ["TbNetwork"],
  dns: ["TbWorldSearch", "TbSearch"],
  photo: ["TbPhoto"],
  timer: ["TbHourglass"],
  check: ["TbCircleCheck"],
  x: ["TbCircleX"],
  question: ["TbHelpCircle"],
  book: ["TbBook"],
  tool: ["TbTool"],
  layers: ["TbStack2"],
  scale: ["TbScale"],
  link: ["TbLink"],
  skull: ["TbSkull"],
  flame: ["TbFlame"],
  copy: ["TbCopy"],
  search: ["TbSearch"],
  message: ["TbMessage2"],
  id: ["TbId"],
  rocket: ["TbRocket"],
  arrowsplit: ["TbArrowsSplit2", "TbArrowsSplit"],
  versions: ["TbVersions"],
  certificate: ["TbCertificate"],
  pin: ["TbPinned"],
  slack: ["TbBrandSlack"],
  chart: ["TbChartBar"],
  quiz: ["TbBulb"],
};

const OUT = path.join(__dirname, "assets", "icons");
fs.mkdirSync(OUT, { recursive: true });

async function main() {
  const missing = [];
  for (const [name, cands] of Object.entries(ICONS)) {
    const compName = cands.find((c) => tb[c]);
    if (!compName) { missing.push(`${name} (${cands.join("/")})`); continue; }
    for (const [cname, hex] of Object.entries(COLORS)) {
      const svg = ReactDOMServer.renderToStaticMarkup(
        React.createElement(tb[compName], { size: 256, color: hex, strokeWidth: 1.7 })
      );
      const file = path.join(OUT, `${name}-${cname}.png`);
      await sharp(Buffer.from(svg), { density: 300 }).resize(256, 256).png().toFile(file);
    }
  }
  console.log(`icons written to ${OUT}`);
  if (missing.length) console.log("MISSING:", missing.join(", "));
}
main().catch((e) => { console.error(e); process.exit(1); });
