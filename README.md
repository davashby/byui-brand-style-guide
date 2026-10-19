# BYU-Idaho Brand Style Guide

A reusable plugin for planning, creating, and reviewing BYU-Idaho visual and written assets using the university’s public branding guidance.

Current plugin version: **0.1.11**.

## Contents

- Brand guidance skill and references covering colors, typography, logos, photography, illustration, writing, and campus communication channels.
- Four supplied university logo tiles.
- Blue and white PowerPoint templates (`.potx`).
- A supplied email signature template (`.docx`).
- A link to the university’s LinkedIn banner collection.

## Use

Use the [published workspace plugin](https://chatgpt.com/plugins/Plugin_577e4a2f4ccc819180d1bc4a6aa1bfe3) where you have access. This repository stores the editable plugin source and bundled assets.

The plugin is a practical summary, not an official university publication or approval. Current [BYU-Idaho branding pages](https://www.byui.edu/branding/) are the authority. The references record how claims from the supplied institutional brand architecture document were reconciled with those pages.

## Package

From the repository root, run:

```sh
python3 scripts/package_plugin.py
```

The ZIP is written to `dist/byui-brand-guide-plugin.zip` and contains a single plugin directory. Generated archives are excluded from Git.

## Maintain

Edit `skills/byui-brand-guide/SKILL.md` and its references as guidance changes. Keep the versions in `plugin.json` and `.codex-plugin/plugin.json` aligned, and preserve the package name `byui-brand-guide` when updating the existing plugin. Its visible title is configured in both manifests.

Publishing to GitHub does not update the workspace plugin automatically. Publish a new package through the existing Plugin Creator workflow when a release is ready.

## Assets and access

Bundled logos and templates retain their original ownership and usage restrictions. This repository does not grant permission to redistribute or alter university marks. Linked Drive resources retain their own access requirements.
