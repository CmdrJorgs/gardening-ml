import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

def build_flowchart(output_path="figure_5_pipeline_architecture.png"):
    fig_w = 35.7
    fig_h = 20.7
    dpi = 100
    
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # -------------------------------------------------------------------------
    # 1. HEADER (Title & Subtitle)
    # -------------------------------------------------------------------------
    ax.text(50, 94.8, "End-to-End Cyber-Physical Precision Agronomy Architecture",
            ha='center', va='center', fontsize=38, fontweight='bold', color='#0d2366',
            fontfamily='DejaVu Sans')
    ax.text(50, 89.8, "Distributed Data Lake, Optimization, Machine Learning, Hydrology, and Generative Synthesis",
            ha='center', va='center', fontsize=25, fontstyle='italic', color='#4b5563',
            fontfamily='DejaVu Sans')

    def draw_box(x, y, w, h, bg_color, border_color, border_width=3.5, rounding=1.5):
        box = FancyBboxPatch((x, y), w, h,
                             boxstyle=f"round,pad=0.2,rounding_size={rounding}",
                             facecolor=bg_color, edgecolor=border_color,
                             linewidth=border_width, zorder=2)
        ax.add_patch(box)
        return box

    def draw_arrow(start, end, color):
        arrow = FancyArrowPatch(start, end,
                                arrowstyle='simple,head_length=1.4,head_width=1.5,tail_width=0.45',
                                mutation_scale=42,
                                facecolor=color, edgecolor=color, zorder=4)
        ax.add_patch(arrow)

    # -------------------------------------------------------------------------
    # COLUMN 1: Data Sources & Lake
    # -------------------------------------------------------------------------
    col1_x, col1_y, col1_w, col1_h = 2.5, 51.0, 19.5, 34.0
    draw_box(col1_x, col1_y, col1_w, col1_h, bg_color='#f0f7ff', border_color='#1976d2', border_width=3.5)
    
    ax.text(col1_x + col1_w/2, col1_y + col1_h - 4.5, "Data Sources & Lake",
            ha='center', va='center', fontsize=26, fontweight='bold', color='#0d47a1',
            fontfamily='DejaVu Sans', zorder=3)
    
    col1_bullets = [
        "• DuckDB Parquet Lake\n  (11 yrs, 3,974 days)",
        "• Open-Meteo ERA5",
        "• Permapeople / PFAF",
        "• USDA / USU Extension"
    ]
    b_y = col1_y + col1_h - 11.2
    for bullet in col1_bullets:
        ax.text(col1_x + 2.2, b_y, bullet,
                ha='left', va='top', fontsize=21, color='#1e3a8a',
                fontfamily='DejaVu Sans', linespacing=1.35, zorder=3)
        b_y -= 5.6

    # ARROW 1 -> 2 (Horizontal)
    draw_arrow((col1_x + col1_w + 0.4, col1_y + col1_h/2),
               (25.5 - 0.4, col1_y + col1_h/2),
               color='#1976d2')

    # -------------------------------------------------------------------------
    # COLUMN 2: LAN IPC Daemon
    # -------------------------------------------------------------------------
    col2_x, col2_y, col2_w, col2_h = 25.5, 51.0, 19.5, 34.0
    draw_box(col2_x, col2_y, col2_w, col2_h, bg_color='#e8f5e9', border_color='#00897b', border_width=3.5)
    
    ax.text(col2_x + col2_w/2, col2_y + col2_h - 4.5, "LAN IPC Daemon",
            ha='center', va='center', fontsize=26, fontweight='bold', color='#004d40',
            fontfamily='DejaVu Sans', zorder=3)
    
    col2_bullets = [
        "• FastAPI / Uvicorn",
        "• Port 8815 LAN Host",
        "• Zero-Copy Arrow IPC",
        "• 459k rows/sec stream",
        "• <10ms query latency"
    ]
    b_y = col2_y + col2_h - 10.8
    for bullet in col2_bullets:
        ax.text(col2_x + 2.2, b_y, bullet,
                ha='left', va='top', fontsize=21, color='#064e3b',
                fontfamily='DejaVu Sans', linespacing=1.35, zorder=3)
        b_y -= 4.6

    # ARROW 2 -> 3 (Horizontal)
    draw_arrow((col2_x + col2_w + 0.4, col2_y + col2_h/2),
               (48.5 - 0.4, col2_y + col2_h/2),
               color='#00897b')

    # -------------------------------------------------------------------------
    # COLUMN 3: Computational Agronomy Engines
    # -------------------------------------------------------------------------
    col3_x, col3_y, col3_w, col3_h = 48.5, 14.0, 28.0, 71.0
    draw_box(col3_x, col3_y, col3_w, col3_h, bg_color='#fffde7', border_color='#ffa000', border_width=3.5)
    
    ax.text(col3_x + col3_w/2, col3_y + col3_h - 4.5, "Computational Agronomy Engines",
            ha='center', va='center', fontsize=25, fontweight='bold', color='#b75500',
            fontfamily='DejaVu Sans', zorder=3)

    modules = [
        ("Module A: Spatial ILP Optimizer",
         "PuLP / MILP: Canopy spread, phototrophic\ngeometry, allelopathy & companion synergy"),
        ("Module B: Frost & Thermal Model",
         "Logistic Reg & 0-7cm soil temp: Spring\nfreeze risk curves & planting windows"),
        ("Module C: Phenology GBDT Regressor",
         "XGBoost: GDD thermal time, photoperiod,\nMAE=0.67 days vs DTM MAE=29.77 days"),
        ("Module D: FAO-56 Hydrology Engine",
         "Dual crop coeff (Kc, TAW, RAW, Dr):\nAutomated irrigation volume & drip runtime")
    ]
    
    mod_w = col3_w - 3.6
    mod_h = 13.0
    m_y = col3_y + col3_h - 8.8 - mod_h
    for title, desc in modules:
        draw_box(col3_x + 1.8, m_y, mod_w, mod_h, bg_color='#ffffff', border_color='#ffe082', border_width=2.0, rounding=1.0)
        ax.text(col3_x + 1.8 + mod_w/2, m_y + mod_h - 3.8, title,
                ha='center', va='center', fontsize=20, fontweight='bold', color='#b71c1c',
                fontfamily='DejaVu Sans', zorder=3)
        ax.text(col3_x + 1.8 + mod_w/2, m_y + 4.2, desc,
                ha='center', va='center', fontsize=16, color='#37474f',
                fontfamily='DejaVu Sans', linespacing=1.35, zorder=3)
        m_y -= (mod_h + 2.5)

    # ARROW 3 -> 4 Top (Orange, to LLM)
    draw_arrow((col3_x + col3_w + 0.4, 68.0),
               (80.5 - 0.4, 68.0),
               color='#ff9800')

    # -------------------------------------------------------------------------
    # COLUMN 4 (TOP): LLM Generative Layer (Gemini 4 Hydrogen)
    # -------------------------------------------------------------------------
    col4_top_x, col4_top_y, col4_top_w, col4_top_h = 80.5, 51.0, 17.5, 34.0
    draw_box(col4_top_x, col4_top_y, col4_top_w, col4_top_h, bg_color='#f3e5f5', border_color='#7b1fa2', border_width=3.5)
    
    ax.text(col4_top_x + col4_top_w/2, col4_top_y + col4_top_h - 4.5, "LLM Generative Layer",
            ha='center', va='center', fontsize=25, fontweight='bold', color='#4a148c',
            fontfamily='DejaVu Sans', zorder=3)
    
    col4_top_bullets = [
        "• Daily State JSON Schema",
        "• Gemini 4 Hydrogen (T=0.1)",
        "• 8th-Grade Reading Level",
        "• Plain English translation",
        "• Urgent actions & timers"
    ]
    b_y = col4_top_y + col4_top_h - 10.8
    for bullet in col4_top_bullets:
        is_model = "Gemini 4 Hydrogen" in bullet
        ax.text(col4_top_x + 1.8, b_y, bullet,
                ha='left', va='top', fontsize=20,
                fontweight='bold' if is_model else 'normal',
                color='#3b0764',
                fontfamily='DejaVu Sans', linespacing=1.35, zorder=3)
        b_y -= 4.6

    # ARROW LLM -> Field Action Layer (Vertical Purple Arrow)
    draw_arrow((col4_top_x + col4_top_w/2, col4_top_y - 0.4),
               (col4_top_x + col4_top_w/2, 45.0 + 0.4),
               color='#6a1b9a')

    # ARROW Module D -> Field Action Layer (Horizontal Green Arrow)
    draw_arrow((col3_x + col3_w + 0.4, 29.5),
               (80.5 - 0.4, 29.5),
               color='#2e7d32')

    # -------------------------------------------------------------------------
    # COLUMN 4 (BOTTOM): Field Action Layer
    # -------------------------------------------------------------------------
    col4_bot_x, col4_bot_y, col4_bot_w, col4_bot_h = 80.5, 14.0, 17.5, 31.0
    draw_box(col4_bot_x, col4_bot_y, col4_bot_w, col4_bot_h, bg_color='#e8f5e9', border_color='#2e7d32', border_width=3.5)
    
    ax.text(col4_bot_x + col4_bot_w/2, col4_bot_y + col4_bot_h - 4.5, "Field Action Layer",
            ha='center', va='center', fontsize=25, fontweight='bold', color='#1b5e20',
            fontfamily='DejaVu Sans', zorder=3)
    
    col4_bot_bullets = [
        "• Raised Bed Poly-Culture",
        "• Precision Drip Irrigation",
        "• Community Gardeners",
        "• Verified Agronomic Care"
    ]
    b_y = col4_bot_y + col4_bot_h - 11.0
    for bullet in col4_bot_bullets:
        ax.text(col4_bot_x + 1.8, b_y, bullet,
                ha='left', va='top', fontsize=20, color='#064e3b',
                fontfamily='DejaVu Sans', linespacing=1.35, zorder=3)
        b_y -= 4.6

    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    plt.savefig(output_path, dpi=100, facecolor='#ffffff', edgecolor='none')
    plt.close()
    print(f"Successfully generated clean flowchart to {output_path}")

if __name__ == "__main__":
    build_flowchart("figure_5_pipeline_architecture.png")
