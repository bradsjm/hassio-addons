#!/usr/bin/with-contenv bashio

wait_for_json_api() {
    local attempt

    for attempt in $(seq 1 15); do
        if ! kill -0 "${hyperion_pid}" 2>/dev/null; then
            return 1
        fi

        if { exec 3<>/dev/tcp/127.0.0.1/19444; } 2>/dev/null; then
            return 0
        fi

        sleep 1
    done

    return 1
}

close_json_api() {
    exec 3>&- 2>/dev/null || true
    exec 3<&- 2>/dev/null || true
}

send_authorize_request() {
    local subcommand="$1"
    local request

    case "${subcommand}" in
        newPasswordRequired)
            request=$(jq -cn '{command: "authorize", subcommand: "newPasswordRequired"}')
            ;;
        login)
            request=$(jq -cn --arg password "$2" '{command: "authorize", subcommand: "login", password: $password}')
            ;;
        newPassword)
            request=$(jq -cn --arg password "$2" --arg new_password "$3" \
                '{command: "authorize", subcommand: "newPassword", password: $password, newPassword: $new_password}')
            ;;
        *)
            return 1
            ;;
    esac

    if ! printf '%s\n' "${request}" >&3; then
        return 1
    fi

    if ! IFS= read -r -t 5 api_response <&3; then
        return 1
    fi

    jq -e . >/dev/null <<< "${api_response}"
}

api_response_succeeded() {
    jq -e '.success == true' >/dev/null <<< "${api_response}"
}

bootstrap_admin_password() {
    local desired_password
    local new_password_required

    if ! bashio::config.has_value 'admin_password'; then
        return 0
    fi

    desired_password=$(bashio::config 'admin_password')
    if [[ ${#desired_password} -lt 8 ]]; then
        bashio::log.error "Configured admin password must contain at least 8 characters; skipping password bootstrap"
        return 0
    fi

    if ! wait_for_json_api; then
        bashio::log.warning "Hyperion JSON API did not become ready for password bootstrap; Hyperion will continue running"
        return 0
    fi

    if ! send_authorize_request newPasswordRequired || \
        ! new_password_required=$(jq -er 'if .success == true and (.info.newPasswordRequired | type == "boolean") then if .info.newPasswordRequired then "true" else "false" end else empty end' <<< "${api_response}"); then
        bashio::log.warning "Could not determine whether Hyperion requires an initial admin password; skipping password bootstrap"
        close_json_api
        return 0
    fi

    if [[ "${new_password_required}" == "true" ]]; then
        if ! send_authorize_request login 'hyperion' || ! api_response_succeeded; then
            bashio::log.warning "Could not authenticate Hyperion's initial admin password; skipping password bootstrap"
        elif ! send_authorize_request newPassword 'hyperion' "${desired_password}" || ! api_response_succeeded; then
            bashio::log.warning "Could not set Hyperion's initial admin password; skipping password bootstrap"
        else
            bashio::log.info "Configured Hyperion admin password on initial startup"
        fi
    elif [[ "${new_password_required}" == "false" ]]; then
        if send_authorize_request login "${desired_password}" && api_response_succeeded; then
            bashio::log.info "Configured Hyperion admin password is already active"
        else
            bashio::log.warning "Configured admin password does not match Hyperion; refusing to overwrite an existing password"
        fi
    else
        bashio::log.warning "Hyperion returned an invalid initial-password status; skipping password bootstrap"
    fi

    close_json_api
}

forward_signal() {
    local signal="$1"
    local status=0

    if kill -0 "${hyperion_pid}" 2>/dev/null; then
        kill -s "${signal}" "${hyperion_pid}" 2>/dev/null || true
        wait "${hyperion_pid}" || status=$?
    fi

    trap - TERM INT
    exit "${status}"
}

mkdir -p /config/hyperion
/usr/bin/hyperiond -d -u /config/hyperion &
hyperion_pid=$!

trap 'forward_signal TERM' TERM
trap 'forward_signal INT' INT

bootstrap_admin_password

if wait "${hyperion_pid}"; then
    exit 0
else
    exit $?
fi
