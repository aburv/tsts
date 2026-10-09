"""Shared in-memory event store for local development."""

events: dict[str, dict[str, list[str]]] = {}