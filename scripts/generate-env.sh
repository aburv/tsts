#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "$0")/.." && pwd)
template_dir="$repo_root/envs"
source_env="$repo_root/.env"
output_dir="$repo_root/app/server"
selected_template=""

usage() {
    printf 'Usage: %s --server|--db|--auth|--redis [output-directory]\n' "$0"
    printf '\nRead values from ./.env using source keys declared in the selected template.\n'
    printf 'The default output directory is app/server.\n'
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --server|--db|--auth|--redis)
            if [[ -n "$selected_template" ]]; then
                printf 'Choose only one template selector.\n' >&2
                usage >&2
                exit 1
            fi
            selected_template="${1#--}.env"
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        --*)
            printf 'Unknown option: %s\n' "$1" >&2
            usage >&2
            exit 1
            ;;
        *)
            output_dir=$1
            shift
            ;;
    esac
done

if [[ -z "$selected_template" ]]; then
    printf 'A template selector is required.\n' >&2
    usage >&2
    exit 1
fi

if [[ ! -f "$source_env" ]]; then
    printf 'Source environment file not found: %s\n' "$source_env" >&2
    exit 1
fi
template_file="$template_dir/$selected_template"
if [[ ! -f "$template_file" ]]; then
    printf 'Template file not found: %s\n' "$template_file" >&2
    exit 1
fi

mkdir -p "$output_dir"

output_file="$output_dir/$(basename "$template_file")"
temporary_file=$(mktemp "${output_file}.tmp.XXXXXX")
missing_keys=()

while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ "$line" =~ ^([A-Za-z_][A-Za-z0-9_]*)=([A-Za-z_][A-Za-z0-9_]*)$ ]]; then
        key=${BASH_REMATCH[1]}
        source_key=${BASH_REMATCH[2]}
        if value=$(awk -F= -v key="$source_key" '$1 == key { print substr($0, index($0, "=") + 1); found=1; exit } END { if (!found) exit 1 }' "$source_env"); then
            printf '%s=%s\n' "$key" "$value" >> "$temporary_file"
        else
            missing_keys+=("$key")
            printf '%s=\n' "$key" >> "$temporary_file"
        fi
    fi
done < "$template_file"

if [[ ${#missing_keys[@]} -gt 0 ]]; then
    printf '%s: missing keys in .env, generated as blank: %s\n' \
        "$(basename "$template_file")" "${missing_keys[*]}" >&2
fi

chmod 600 "$temporary_file"
mv "$temporary_file" "$output_file"
printf 'Generated %s\n' "$output_file"