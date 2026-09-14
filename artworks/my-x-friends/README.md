# My X Friends

Static follower portrait wall at https://andrew-zyf.github.io/my-x-friends/.

- Snapshot: 2026-09-14, all 1,326 accounts from @andrew_zyf/followers, including 7 default avatars. Not historical follow order; no automatic refresh.
- Source: adapted from https://github.com/yuezengwu/yueonline under MIT. Attribution links to 岳增五 and First Thousand appear at the bottom.
- Source files live here. Build output lives in `/my-x-friends/`; do not edit the output directly.
- At repository root: `npm ci`, `npm run dev`, `npm run build`. Commit the built output for the existing branch-based GitHub Pages deployment.
- `tools/prepare-portraits.py <captured-followers.json> <workspace-cache-dir>` builds the atlas from a verified full snapshot using Pillow. No credentials belong in this repository.
- Desktop and mobile layouts grow with the collection size. The overview displays each account exactly once.
