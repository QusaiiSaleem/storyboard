"""
Extract key PPTX formatting details for documentation.
"""
import json

with open("/Users/qusaiabushanap/dev/storyboard/docs/pptx_analysis_raw.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"PPTX TEMPLATE: {data['filename']}")
print(f"Slide dimensions: {data['slide_width_cm']}cm x {data['slide_height_cm']}cm")
print(f"  Width EMU: {data['slide_width_emu']}, Height EMU: {data['slide_height_emu']}")
print(f"Slide count: {data['slide_count']}")

# Collect all colors and fonts
colors = set()
fonts = set()
font_sizes = set()

for slide in data['slides']:
    print(f"\n{'='*60}")
    print(f"SLIDE {slide['slide_number']} - Layout: {slide['layout_name']}")
    print(f"{'='*60}")

    for shape in slide['shapes']:
        shape_type = shape.get('shape_type', 'Unknown')
        print(f"\n  Shape: {shape['name']}")
        print(f"    Type: {shape_type}")
        print(f"    Position: left={shape['left_cm']}cm, top={shape['top_cm']}cm")
        print(f"    Size: {shape['width_cm']}cm x {shape['height_cm']}cm")
        print(f"    EMU: left={shape['left_emu']}, top={shape['top_emu']}, w={shape['width_emu']}, h={shape['height_emu']}")

        if shape.get('fill'):
            print(f"    Fill: {shape['fill']}")

        if shape.get('line'):
            print(f"    Line: {shape['line']}")

        if shape.get('text_frame'):
            tf = shape['text_frame']
            text_preview = tf['text'][:80] if tf['text'] else '(empty)'
            print(f"    Text: \"{text_preview}\"")
            print(f"    AutoSize: {tf.get('auto_size')}")
            print(f"    Margins: L={tf.get('margin_left_cm')} R={tf.get('margin_right_cm')} T={tf.get('margin_top_cm')} B={tf.get('margin_bottom_cm')}cm")

            for para in tf.get('paragraphs', []):
                if para.get('text', '').strip():
                    print(f"    Paragraph: \"{para['text'][:60]}\"")
                    print(f"      RTL: {para.get('rtl')}, Align: {para.get('algn') or para.get('alignment')}")
                    if para.get('space_before_pt'): print(f"      SpaceBefore: {para['space_before_pt']}pt")
                    if para.get('space_after_pt'): print(f"      SpaceAfter: {para['space_after_pt']}pt")
                    if para.get('line_spacing_pct'): print(f"      LineSpacing: {para['line_spacing_pct']}%")

                    for run in para.get('runs', []):
                        if run.get('text', '').strip():
                            details = []
                            if run.get('font_name'):
                                details.append(f"font={run['font_name']}")
                                fonts.add(run['font_name'])
                            if run.get('cs_font'):
                                details.append(f"cs={run['cs_font']}")
                                fonts.add(run['cs_font'])
                            if run.get('latin_font'):
                                fonts.add(run['latin_font'])
                            if run.get('font_size_pt'):
                                details.append(f"size={run['font_size_pt']}pt")
                                font_sizes.add(run['font_size_pt'])
                            if run.get('font_color_rgb'):
                                details.append(f"color=#{run['font_color_rgb']}")
                                colors.add(f"#{run['font_color_rgb']}")
                            if run.get('bold'): details.append("BOLD")
                            if run.get('italic'): details.append("ITALIC")
                            if run.get('lang'): details.append(f"lang={run['lang']}")
                            print(f"      Run: {', '.join(details)}")

        if shape.get('is_image'):
            print(f"    IMAGE: {shape.get('image_content_type', 'unknown')}")

    if slide.get('notes'):
        print(f"\n  Notes: {slide['notes'][:120]}...")

print(f"\n\n{'='*60}")
print(f"ALL COLORS: {sorted(colors)}")
print(f"ALL FONTS: {sorted(fonts)}")
print(f"ALL FONT SIZES (pt): {sorted(font_sizes)}")

# Print slide master info
print(f"\n\nSLIDE MASTER INFO:")
for i, master in enumerate(data.get('slide_masters', [])):
    print(f"\n  Master {i}:")
    for layout in master.get('layouts', []):
        print(f"    Layout: {layout['name']} ({layout['placeholder_count']} placeholders)")
    for shape in master.get('shapes', []):
        print(f"    Master Shape: {shape['name']} | Type: {shape.get('shape_type')}")
        print(f"      Pos: ({shape['left_cm']}, {shape['top_cm']})cm | Size: {shape['width_cm']}x{shape['height_cm']}cm")
        if shape.get('text_frame'):
            print(f"      Text: \"{shape['text_frame']['text'][:60]}\"")
            for para in shape['text_frame'].get('paragraphs', []):
                for run in para.get('runs', []):
                    if run.get('text', '').strip():
                        rdetails = []
                        if run.get('font_name'): rdetails.append(f"font={run['font_name']}")
                        if run.get('cs_font'): rdetails.append(f"cs={run['cs_font']}")
                        if run.get('font_size_pt'): rdetails.append(f"size={run['font_size_pt']}pt")
                        if run.get('font_color_rgb'): rdetails.append(f"color=#{run['font_color_rgb']}")
                        if run.get('bold'): rdetails.append("BOLD")
                        print(f"        Run: {', '.join(rdetails)}")
