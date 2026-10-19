# Producing and validating outputs

Use the host's relevant artifact tools/skills when available. These are production practices supporting the university's [accessibility guidance](https://www.byui.edu/accessibility-services/web-accessibility-guidelines), not invented university layout specifications. Only read the requested format's section and common checks. No Office renderer or licensed fonts are bundled with this plugin.

## Common checks

Identify the requested deliverable and editability. Respect an explicit format, page/slide count, dimensions, destination, and supplied template. Use cataloged assets from the plugin root; do not assume the current working directory is the plugin directory. Check campaign status and actual font availability before layout. Reuse validated content/styles when making several exports.

Use semantic headings/lists, descriptive links, table headers, alt descriptions, and logical reading order. Check foreground/background contrast and distinguish categories with labels or patterns as well as color. Keep data, captions, sources, and relationships accurate. For a substantial infographic, supply an accessible text description. When a tool cannot preserve tags, native charts, or reading order, identify the specific loss rather than labeling the output fully accessible/editable.

Inspect the saved output, not only an in-memory preview: file opens, actual dimensions/count, all required content, fonts, image proportions, logo size/clear space, cropping, clipping, and unresolved placeholders. Render relevant final pages/slides and inspect them. Check all changed/shared-layout-affected pages and follow the host's full-render requirements. Validation checklists stay outside the user's content.

## DOCX

Use a supplied approved office/letterhead template when available. The bundled signature file is only a signature template, not a generic letterhead. For an official stationery request, retrieve the applicable approved template or ask for it if access is unavailable. An ordinary document may use a clearly identified draft layout with standard document design choices; do not claim invented margins/header arrangements are university policy or call it official letterhead.

Build editable paragraphs, heading styles, lists, tables, and fields. Use the original PNG logo tiles in `assets/logos/`; WebP is unsupported by some DOCX libraries. Keep the image background and aspect ratio, size by the visible mark, and provide alt text where appropriate. Apply the correct font category and verify actual fonts. Render the result and inspect pagination, table wrapping, headings, and images. Do not silently substitute a PDF when DOCX was requested.

## PPTX / presentations

1. Check `assets/catalog.json` and `assets/powerpoint-layouts.json` before opening a template. Both supplied POTX files have a 25 YEARS master footer and need confirmed current anniversary authorization. For a general official presentation, obtain an approved current generic template from the official resource; if unavailable, report that dependency. Do not invent an official generic template or remove/reconstruct the restricted mark.
2. Inspect the selected template's relevant slides and layouts. Preserve dimensions, masters, backgrounds, branding, spacing, and appropriate fonts. The supplied templates are 16:9 with 32 example/instruction slides and 27 layouts; this is not a requirement to deliver 32 slides. Remove instruction slides, unused examples, and dummy data as content is adapted. Deliver the requested count.
3. Create a working PPTX, preserving original files. For the bundled anniversary templates, the packaged `scripts/prepare_pptx.py` can make a byte-preserving working copy of Office parts after explicit campaign confirmation:

   `python3 <skill-directory>/scripts/prepare_pptx.py --variant blue --output <absolute-output.pptx> --anniversary-approved`

   The flag records a prior authorization decision; running the script does not grant university approval. The copy still contains all example slides and anniversary artwork and needs subsequent editing/validation.
4. Preserve native editable charts/tables and their data when requested. The source templates each contain seven native charts; this is source metadata, not a requirement that every final deck contain seven charts. A tested general importer/exporter flattened those charts. Use a route that preserves retained chart/workbook parts or recreate requested charts natively. Verify native parts/editability in the saved PPTX; a good render does not prove it. Do not use a known lossy round trip as the default without repair.
5. Check actual font use in theme text, charts, and retained layouts. Main placeholders use Arial; the templates also declare Calibri and a legacy NewsGoth chart font, without embedded fonts. Apply context-specific current font guidance and report substitutions. Do not replace approved template typography blindly or claim every inherited style is current.
6. Save as PPTX rather than returning only the POTX source. Render and compare relevant final slides with the approved source; check logo/footer rendering across the chosen export route. EMF anniversary footers disappeared in one tested LibreOffice render, so that route alone cannot certify branding fidelity.

## PDF

Export from a validated editable source to keep copy and layout consistent. Preserve selectable text, links, appropriate font embedding, and images at adequate resolution. For accessible delivery, verify structure tags, headings/bookmarks, alt text, and reading order where the exporter supports them; PDF appearance alone is not accessibility proof. If tagging is unavailable, disclose that limitation and retain/provide the accessible source as appropriate.

For print, use printer-approved color/output settings and requested trim/bleed/stock; do not assert universal BYU-Idaho print specifications that the source does not state. Inspect final page size, pagination, fonts, links, clipping, and legibility. A scanned/image-only PDF requires OCR and accessibility work before a claim of accessible text.

## Images and graphics

Select dimensions and format from the intended channel, not from the logo tile. Use RGB/HEX for screen work. DSN requires JPEG at 1920 × 1080 and does not require a logo. PNG is suitable for lossless graphics when the destination permits it; use other formats only when accepted by the intended tool/channel.

Use AI for permitted artwork/concept exploration; compose accurate final typography and the exact approved logo using deterministic layout. Never generate official marks. Use an approved vector/transparent master when required; do not create one by redrawing, background removal, or enlargement. Verify visible logo size, clear space, contrast, wording, and resolution in the final export. Requesting a design prompt does not require rendering an artifact.

## Infographics and data visuals

Verify every number, unit, label, comparison, and source. Use appropriate chart forms with readable labels, direct explanations, and alternatives to color-only encoding. Use native editable charts/tables in DOCX/PPTX or a suitable editable source when requested, then export PNG/PDF as needed. Avoid giving an image-generation model responsibility for exact chart data or final labels. Provide alt text or an accompanying text equivalent. Apply source-specific palette rules without sacrificing readable contrast; label any production limitation.
