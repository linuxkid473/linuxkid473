#!/usr/bin/env node
/**
 * generate-activity.js
 *
 * Fetches the latest commit on the PureUNIX repository (public GitHub REST
 * API) and renders assets/activity.svg — a single kernel-log-style status
 * line showing which subsystem was most recently touched.
 *
 * Deliberately deterministic: the SVG only encodes data that comes from the
 * commit itself (sha, message, top-level path, commit date). No "generated
 * at" wall-clock timestamp is embedded, so re-running this script when
 * nothing has changed upstream produces byte-identical output and the
 * workflow will not create an empty commit.
 *
 * Env vars:
 *   OWNER         GitHub username/org that owns the PureUNIX repo (default: linuxkid473)
 *   REPO          Repository name (default: PureUNIX)
 *   GITHUB_TOKEN  Optional. If set, used as a bearer token to raise the API
 *                 rate limit. Never required for public repos.
 */

const OWNER = process.env.OWNER || "linuxkid473";
const REPO = process.env.REPO || "PureUNIX";
const API = "https://api.github.com";
const OUT_PATH = new URL("../assets/activity.svg", import.meta.url);

function escapeXml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

function truncate(str, max) {
  const clean = str.split("\n")[0].trim();
  if (clean.length <= max) return clean;
  return clean.slice(0, max - 1).trimEnd() + "\u2026";
}

async function githubFetch(path) {
  const headers = {
    Accept: "application/vnd.github+json",
    "User-Agent": `${OWNER}-profile-activity-generator`,
  };
  if (process.env.GITHUB_TOKEN) {
    headers.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`;
  }
  const res = await fetch(`${API}${path}`, { headers });
  if (!res.ok) {
    throw new Error(`GitHub API ${path} responded ${res.status}`);
  }
  return res.json();
}

function subsystemFromPath(filename) {
  if (!filename) return "root";
  const parts = filename.split("/");
  if (parts.length === 1) return "root";
  // Use the first two path segments when the top level is generic
  // (e.g. "src/usb/xhci.c" -> "src/usb"), otherwise just the first.
  const generic = new Set(["src", "kernel", "lib", "drivers"]);
  if (generic.has(parts[0]) && parts.length > 2) {
    return `${parts[0]}/${parts[1]}`;
  }
  return parts[0];
}

function renderSvg({ subsystem, sha, message, date }) {
  const safeSubsystem = escapeXml(subsystem);
  const safeMessage = escapeXml(truncate(message, 58));
  const safeSha = escapeXml(sha.slice(0, 7));
  const safeDate = escapeXml(date);

  return `<svg width="100%" viewBox="0 0 1000 110" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="actTitle actDesc">
  <title id="actTitle">PureUNIX latest activity</title>
  <desc id="actDesc">Most recently touched subsystem: ${safeSubsystem}. Commit ${safeSha}: ${safeMessage}. ${safeDate}.</desc>
  <defs>
    <linearGradient id="abg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0b0e12"/>
      <stop offset="100%" stop-color="#090b0e"/>
    </linearGradient>
    <linearGradient id="aedge" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2a323a"/>
      <stop offset="100%" stop-color="#171c21"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="998" height="108" rx="10" fill="url(#abg)" stroke="url(#aedge)" stroke-width="1.5"/>
  <g font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace">
    <text x="32" y="38" font-size="12" letter-spacing="1.5" fill="#5b6a72">/dev/log/pureunix.activity</text>
    <line x1="32" y1="50" x2="968" y2="50" stroke="#1c232b" stroke-width="1"/>
    <text x="32" y="80" font-size="14.5">
      <tspan fill="#4b5b63">[ sync ]</tspan>
      <tspan fill="#c9d3d6" dx="10">last touched:</tspan>
      <tspan fill="#7fb3ac" dx="6">${safeSubsystem}</tspan>
      <tspan fill="#3f4a52" dx="14">commit</tspan>
      <tspan fill="#8fa3ad" dx="6">${safeSha}</tspan>
      <tspan fill="#3f4a52" dx="14">${safeDate}</tspan>
    </text>
  </g>
</svg>
`;
}

async function main() {
  const [commitSummary] = await githubFetch(
    `/repos/${OWNER}/${REPO}/commits?per_page=1`
  );

  if (!commitSummary) {
    throw new Error("No commits returned for the PureUNIX repository.");
  }

  const commitDetail = await githubFetch(
    `/repos/${OWNER}/${REPO}/commits/${commitSummary.sha}`
  );

  const firstFile = (commitDetail.files && commitDetail.files[0]) || null;
  const subsystem = subsystemFromPath(firstFile && firstFile.filename);
  const message = commitSummary.commit.message;
  const date = (commitSummary.commit.committer || commitSummary.commit.author)
    .date.slice(0, 10);

  const svg = renderSvg({
    subsystem,
    sha: commitSummary.sha,
    message,
    date,
  });

  const fs = await import("node:fs/promises");
  await fs.writeFile(OUT_PATH, svg, "utf8");
  console.log(`Wrote ${OUT_PATH.pathname}`);
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
