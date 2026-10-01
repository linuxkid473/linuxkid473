#!/usr/bin/env node
/**
 * generate-activity.js
 *
 * Renders assets/activity.svg — a neon status line showing the most recently
 * pushed-to public repository and the commit that touched it.
 *
 * Data comes entirely from the public GitHub REST API:
 *   1. GET /users/{OWNER}/repos?sort=pushed&per_page=1   -> latest public repo
 *   2. GET /repos/{OWNER}/{repo}/commits?per_page=1      -> latest commit
 *
 * Deliberately deterministic: the SVG encodes only data returned by the API
 * (repo name, first changed path, sha, message, commit date). No "generated
 * at" wall-clock timestamp is embedded, so re-running this script when nothing
 * has changed upstream produces byte-identical output and the workflow will
 * not create an empty commit.
 *
 * Env vars:
 *   OWNER         GitHub username/org whose public activity is rendered
 *                 (default: linuxkid473)
 *   GITHUB_TOKEN  Optional. If set, used as a bearer token to raise the API
 *                 rate limit. Never required for public repositories.
 */

const OWNER = process.env.OWNER || "linuxkid473";
const API = "https://api.github.com";
const OUT_PATH = new URL("../assets/activity.svg", import.meta.url);

// Neon palette shared with the other profile panels.
const C = {
  dim: "#31505b",
  mid: "#5d7f8b",
  txt: "#d8fff4",
  green: "#39ff14",
  cyan: "#19f7ff",
  magenta: "#ff2bd6",
};
const MONO =
  "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace";

function escapeXml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

function truncate(str, max) {
  const clean = String(str).split("\n")[0].trim();
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

function renderSvg({ repo, url, subsystem, sha, message, date }) {
  const safeRepo = escapeXml(repo);
  const safeSubsystem = escapeXml(subsystem);
  const safeMessage = escapeXml(truncate(message, 96));
  const safeSha = escapeXml(sha.slice(0, 7));
  const safeDate = escapeXml(date);
  const safeUrl = escapeXml(url);

  return `<svg width="100%" viewBox="0 0 1000 132" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="actTitle actDesc">
  <title id="actTitle">Latest GitHub activity</title>
  <desc id="actDesc">Most recently pushed public repository: ${safeRepo}. Latest commit ${safeSha} on ${safeDate} touching ${safeSubsystem}: ${safeMessage}.</desc>
  <defs>
    <linearGradient id="abg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#04070b"/>
      <stop offset="100%" stop-color="#080d13"/>
    </linearGradient>
    <linearGradient id="aedge" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1d3a40"/>
      <stop offset="100%" stop-color="#0d1a1f"/>
    </linearGradient>
    <filter id="asoft" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.4" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <pattern id="agrid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0 H0 V40" fill="none" stroke="${C.cyan}" stroke-opacity="0.05" stroke-width="1"/>
    </pattern>
  </defs>
  <rect x="1" y="1" width="998" height="130" rx="12" fill="url(#abg)"/>
  <rect x="1" y="1" width="998" height="130" rx="12" fill="url(#agrid)"/>
  <g font-family="${MONO}">
    <text x="32" y="36" font-size="12.5" letter-spacing="1.5" fill="${C.mid}">/dev/log/github.activity</text>
    <text x="968" y="36" font-size="12" letter-spacing="1.5" fill="${C.dim}" text-anchor="end">tail -n 1</text>
    <line x1="32" y1="48" x2="968" y2="48" stroke="#0d1a1f" stroke-width="1"/>
    <text x="32" y="80" font-size="14.5">
      <tspan fill="${C.dim}">[ sync ]</tspan>
      <tspan fill="${C.txt}" dx="10">last touched:</tspan>
      <tspan fill="${C.green}" dx="6" filter="url(#asoft)">${safeRepo}</tspan>
      <tspan fill="${C.dim}" dx="6">&#9656;</tspan>
      <tspan fill="${C.cyan}" dx="6">${safeSubsystem}</tspan>
      <tspan fill="${C.dim}" dx="14">commit</tspan>
      <tspan fill="${C.mid}" dx="6">${safeSha}</tspan>
      <tspan fill="${C.dim}" dx="14">${safeDate}</tspan>
    </text>
    <text x="32" y="106" font-size="12.5" fill="${C.mid}">
      <tspan fill="${C.magenta}">msg:</tspan><tspan dx="7">${safeMessage}</tspan>
    </text>
    <text x="968" y="106" font-size="12" fill="${C.dim}" text-anchor="end">${safeUrl}</text>
  </g>
  <rect x="1" y="1" width="998" height="130" rx="12" fill="none" stroke="url(#aedge)" stroke-width="1.5"/>
</svg>
`;
}

async function main() {
  const repos = await githubFetch(
    `/users/${OWNER}/repos?sort=pushed&per_page=10&type=owner`
  );

  // Never pick the profile repo itself: the workflow commits activity.svg into
  // it, which would make it the most recently pushed repo and cause the panel
  // to regenerate (and commit) itself on every run.
  const candidates = (Array.isArray(repos) ? repos : []).filter(
    (r) => r && r.name && r.name !== OWNER && r.pushed_at
  );

  const latest = candidates[0];
  if (!latest) {
    throw new Error(`No public repositories returned for ${OWNER}.`);
  }

  const commits = await githubFetch(
    `/repos/${OWNER}/${latest.name}/commits?per_page=1`
  );
  const commitSummary = Array.isArray(commits) ? commits[0] : null;
  if (!commitSummary) {
    throw new Error(`No commits returned for ${OWNER}/${latest.name}.`);
  }

  const detail = await githubFetch(
    `/repos/${OWNER}/${latest.name}/commits/${commitSummary.sha}`
  );

  const firstFile = (detail.files && detail.files[0]) || null;
  const subsystem = subsystemFromPath(firstFile && firstFile.filename);
  const committedAt = commitSummary.commit.committer || commitSummary.commit.author;

  const svg = renderSvg({
    repo: latest.name,
    url: `github.com/${OWNER}/${latest.name}`,
    subsystem,
    sha: commitSummary.sha,
    message: commitSummary.commit.message,
    date: committedAt.date.slice(0, 10),
  });

  const fs = await import("node:fs/promises");
  await fs.writeFile(OUT_PATH, svg, "utf8");
  console.log(`Wrote ${OUT_PATH.pathname}`);
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});