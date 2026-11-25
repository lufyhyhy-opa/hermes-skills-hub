#!/usr/bin/env bash
# ==============================================================================
# sync-hermes-brain.sh — Đồng Bộ Bộ Nhớ & Kỹ Năng Lõi Xuyên Suốt 19 Agent Hermes
# Tự động tìm bản MEMORY.md / USER.md mới nhất (giữa root và các profile) rồi
# đồng bộ đồng loạt cho toàn bộ hệ sinh thái Agent của Anh Huy.
# ==============================================================================
set -euo pipefail

HERMES_ROOT="${HOME}/.hermes"
ROOT_MEM_DIR="${HERMES_ROOT}/memories"
PROFILES_DIR="${HERMES_ROOT}/profiles"

mkdir -p "${ROOT_MEM_DIR}"

# 1. Tìm file USER.md và MEMORY.md được cập nhật gần nhất (nếu Anh Huy vừa dạy ở agent-00 hoặc default)
for fname in USER.md MEMORY.md; do
  newest_file="${ROOT_MEM_DIR}/${fname}"
  for prof_mem in "${PROFILES_DIR}"/*/memories/"${fname}"; do
    if [[ -f "${prof_mem}" && "${prof_mem}" -nt "${newest_file}" ]]; then
      newest_file="${prof_mem}"
    fi
  done

  if [[ -f "${newest_file}" && "${newest_file}" != "${ROOT_MEM_DIR}/${fname}" ]]; then
    cp -f "${newest_file}" "${ROOT_MEM_DIR}/${fname}"
  fi

  # Phân phối từ Root xuống toàn bộ 19 Agent Profiles
  if [[ -f "${ROOT_MEM_DIR}/${fname}" ]]; then
    for prof_dir in "${PROFILES_DIR}"/*/; do
      [[ -d "${prof_dir}" ]] || continue
      prof_name="$(basename "${prof_dir}")"
      [[ "${prof_name}" == .* ]] && continue
      mkdir -p "${prof_dir}/memories"
      cp -f "${ROOT_MEM_DIR}/${fname}" "${prof_dir}/memories/${fname}"
    done
  fi
done

# 2. Đồng bộ các Skill lõi sang shared-skills và toàn bộ 19 Agent Profiles
mkdir -p "${HERMES_ROOT}/shared-skills/lintech-os/huy-intent-and-gold-standards"
mkdir -p "${HERMES_ROOT}/shared-skills/lintech-os/autonomous-slide-council"
mkdir -p "${HERMES_ROOT}/shared-skills/lintech-os/telegram-hitl-gate"
mkdir -p "${HERMES_ROOT}/shared-skills/lintech-os/harness-engineering-trust-pyramid"
mkdir -p "${HERMES_ROOT}/skills/software-development/harness-engineering-trust-pyramid"
mkdir -p "${HERMES_ROOT}/shared-skills/lintech-os/claude-agentic-stack-and-harnesses"
mkdir -p "${HERMES_ROOT}/skills/software-development/claude-agentic-stack-and-harnesses"

if [[ -f "${HERMES_ROOT}/skills/lintech-os/huy-intent-and-gold-standards/SKILL.md" ]]; then
  cp -f "${HERMES_ROOT}/skills/lintech-os/huy-intent-and-gold-standards/SKILL.md" \
        "${HERMES_ROOT}/shared-skills/lintech-os/huy-intent-and-gold-standards/SKILL.md"
fi

if [[ -f "${HERMES_ROOT}/skills/lintech-os/autonomous-slide-council/SKILL.md" ]]; then
  cp -f "${HERMES_ROOT}/skills/lintech-os/autonomous-slide-council/SKILL.md" \
        "${HERMES_ROOT}/shared-skills/lintech-os/autonomous-slide-council/SKILL.md"
fi

if [[ -f "${HERMES_ROOT}/skills/lintech-os/telegram-hitl-gate/SKILL.md" ]]; then
  cp -f "${HERMES_ROOT}/skills/lintech-os/telegram-hitl-gate/SKILL.md" \
        "${HERMES_ROOT}/shared-skills/lintech-os/telegram-hitl-gate/SKILL.md"
fi

if [[ -f "${HERMES_ROOT}/skills/lintech-os/harness-engineering-trust-pyramid/SKILL.md" ]]; then
  cp -f "${HERMES_ROOT}/skills/lintech-os/harness-engineering-trust-pyramid/SKILL.md" \
        "${HERMES_ROOT}/shared-skills/lintech-os/harness-engineering-trust-pyramid/SKILL.md"
  cp -f "${HERMES_ROOT}/skills/lintech-os/harness-engineering-trust-pyramid/SKILL.md" \
        "${HERMES_ROOT}/skills/software-development/harness-engineering-trust-pyramid/SKILL.md"
