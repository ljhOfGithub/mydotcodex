#!/bin/sh
set -eu

if [ "$#" -eq 0 ]; then
  printf '%s\n' "usage: run-wechat-direct.sh <command> [args...]" >&2
  exit 64
fi

clash_socket="${WECHAT_CLASH_SOCKET:-/tmp/verge/verge-mihomo.sock}"
skip_clash="${WECHAT_SKIP_CLASH:-0}"
previous_mode=""
proxy_changed=0

restore_proxy_mode() {
  if [ "$proxy_changed" -eq 1 ]; then
    curl --silent --show-error --fail \
      --unix-socket "$clash_socket" \
      -X PATCH \
      -H "Content-Type: application/json" \
      -d "{\"mode\":\"$previous_mode\"}" \
      http://localhost/configs >/dev/null
    proxy_changed=0
  fi
}

trap restore_proxy_mode EXIT HUP INT TERM

if [ "$skip_clash" != "1" ] && [ -S "$clash_socket" ]; then
  previous_mode="$(
    curl --silent --show-error --fail \
      --unix-socket "$clash_socket" \
      http://localhost/configs |
      jq -er '.mode'
  )"
  if [ "$previous_mode" != "rule" ]; then
    curl --silent --show-error --fail \
      --unix-socket "$clash_socket" \
      -X PATCH \
      -H "Content-Type: application/json" \
      -d '{"mode":"rule"}' \
      http://localhost/configs >/dev/null
    proxy_changed=1
  fi
fi

set +e
env \
  -u HTTP_PROXY \
  -u HTTPS_PROXY \
  -u ALL_PROXY \
  -u NO_PROXY \
  -u http_proxy \
  -u https_proxy \
  -u all_proxy \
  -u no_proxy \
  "$@"
command_status=$?
set -e

restore_proxy_mode
trap - EXIT HUP INT TERM
exit "$command_status"
