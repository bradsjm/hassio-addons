#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
addon_dir="${repo_root}/addon-mcpx"
upstream_dir=${UPSTREAM_DIR:-}

require() {
  local pattern=$1
  local file=$2
  if ! grep -Fq -- "${pattern}" "${file}"; then
    printf 'Missing %s in %s\n' "${pattern}" "${file}" >&2
    exit 1
  fi
}

bash -n "${addon_dir}/rootfs/etc/services.d/mcpx/run"

require 'version: "0.2.0"' "${addon_dir}/config.yaml"
require 'type: addon_config' "${addon_dir}/config.yaml"
require 'path: /config' "${addon_dir}/config.yaml"
require 'docker_api: true' "${addon_dir}/config.yaml"
require 'enable_docker_mcp: false' "${addon_dir}/config.yaml"
require 'image: "docker.io/bradsjm/addon-mcpx"' "${addon_dir}/config.yaml"
require 'APP_CONFIG_PATH="${app_config_path}"' "${addon_dir}/rootfs/etc/services.d/mcpx/run"
require 'SERVERS_CONFIG_PATH="${servers_config_path}"' "${addon_dir}/rootfs/etc/services.d/mcpx/run"
require 'ENABLE_STDIO_MCP_SERVERS=true' "${addon_dir}/rootfs/etc/services.d/mcpx/run"
require 'header: x-lunar-api-key' "${addon_dir}/rootfs/etc/services.d/mcpx/run"
require 'cd "${data_dir}"' "${addon_dir}/rootfs/etc/services.d/mcpx/run"
require 'su-exec lunar docker version' "${addon_dir}/rootfs/etc/services.d/mcpx/run"
require 'x-lunar-api-key' "${addon_dir}/patches/lunar-e4a70047221fa015973d78858b7bdfd7ca321b32.patch"
require 'ipAllowed' "${addon_dir}/patches/lunar-e4a70047221fa015973d78858b7bdfd7ca321b32.patch"
require 'origin: env.CORS_ORIGINS || true' "${addon_dir}/patches/lunar-e4a70047221fa015973d78858b7bdfd7ca321b32.patch"
require 'REGISTRY_PREFIX: docker.io/bradsjm' "${repo_root}/.github/workflows/addon-mcpx.yml"
require 'container-registry: docker.io' "${repo_root}/.github/workflows/addon-mcpx.yml"

if grep -Fq 'chown -R' "${addon_dir}/rootfs/etc/services.d/mcpx/run"; then
  printf 'The service must not recursively chown /data.\n' >&2
  exit 1
fi

if [[ -n "${upstream_dir}" ]]; then
  patch --dry-run --fuzz=0 --batch --forward -p1 -d "${upstream_dir}" \
    < "${addon_dir}/patches/lunar-e4a70047221fa015973d78858b7bdfd7ca321b32.patch"
fi

printf 'MCPX static verification passed.\n'