fi

if [[ -f "${HERMES_ROOT}/skills/lintech-os/claude-agentic-stack-and-harnesses/SKILL.md" ]]; then
  cp -f "${HERMES_ROOT}/skills/lintech-os/claude-agentic-stack-and-harnesses/SKILL.md" \
        "${HERMES_ROOT}/shared-skills/lintech-os/claude-agentic-stack-and-harnesses/SKILL.md"
  cp -f "${HERMES_ROOT}/skills/lintech-os/claude-agentic-stack-and-harnesses/SKILL.md" \
        "${HERMES_ROOT}/skills/software-development/claude-agentic-stack-and-harnesses/SKILL.md"
fi

for prof_dir in "${PROFILES_DIR}"/*/; do
  [[ -d "${prof_dir}" ]] || continue
  prof_name="$(basename "${prof_dir}")"
  [[ "${prof_name}" == .* ]] && continue

  # Đồng bộ huy-intent-and-gold-standards cho mọi Agent
  mkdir -p "${prof_dir}/skills/lintech-os/huy-intent-and-gold-standards"
  cp -f "${HERMES_ROOT}/skills/lintech-os/huy-intent-and-gold-standards/SKILL.md" \
        "${prof_dir}/skills/lintech-os/huy-intent-and-gold-standards/SKILL.md"

  # Đồng bộ harness-engineering-trust-pyramid cho mọi Agent
  if [[ -f "${HERMES_ROOT}/skills/lintech-os/harness-engineering-trust-pyramid/SKILL.md" ]]; then
    mkdir -p "${prof_dir}/skills/lintech-os/harness-engineering-trust-pyramid"
    cp -f "${HERMES_ROOT}/skills/lintech-os/harness-engineering-trust-pyramid/SKILL.md" \
          "${prof_dir}/skills/lintech-os/harness-engineering-trust-pyramid/SKILL.md"
  fi

  # Đồng bộ claude-agentic-stack-and-harnesses cho mọi Agent
  if [[ -f "${HERMES_ROOT}/skills/lintech-os/claude-agentic-stack-and-harnesses/SKILL.md" ]]; then
    mkdir -p "${prof_dir}/skills/lintech-os/claude-agentic-stack-and-harnesses"
    cp -f "${HERMES_ROOT}/skills/lintech-os/claude-agentic-stack-and-harnesses/SKILL.md" \
          "${prof_dir}/skills/lintech-os/claude-agentic-stack-and-harnesses/SKILL.md"
  fi

  # Đồng bộ opa-knowledge nếu profile có cài đặt
  if [[ -d "${prof_dir}/skills/opa-knowledge" && -f "${HERMES_ROOT}/skills/opa-knowledge/SKILL.md" ]]; then
    cp -f "${HERMES_ROOT}/skills/opa-knowledge/SKILL.md" \
          "${prof_dir}/skills/opa-knowledge/SKILL.md"
  fi

  # Đồng bộ telegram-hitl-gate nếu profile có cài đặt
  if [[ -d "${prof_dir}/skills/lintech-os/telegram-hitl-gate" && -f "${HERMES_ROOT}/skills/lintech-os/telegram-hitl-gate/SKILL.md" ]]; then
    cp -f "${HERMES_ROOT}/skills/lintech-os/telegram-hitl-gate/SKILL.md" \
          "${prof_dir}/skills/lintech-os/telegram-hitl-gate/SKILL.md"
  fi
  # Đồng bộ comfyui-family-filmmaker & comfyui-workflow-skill cho mọi Agent
  if [[ -f "${HERMES_ROOT}/skills/media/comfyui-family-filmmaker/SKILL.md" ]]; then
    mkdir -p "${prof_dir}/skills/media/comfyui-family-filmmaker"
    cp -f "${HERMES_ROOT}/skills/media/comfyui-family-filmmaker/SKILL.md" \
          "${prof_dir}/skills/media/comfyui-family-filmmaker/SKILL.md"
  fi
  if [[ -d "${HERMES_ROOT}/skills/media/comfyui-workflow-skill" ]]; then
    if [[ ! -d "${prof_dir}/skills/media/comfyui-workflow-skill" || -L "${prof_dir}/skills/media/comfyui-workflow-skill" ]]; then
      ln -sfn "${HERMES_ROOT}/skills/media/comfyui-workflow-skill" \
              "${prof_dir}/skills/media/comfyui-workflow-skill" || true
    fi
  fi
done

echo "[SYNC-HERMES-BRAIN] Đã đồng bộ USER.md, MEMORY.md và các Skill lõi cho toàn bộ 19 Agent Profiles!"
