# BYU-Idaho Brand Style Guide

A reusable plugin for creating and reviewing BYU-Idaho documents, presentations, PDFs, images, infographics, and copy using official public branding guidance.

Current version: **0.2.0**. Use the [published workspace plugin](https://chatgpt.com/plugins/Plugin_577e4a2f4ccc819180d1bc4a6aa1bfe3) where you have access.

## Install from this GitHub marketplace

Repository URL: **https://github.com/davashby/byui-brand-style-guide**

This repository includes a marketplace catalog at [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json). It lists the plugin at the repository root. This is a repository marketplace; it does not mean the plugin has been approved for the universal public Plugins Directory. Client availability and workspace policies determine which installation options you can use.

### ChatGPT workspace import (workspace admin)

1. Open **Admin > Plugins > Add > Import marketplace**.
2. Set **Source** to `https://github.com/davashby/byui-brand-style-guide`.
3. Leave **Path** empty. Set **Branch, tag, or commit** to `main` to receive updates, or choose a full commit SHA for a fixed revision.
4. Select **Import marketplace** and authorize GitHub access if prompted.
5. Review the import results and make **BYU-Idaho Brand Style Guide** available to the intended workspace roles.

Workspace imports normally sync daily. To request the latest changes, use **Admin > Plugins > Marketplaces > Sync now**. Admin settings determine installation and access; repository policy values do not override them. Members install the imported plugin through their workspace's Plugins Directory.

The catalog intentionally has no workspace-specific `pluginId`, so other workspaces can import their own copy. This does not migrate or change the existing private workspace plugin. An admin who wants to migrate that existing plugin to GitHub management should follow the official migration instructions separately.

### Local marketplace (supported desktop clients)

With a current Codex CLI installed, add the repository marketplace:

```sh
codex plugin marketplace add davashby/byui-brand-style-guide --ref main
```

Restart the desktop app, open the **Plugins Directory**, choose the **BYU-Idaho Brand Style Guide** marketplace source, and install the plugin. Start a new chat and try: “Help me create an asset that follows BYU-Idaho's brand guidance.”

To refresh the tracked repository source:

```sh
codex plugin marketplace upgrade byui-brand-style-guide
```

Restart the app so it picks up the refreshed files. The CLI command registers or refreshes the marketplace source; installation happens through the desktop Plugins Directory. This skills-only plugin has no bundled service connection, API key, or sign-in. Some university resources linked by the guide require separate university access. Creating files also requires the host's relevant document, presentation, image, or PDF capabilities.

Official workflow documentation: [repository marketplaces](https://developers.openai.com/plugins/build/plugins#build-your-own-curated-plugin-list) and [workspace GitHub import and sync](https://learn.chatgpt.com/docs/enterprise/plugin-management).

## Included resources

- A short core skill with references loaded by task, covering brand rules, writing, channels, assets, and output production.
- Four unmodified original PNG logo tiles from the official logo page, plus the four supplied WebP tiles.
- The supplied email signature DOCX.
- Blue and white POTX templates **with a 25 YEARS footer**. These require confirmed current anniversary authorization and are not generic evergreen templates.
- Asset provenance/hashes and a compact PowerPoint layout index.
- Links to official generic office/PPT templates, department/vector logos, licensed font access, photography, and LinkedIn banners. These linked resources are not bundled and may require sign-in.

This plugin is a practical summary, not university approval. Current [BYU-Idaho branding guidance](https://www.byui.edu/branding/) is authoritative. The host supplies document/presentation/image tools; this package does not bundle Office, a renderer, or licensed fonts. It identifies missing capabilities or restricted assets rather than claiming an unavailable output is complete.

## Validate and package

Python 3.10 or newer is sufficient for package validation, packaging, and the guarded template-copy helper:

```sh
python3 scripts/validate_plugin.py
python3 -m unittest discover -s tests -v
python3 scripts/package_plugin.py
```

The optional DOCX compatibility test uses `python-docx` when available in the host's artifact runtime. Tests otherwise run with the standard library. The package builder validates first and creates a reproducible ZIP at `dist/byui-brand-guide-plugin.zip`. It includes only plugin components, excludes build/cache files, and rejects symlinks. Root maintenance scripts, tests, audit documents, and generated archives are not shipped to the plugin.

## PowerPoint working copies

The original templates remain intact. A helper can change only the main Office MIME type to make a working PPTX while preserving all other parts, including charts and workbooks:

```sh
python3 skills/byui-brand-guide/scripts/prepare_pptx.py --variant blue --output /absolute/path/working.pptx --anniversary-approved
```

Use that flag only after independently confirming current anniversary authorization. It does not grant approval. The working copy still includes examples and anniversary artwork, and subsequent edits/exports need validation. For general official presentations, obtain the current approved generic template from the university's resource library.

## Maintain and release

- Edit the core skill sparingly; put conditional detail in references.
- When assets change, update their catalog hashes/provenance and the template layout index, then validate.
- Synchronize versions, identity, and interface metadata in both manifests; preserve the existing package name `byui-brand-guide` and plugin ID.
- Build/test a new package and update the existing workspace plugin through Plugin Creator. GitHub pushes do not automatically publish plugin releases.
- For repository marketplace users, push reviewed changes to `main`; workspace imports sync from that branch and local users refresh their marketplace source. Bump the plugin version when plugin content changes. Repository-only catalog/documentation changes do not change the plugin version.
- Review [the original audit](docs/audit-2026-10-19.md), [release validation](docs/validation-0.2.0.md), and [changelog](CHANGELOG.md).

Bundled logos/templates retain their original ownership and usage restrictions. This repository does not grant permission to alter or redistribute university marks. Linked resources retain their own access requirements.

Maintained by David Ashby. This listing does not claim university endorsement or grant university approval for assets created with the plugin.
