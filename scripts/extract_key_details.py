"""
Extract key formatting details from the raw JSON analysis for the final documentation.
Focus on: colors, fonts, table structures, cell content patterns.
"""
import json

with open("/Users/qusaiabushanap/dev/storyboard/docs/template_analysis_raw.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

for template_name, analysis in data.items():
    print(f"\n{'='*80}")
    print(f"TEMPLATE: {template_name}")
    print(f"{'='*80}")

    # Page layout
    sec = analysis['sections'][0]
    print(f"\nPAGE: {sec['page_width_cm']}cm x {sec['page_height_cm']}cm ({sec['orientation']})")
    print(f"MARGINS: T={sec['margin_top_cm']} B={sec['margin_bottom_cm']} L={sec['margin_left_cm']} R={sec['margin_right_cm']} cm")

    # Collect all unique colors and fonts
    colors = set()
    fonts = set()
    font_sizes = set()

    def extract_from_runs(runs):
        for run in runs:
            if run.get('font_color'):
                colors.add(f"#{run['font_color']}")
            if run.get('font_name'):
                fonts.add(run['font_name'])
            if run.get('cs_font'):
                fonts.add(run['cs_font'])
            if run.get('ascii_font'):
                fonts.add(run['ascii_font'])
            if run.get('font_size_pt'):
                font_sizes.add(run['font_size_pt'])
            if run.get('cs_font_size_pt'):
                font_sizes.add(run['cs_font_size_pt'])

    def extract_from_paragraphs(paras):
        for para in paras:
            extract_from_runs(para.get('runs', []))

    # Extract from body paragraphs
    extract_from_paragraphs(analysis.get('body_paragraphs', []))

    # Extract from header/footer
    for sec in analysis['sections']:
        extract_from_paragraphs(sec.get('header_paragraphs', []))
        extract_from_paragraphs(sec.get('footer_paragraphs', []))

    # Tables
    for table in analysis['tables']:
        print(f"\nTABLE {table['table_index']}: {table['row_count']} rows x {table['col_count']} cols")
        print(f"  BiDi (RTL): {table.get('bidi_visual')}")
        print(f"  Width: {table.get('table_width')}")
        print(f"  Grid columns (cm): {table.get('grid_columns_cm')}")

        if table.get('table_borders'):
            print(f"  Table borders:")
            for side, border in table['table_borders'].items():
                print(f"    {side}: val={border.get('val')} sz={border.get('sz')} color={border.get('color')}")

        for row in table['rows']:
            row_idx = row['row_index']
            for cell in row['cells']:
                cell_text = cell['text'][:60] if cell['text'] else '(empty)'
                shading = cell.get('shading')
                shading_str = f"fill=#{shading['fill']}" if shading and shading.get('fill') and shading['fill'] != 'auto' else ''
                merge = cell.get('merge_info')
                merge_str = f"merge={merge}" if merge else ''
                width = cell.get('width')
                width_str = f"w={width['width']}({width['type']})" if width else ''
                valign = cell.get('vertical_alignment', '')

                if shading and shading.get('fill') and shading['fill'] != 'auto':
                    colors.add(f"#{shading['fill']}")

                # Cell formatting
                for para in cell.get('paragraphs', []):
                    extract_from_runs(para.get('runs', []))

                print(f"  [{row_idx},{cell['col']}] {shading_str} {width_str} {merge_str} vAlign={valign} | \"{cell_text}\"")

                # Show first paragraph run details
                for para in cell.get('paragraphs', []):
                    for run in para.get('runs', []):
                        if run.get('text', '').strip():
                            run_details = []
                            if run.get('font_name'): run_details.append(f"font={run['font_name']}")
                            if run.get('cs_font'): run_details.append(f"cs={run['cs_font']}")
                            if run.get('font_size_pt'): run_details.append(f"size={run['font_size_pt']}pt")
                            if run.get('cs_font_size_pt'): run_details.append(f"csSize={run['cs_font_size_pt']}pt")
                            if run.get('font_color'): run_details.append(f"color=#{run['font_color']}")
                            if run.get('bold'): run_details.append("BOLD")
                            if para.get('alignment'): run_details.append(f"align={para['alignment']}")
                            if para.get('bidi_rtl'): run_details.append("RTL")
                            if run_details:
                                print(f"         Run: {', '.join(run_details)}")

    print(f"\nALL COLORS: {sorted(colors)}")
    print(f"ALL FONTS: {sorted(fonts)}")
    print(f"ALL FONT SIZES (pt): {sorted(font_sizes)}")
