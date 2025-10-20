#!/usr/bin/env bash
set -euo pipefail

# === CONFIGURATION ===
opt_dir="../opt/"        # Directory containing opt_log and .out files
template="template_coup.in"     # Template file in current directory
log_file="$opt_dir/opt_log"     # opt_log path inside opt_dir

# === CHECK INPUT FILES ===
if [[ ! -f "$log_file" ]]; then
  echo "ERROR: $log_file not found." >&2
  exit 1
fi
if [[ ! -f "$template" ]]; then
  echo "ERROR: $template not found." >&2
  exit 1
fi

# === MAIN LOOP ===
while read -r first _; do
  [[ -z "${first:-}" ]] && continue
  if [[ "$first" != *"-opt-"*".out" ]]; then
    continue
  fi

  src_out="$opt_dir/$first"
  if [[ ! -f "$src_out" ]]; then
    echo "WARN: '$src_out' not found; skipping."
    continue
  fi

  # Create destination filename (replace opt→coup and .out→.in)
  base="$(basename -- "$src_out")"
  dest="${base/opt/coup}"
  dest="${dest%.out}.in"

  # Copy template to destination
  cp -f "$template" "$dest"

  # Find the line number where optimization converged
  line_num=$(grep -n "OPTIMIZATION CONVERGED" "$src_out" | tail -n 1 | cut -d: -f1 || true)
  if [[ -z "$line_num" ]]; then
    echo "WARN: 'OPTIMIZATION CONVERGED' not found in '$src_out'; leaving template as-is."
    continue
  fi

  # Extract geometry section: 160 lines starting 15 lines after convergence
  start=$((line_num + 15))
  tmp_geom="$(mktemp)"
  sed -n "${start},$((start+159))p" "$src_out" > "$tmp_geom"

  # Strip FIRST 10 CHARACTERS from EACH line
  sed -E 's/^.{10}//' "$tmp_geom" > "${tmp_geom}_stripped"

  # Insert stripped geometry after 2nd line in the template
  {
    head -n 2 "$dest"
    cat "${tmp_geom}_stripped"
    tail -n +3 "$dest" 2>/dev/null || true
  } > "${dest}.tmp" && mv "${dest}.tmp" "$dest"

  rm -f "$tmp_geom" "${tmp_geom}_stripped"

  echo "✅ Created '$dest' with geometry (first 10 characters stripped)."

done < "$log_file"

