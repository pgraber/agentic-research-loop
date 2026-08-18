#!/usr/bin/env bash
# Continuous validation helper for shell and pipeline steps (Nextflow processes, CLI tools, awk
# one-liners). Emits the same checks.log / checks.tsv contract as the R and Python helpers, so a
# pipeline written in any language contributes to one validation record.
#
# Works in bash and zsh.
#
# Usage:
#   source validate.sh
#   vcheck_init results/checks 02_align
#   vcheck "reads in FASTQ" "$(($(wc -l < reads.fq) / 4))" 12000000 "sequencing report"
#   vcheck "BAM files written" "$(ls -1 bam/*.bam | wc -l)" 24 "samplesheet.csv"
#   vcheck_summary
#
# Integer and string comparison only. A failed check returns non-zero and, under `set -e`, stops the
# run. Nothing downstream should execute on data of the wrong shape.

VCHECK_LOG=""
VCHECK_TSV=""
VCHECK_STEP=""
VCHECK_PASS=0
VCHECK_FAIL=0

vcheck_init() {
  local prefix="${1:-results/checks}"
  VCHECK_STEP="${2:-}"
  mkdir -p "$(dirname "$prefix")"
  VCHECK_LOG="${prefix}.log"
  VCHECK_TSV="${prefix}.tsv"
  VCHECK_PASS=0
  VCHECK_FAIL=0
  : > "$VCHECK_LOG"
  printf 'status\ttimestamp\tstep\tlabel\tactual\texpected\tsource\n' > "$VCHECK_TSV"
  _vwrite "=== validation: ${VCHECK_STEP:-analysis} ($(date '+%Y-%m-%d %H:%M:%S')) ==="
}

_vwrite() {
  printf '%s\n' "$1"
  [ -n "$VCHECK_LOG" ] && printf '%s\n' "$1" >> "$VCHECK_LOG"
}

# vcheck <label> <actual> <expected> [source]
vcheck() {
  # `status` and `source` are reserved in zsh, so the locals here are deliberately named
  # vstatus and src.
  local label="$1" actual="$2" expected="$3" src="${4:-}"
  [ -n "$VCHECK_LOG" ] || vcheck_init
  local vstatus="FAIL"
  [ "$actual" = "$expected" ] && vstatus="PASS"
  local ts detail
  ts="$(date '+%Y-%m-%d %H:%M:%S')"
  detail="${label}: ${actual} (expected ${expected})"
  [ -n "$src" ] && detail="${detail}  [${src}]"
  _vwrite "$(printf '%-4s %s  %s' "$vstatus" "$ts" "$detail")"
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$vstatus" "$ts" "$VCHECK_STEP" "$label" "$actual" "$expected" "$src" >> "$VCHECK_TSV"
  if [ "$vstatus" = "PASS" ]; then
    VCHECK_PASS=$((VCHECK_PASS + 1))
    return 0
  fi
  VCHECK_FAIL=$((VCHECK_FAIL + 1))
  printf 'Validation failed | %s\n' "$detail" >&2
  return 1
}

vcheck_summary() {
  _vwrite "--- $((VCHECK_PASS + VCHECK_FAIL)) checks: ${VCHECK_PASS} passed, ${VCHECK_FAIL} failed ---"
  [ "$VCHECK_FAIL" -eq 0 ]
}
