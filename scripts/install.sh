#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

OVERWRITE=false
DRY_RUN=false

COPIED_COUNT=0
SKIPPED_COUNT=0
WARN_COUNT=0
FOUND_CLIENTS=0
MISSING_CLIENTS=0

usage() {
  cat <<'EOF'
Usage: ./scripts/install.sh [--overwrite] [--dry-run] [--help]

Installs skills, subagents, and prompts by copying files from this repository
into detected client directories in your home folder and current project.

Options:
  --overwrite   Replace existing files in detected destinations
  --dry-run     Print actions without writing files
  --help        Show this help message
EOF
}

log_info() {
  printf '[INFO] %s\n' "$1"
}

log_warn() {
  WARN_COUNT=$((WARN_COUNT + 1))
  printf '[WARN] %s\n' "$1"
}

copy_collection() {
  local source_dir="$1"
  local dest_dir="$2"
  local label="$3"

  if [[ ! -d "$source_dir" ]]; then
    log_warn "Source directory missing for ${label}: ${source_dir}"
    return
  fi

  mkdir -p "$dest_dir"
  log_info "Installing ${label}: ${source_dir} -> ${dest_dir}"

  local file
  local files_found=false
  shopt -s nullglob
  for file in "$source_dir"/*.md; do
    files_found=true
    local base_name
    base_name="$(basename "$file")"
    if [[ "$base_name" == example-* ]]; then
      SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
      log_info "Skipping example file: ${file}"
      continue
    fi
    local target_file="${dest_dir}/${base_name}"

    if [[ -e "$target_file" && "$OVERWRITE" != true ]]; then
      SKIPPED_COUNT=$((SKIPPED_COUNT + 1))
      log_warn "Skipping existing file: ${target_file} (use --overwrite to replace)"
      continue
    fi

    if [[ "$DRY_RUN" == true ]]; then
      COPIED_COUNT=$((COPIED_COUNT + 1))
      log_info "Would copy ${file} -> ${target_file}"
      continue
    fi

    cp "$file" "$target_file"
    COPIED_COUNT=$((COPIED_COUNT + 1))
    log_info "Copied ${file} -> ${target_file}"
  done
  shopt -u nullglob

  if [[ "$files_found" == false ]]; then
    log_warn "No markdown files found in ${source_dir} for ${label}"
  fi
}

process_client() {
  local client_name="$1"
  local skill_dir="$2"
  local subagent_dir="$3"
  local prompt_dir="$4"
  local reason="$5"

  log_info "Checking ${client_name}: ${reason}"
  if [[ -z "$skill_dir" && -z "$subagent_dir" && -z "$prompt_dir" ]]; then
    MISSING_CLIENTS=$((MISSING_CLIENTS + 1))
    log_info "No compatible directories found for ${client_name}"
    return
  fi

  FOUND_CLIENTS=$((FOUND_CLIENTS + 1))
  log_info "Detected ${client_name}"

  if [[ -n "$skill_dir" ]]; then
    copy_collection "${REPO_ROOT}/skills" "$skill_dir" "${client_name} skills"
  else
    log_info "No skills destination for ${client_name}"
  fi

  if [[ -n "$subagent_dir" ]]; then
    copy_collection "${REPO_ROOT}/subagents" "$subagent_dir" "${client_name} subagents"
  else
    log_info "No subagents destination for ${client_name}"
  fi

  if [[ -n "$prompt_dir" ]]; then
    copy_collection "${REPO_ROOT}/prompts" "$prompt_dir" "${client_name} prompts"
  else
    log_info "No prompts destination for ${client_name}"
  fi
}

detect_os() {
  local uname_out
  uname_out="$(uname -s || true)"
  case "$uname_out" in
    Linux*) echo "linux" ;;
    Darwin*) echo "macos" ;;
    MINGW*|MSYS*|CYGWIN*) echo "git-bash-windows" ;;
    *) echo "unknown" ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --overwrite)
      OVERWRITE=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      printf '[ERROR] Unknown argument: %s\n' "$1"
      usage
      exit 1
      ;;
  esac
done

log_info "Starting install script (copy mode only)"
log_warn "Symlink mode is intentionally disabled. Re-run this script when you want to update installed files."
log_info "Repository root: ${REPO_ROOT}"
log_info "Detected platform: $(detect_os)"
log_info "Options: overwrite=${OVERWRITE}, dry-run=${DRY_RUN}"

if [[ ! -d "${REPO_ROOT}/skills" || ! -d "${REPO_ROOT}/subagents" || ! -d "${REPO_ROOT}/prompts" ]]; then
  printf '[ERROR] Expected skills/, subagents/, and prompts/ in repository root.\n'
  exit 1
fi

HOME_DIR="${HOME:-}"
if [[ -z "$HOME_DIR" ]]; then
  printf '[ERROR] HOME is not set. Cannot detect user install directories.\n'
  exit 1
fi

log_info "Using HOME: ${HOME_DIR}"

cursor_global_root="${HOME_DIR}/.cursor"
cursor_project_root="${REPO_ROOT}/.cursor"
claude_root="${HOME_DIR}/.claude"
gemini_root="${HOME_DIR}/.gemini"
copilot_root="${HOME_DIR}/.github/copilot"

cursor_global_skills=""
cursor_global_subagents=""
cursor_global_prompts=""
if [[ -d "${cursor_global_root}" ]]; then
  cursor_global_skills="${cursor_global_root}/skills"
  [[ -d "${cursor_global_root}/subagents" ]] && cursor_global_subagents="${cursor_global_root}/subagents"
  [[ -d "${cursor_global_root}/prompts" ]] && cursor_global_prompts="${cursor_global_root}/prompts"
fi

cursor_project_skills=""
cursor_project_subagents=""
cursor_project_prompts=""
if [[ -d "${cursor_project_root}" ]]; then
  cursor_project_skills="${cursor_project_root}/skills"
  [[ -d "${cursor_project_root}/subagents" ]] && cursor_project_subagents="${cursor_project_root}/subagents"
  [[ -d "${cursor_project_root}/prompts" ]] && cursor_project_prompts="${cursor_project_root}/prompts"
fi

claude_skills=""
claude_subagents=""
claude_prompts=""
if [[ -d "${claude_root}" ]]; then
  [[ -d "${claude_root}/skills" ]] && claude_skills="${claude_root}/skills"
  [[ -d "${claude_root}/subagents" ]] && claude_subagents="${claude_root}/subagents"
  [[ -d "${claude_root}/prompts" ]] && claude_prompts="${claude_root}/prompts"
  [[ -z "$claude_subagents" && -d "${claude_root}/agents" ]] && claude_subagents="${claude_root}/agents"
fi

gemini_skills=""
gemini_subagents=""
gemini_prompts=""
if [[ -d "${gemini_root}" ]]; then
  [[ -d "${gemini_root}/skills" ]] && gemini_skills="${gemini_root}/skills"
  [[ -d "${gemini_root}/subagents" ]] && gemini_subagents="${gemini_root}/subagents"
  [[ -d "${gemini_root}/prompts" ]] && gemini_prompts="${gemini_root}/prompts"
  [[ -z "$gemini_subagents" && -d "${gemini_root}/agents" ]] && gemini_subagents="${gemini_root}/agents"
fi

copilot_skills=""
copilot_subagents=""
copilot_prompts=""
if [[ -d "${copilot_root}" ]]; then
  [[ -d "${copilot_root}/skills" ]] && copilot_skills="${copilot_root}/skills"
  [[ -d "${copilot_root}/subagents" ]] && copilot_subagents="${copilot_root}/subagents"
  [[ -d "${copilot_root}/prompts" ]] && copilot_prompts="${copilot_root}/prompts"
  [[ -z "$copilot_subagents" && -d "${copilot_root}/agents" ]] && copilot_subagents="${copilot_root}/agents"
fi

process_client "Cursor (global)" "$cursor_global_skills" "$cursor_global_subagents" "$cursor_global_prompts" "expected root at ${cursor_global_root}"
process_client "Cursor (project)" "$cursor_project_skills" "$cursor_project_subagents" "$cursor_project_prompts" "expected root at ${cursor_project_root}"
process_client "Claude Code" "$claude_skills" "$claude_subagents" "$claude_prompts" "expected root at ${claude_root}"
process_client "Gemini CLI" "$gemini_skills" "$gemini_subagents" "$gemini_prompts" "expected root at ${gemini_root}"
process_client "Copilot" "$copilot_skills" "$copilot_subagents" "$copilot_prompts" "expected root at ${copilot_root}"

log_info "Install run complete."
log_info "Detected clients: ${FOUND_CLIENTS}"
log_info "Clients without compatible directories: ${MISSING_CLIENTS}"
log_info "Files copied (or would copy in dry-run): ${COPIED_COUNT}"
log_info "Files skipped: ${SKIPPED_COUNT}"
log_info "Warnings: ${WARN_COUNT}"

if [[ "$FOUND_CLIENTS" -eq 0 ]]; then
  log_warn "No supported client directories were detected."
  exit 2
fi
