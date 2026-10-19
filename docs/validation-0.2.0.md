# Release validation 0.2.0

Checked 2026-10-19. This release implements the recommendations in the version 0.1.11 audit.

## Implemented changes

| Audit issue | Resolution |
|---|---|
| Invalid portable manifest fields | Moved the six host presentation fields into `extensions.com.openai.interface`, following the official plugin package guide; compatibility metadata matches. |
| WebP rejected by DOCX | Added four unmodified original 2500 × 2500 PNG tiles exposed by the official logo page, with exact download provenance and hashes. Kept the original supplied WebPs. |
| Anniversary templates recommended generically | Added campaign status to the asset catalog, core skill, asset guide, and output recipe. Current authorization is required; no anniversary end date is invented. |
| Native charts lost by an importer/exporter | Added a guarded working-copy helper that changes only the main Office MIME type and preserves all other Office part bytes. Saved-output native chart/editability checks are required for subsequent edits. |
| Stale society source/platform | Replaced current-use I-Belong instructions with myBYUI Groups, current society policy and department sources. Historical assertions are qualified in the secondary-document reference. |
| Missing production instructions | Added DOCX, PPTX, PDF, image and infographic recipes covering actual file creation, export, host capabilities, and material limitations. |
| Missing accessibility/font checks | Added semantic structure, alt descriptions, contrast, reading order, PDF tagging limitations, font access, and actual retained-font checks. |
| Missing channel coverage | Added task-specific references for social review/training, paid ads, email, myBYUI, texts, merchandise, IBC, outside organizations, and current DSN details. |
| Paths, naming, dark color | Correct paths are explicit in references/catalog; skill title matches the display title; dark icon background uses approved black. |
| Redundant instruction/context loading | Core reduced from 2,265 to 648 words (about 71%); detailed references are conditional, template layout records are shared, and evidence is reused within a task. No measured generation-speed claim. |
| Weak packaging checks | Added vendored official schema validation for its used keywords, asset hashes, Office relationships, campaign restrictions, local links, and reproducible archive validation. |

## Verification performed

- Seven automated release tests pass in the bundled artifact Python runtime, including all four PNG insertions into DOCX.
- Both original POTX files remain unchanged. Guarded working copies preserve 32 slides, 27 layouts, seven native chart parts, workbook parts, and all original media; only the template-to-presentation MIME declaration changes.
- The helper refuses conversion without the campaign-confirmation flag and refuses an existing output file. The flag represents a prior approval decision; it does not grant authorization.
- A representative editable DOCX containing all four original PNGs was rendered to a one-page PDF and PNG preview. All four logos were visually inspected and remain readable without cropping/background changes.
- Catalog hashes, layout part coverage, Office internal relationship targets, icon references, relative Markdown downloads, synchronized manifests, source identity, and original starter prompts were checked.
- The release ZIP is built reproducibly, tested for ZIP integrity, and compared with source bytes. Build caches, maintenance scripts, tests, and audit documents are excluded.

## Material limitations

- No approved transparent/vector master or current generic office/PPT template is fabricated. Official linked resources may require university access. Their latest protected SharePoint revisions were not verified.
- Licensed Acumin/Minion font files and Office/rendering software are not bundled. The host must provide authoring capabilities and actual font access.
- The PowerPoint helper preserves source parts; it is not a general slide editor. Later editing/export still requires native-chart and visual checks. One tested LibreOffice route omitted an EMF footer, so that route alone does not certify presentation fidelity.
- The private DOCX/PDF fixture checks raster/Office interoperability and visual rendering, not full PDF accessibility. Production instructions require checking actual accessibility features or identifying exporter limitations.
- Host model instruction-following, Outlook behavior, and every possible output/application combination have not been exhaustively tested. The plugin does not certify final university approval.

Sources: [BYU-Idaho official logo resources](https://www.byui.edu/branding/logos/official), [template resources](https://www.byui.edu/branding/office-templates), [official OpenAI package guide](https://developers.openai.com/plugins/build/plugins), and [Agent Plugins 1.0 schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json). The vendored schema is the exact schema fetched during the audit.
