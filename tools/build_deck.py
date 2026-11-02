"""Build the 10-slide Round 1 deck (v2) for Team Old Men.

Usage: python tools/build_deck.py "IT Consultant Challenge - Round 1 - Old Men v2.pptx"
Needs: pip install python-pptx. Fonts used: IBM Plex Sans and Georgia.
"""
import sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn

OUT = sys.argv[1]

NAVY = RGBColor(0x14, 0x21, 0x3D)
NAVY2 = RGBColor(0x22, 0x32, 0x5A)
ORANGE = RGBColor(0xB8, 0x52, 0x0F)
ORANGE_L = RGBColor(0xF0, 0xA3, 0x5E)
BG = RGBColor(0xF7, 0xF6, 0xF2)
BEIGE = RGBColor(0xEC, 0xE9, 0xE2)
PEACH = RGBColor(0xF6, 0xE1, 0xD3)
MUTED = RGBColor(0x55, 0x5E, 0x72)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SOFT = RGBColor(0xC9, 0xD1, 0xE3)
LINE = RGBColor(0xC8, 0xC3, 0xB8)

SANS = "IBM Plex Sans"
SERIF = "Georgia"
DOTS = "Arial"

prs = Presentation()
prs.slide_width = Inches(20)
prs.slide_height = Inches(11.25)
BLANK = prs.slide_layouts[6]
X0 = 1.333            # left margin (in)
CW = 20 - 2 * X0      # content width


def new_slide(bg=BG):
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = bg
    return s


def _strip_style(shape):
    st = shape._element.find(qn("p:style"))
    if st is not None:
        shape._element.remove(st)


def text(s, x, y, w, h, paras, size=18, color=NAVY, bold=False, font=SANS,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.2, space_after=0):
    """paras: list of str, or list of run-lists [(text, {opts}), ...]."""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    if isinstance(paras, str):
        paras = [paras]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        p.space_after = Pt(space_after)
        runs = [(para, {})] if isinstance(para, str) else para
        for t, o in runs:
            r = p.add_run()
            r.text = t
            f = r.font
            f.name = o.get("font", font)
            f.size = Pt(o.get("size", size))
            f.bold = o.get("bold", bold)
            f.italic = o.get("italic", False)
            f.color.rgb = o.get("color", color)
    return tb


def box(s, x, y, w, h, fill, line=None, lw=1.5, radius=0.06, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    sh = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    _strip_style(sh)
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        sh.adjustments[0] = min(0.5, radius * 3 / min(w, h))  # ~0.18in corner radius
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(lw)
    return sh


def rect(s, x, y, w, h, fill):
    return box(s, x, y, w, h, fill, shape=MSO_SHAPE.RECTANGLE)


def arrow(s, x, y, w=0.45, h=0.36, color=ORANGE):
    sh = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
    _strip_style(sh)
    sh.fill.solid()
    sh.fill.fore_color.rgb = color
    sh.line.fill.background()
    return sh


def header(s, eyebrow, title, dark=False):
    text(s, X0, 0.78, CW, 0.4, eyebrow.upper(), size=17, bold=True,
         color=ORANGE_L if dark else ORANGE)
    text(s, X0, 1.2, CW, 1.0, title, size=40, bold=True, font=SERIF,
         color=WHITE if dark else NAVY, spacing=1.05)


def footer(s, n, dark=False):
    c = SOFT if dark else MUTED
    text(s, X0, 10.45, 12, 0.35, "Team Old Men · Company A · Round 1 proposal", size=14, color=c)
    text(s, 20 - X0 - 1, 10.45, 1, 0.35, f"{n:02d}", size=14, color=c, align=PP_ALIGN.RIGHT)


def table(s, x, y, w, col_w, rows, size=15, header_fill=NAVY, row_h=0.6, header_h=0.6,
          fills=None, bold_cols=(), pad=0.12):
    """rows[0] is the header. fills: dict row_index -> RGB for body rows."""
    nr, nc = len(rows), len(rows[0])
    gs = s.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(header_h + row_h * (nr - 1)))
    tbl = gs.table
    # drop the built-in table style banding
    tblPr = tbl._tbl.tblPr
    tblPr.set("firstRow", "0")
    tblPr.set("bandRow", "0")
    total = sum(col_w)
    for i, cw in enumerate(col_w):
        tbl.columns[i].width = Emu(int(Inches(w) * cw / total))
    for r in range(nr):
        tbl.rows[r].height = Inches(header_h if r == 0 else row_h)
        for c in range(nc):
            cell = tbl.cell(r, c)
            val = rows[r][c]
            cell.margin_left = cell.margin_right = Inches(pad)
            cell.margin_top = cell.margin_bottom = Inches(0.07)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if r == 0:
                cell.fill.fore_color.rgb = header_fill
            else:
                cell.fill.fore_color.rgb = (fills or {}).get(r, BG if r % 2 else RGBColor(0xFB, 0xFA, 0xF7))
            tf = cell.text_frame
            tf.word_wrap = True
            runs = val if isinstance(val, list) else [(val, {})]
            p = tf.paragraphs[0]
            p.line_spacing = 1.1
            for t, o in runs:
                rr = p.add_run()
                rr.text = t
                f = rr.font
                f.name = o.get("font", SANS)
                f.size = Pt(o.get("size", size))
                f.bold = o.get("bold", r == 0 or c in bold_cols)
                f.color.rgb = o.get("color", WHITE if r == 0 else NAVY)
    return tbl


def bullets(items, size=17, color=NAVY, mark="–  ", mark_color=ORANGE):
    return [[(mark, {"color": mark_color, "bold": True, "size": size}), (t, {"size": size, "color": color})]
            if isinstance(t, str) else
            [(mark, {"color": mark_color, "bold": True, "size": size})] + t
            for t in items]


# ---------------------------------------------------------------- 1. Cover
s = new_slide(NAVY)
rect(s, X0, 0.95, 1.25, 0.08, ORANGE_L)
text(s, X0, 1.3, CW, 0.4, "IT CONSULTANT CHALLENGE 2026 · ROUND 1", size=17, bold=True, color=ORANGE_L)
text(s, X0, 1.85, 16, 2.2, "Keeping the delivery promise across three markets",
     size=58, bold=True, font=SERIF, color=WHITE, spacing=1.0)
text(s, X0, 3.95, 15, 0.9,
     "A fulfilment control layer on top of Company A’s existing systems in Denmark, Norway and Sweden",
     size=22, color=SOFT)

box(s, X0, 4.95, CW, 3.85, NAVY2)
text(s, X0 + 0.4, 5.2, 8, 0.4, "THE ANSWER ON ONE PAGE", size=15, bold=True, color=ORANGE_L)
summary = [
    ("Problem", "Order, stock, supplier and transport data sit in separate systems, so a late or incomplete "
                "delivery is usually discovered only when the truck arrives."),
    ("Solution", "One shared layer reads those systems, joins every order into one timeline, flags orders "
                 "at risk and alerts staff and customers early. No existing system is replaced."),
    ("MVP", "Sweden, 20 pilot stores, 12 weeks, read-only. Then Denmark and Norway with their own adapters."),
    ("Impact", "About EUR 135k a year in the pilot and about EUR 2M a year at group scale; payback within "
               "6 months of full rollout (assumed figures, see slide 10)."),
]
yy = 5.7
for k, v in summary:
    text(s, X0 + 0.4, yy, 1.6, 0.6, k, size=17, bold=True, color=ORANGE_L)
    text(s, X0 + 2.1, yy, CW - 2.6, 0.7, v, size=17, color=WHITE)
    yy += 0.75

text(s, X0, 9.05, 4, 0.4, "Team Old Men", size=19, bold=True, color=WHITE)
text(s, X0, 9.5, 14, 0.4, "Nguyễn Việt Anh   ·   Vũ Văn Hậu   ·   Nguyễn Hoàng Anh Dũng", size=17, color=SOFT)
text(s, 20 - X0 - 4, 9.5, 4, 0.4, "October 2026", size=17, color=SOFT, align=PP_ALIGN.RIGHT)

# ---------------------------------------------------------------- 2. Real problem
s = new_slide()
header(s, "The real problem", "All four challenges end in one place: the delivery")
chain = [
    ("ROOT CAUSE", "Fragmented systems", "Order, stock, supplier and transport data live in different systems"),
    ("SO", "No one sees the whole order", "No single system can tell whether every part will be ready on time"),
    ("SO", "Manual chasing", "Staff check several systems and phone colleagues and carriers"),
    ("SO", "Inconsistent handling", "Each store deals with late orders in its own way"),
    ("RESULT", "Broken delivery promise", "Late or incomplete delivery; the customer finds out first"),
]
bw, gap = 2.95, 0.65
for i, (tag, head, body) in enumerate(chain):
    x = X0 + i * (bw + gap)
    last = i == len(chain) - 1
    box(s, x, 2.75, bw, 2.55, NAVY if last else BEIGE)
    text(s, x + 0.25, 2.95, bw - 0.5, 0.3, tag, size=13, bold=True, color=ORANGE_L if last else ORANGE)
    text(s, x + 0.25, 3.3, bw - 0.5, 0.8, head, size=19, bold=True, color=WHITE if last else NAVY, spacing=1.05)
    text(s, x + 0.25, 4.15, bw - 0.5, 1.1, body, size=15, color=SOFT if last else MUTED)
    if not last:
        arrow(s, x + bw + 0.1, 3.85)

box(s, X0, 5.55, CW, 0.8, PEACH)
text(s, X0 + 0.3, 5.55, CW - 0.6, 0.8,
     [[("Fulfilment is where all four challenges meet, and the only one the customer feels directly. ",
        {"bold": True}),
       ("Making every order visible across systems breaks the chain without replacing them.", {})]],
     size=17, anchor=MSO_ANCHOR.MIDDLE)

who = [
    ("Construction customers",
     "A crew of four waiting for a missing delivery loses about EUR 1,500 in a day (assumed). "
     "This is what makes professional customers switch to a competitor."),
    ("Store and distribution staff",
     "Every “where is my order?” call means searching several systems. Problems are found when "
     "it is too late to fix them."),
    ("Management",
     "No shared view of delivery performance across stores and countries, so what works in one "
     "market cannot be repeated in the others."),
]
cw3 = (CW - 2 * 0.5) / 3
text(s, X0, 6.65, CW, 0.35, "WHO IS HURT AND HOW", size=14, bold=True, color=ORANGE)
for i, (h, b) in enumerate(who):
    x = X0 + i * (cw3 + 0.5)
    rect(s, x, 7.1, cw3, 0.06, ORANGE)
    text(s, x, 7.3, cw3, 0.45, h, size=20, bold=True)
    text(s, x, 7.85, cw3, 1.8, b, size=16, color=MUTED)
footer(s, 2)

# ---------------------------------------------------------------- 3. Prioritisation
s = new_slide()
header(s, "Where to focus first", "Fulfilment scores highest on impact and on speed to results")


def dots(n):
    return [("●" * n, {"font": DOTS, "color": ORANGE, "size": 16}),
            ("○" * (3 - n), {"font": DOTS, "color": LINE, "size": 16})]


hdr = ["Challenge", "Business impact", "Felt by customers", "Results within ~3 months", "Helps the other challenges",
       "Score", "Our verdict"]
rows = [hdr,
        ["Fragmented systems", dots(3), dots(1), dots(1), dots(3), "8 / 12",
         "Root cause, but replacing systems takes years. Our layer starts reducing it."],
        ["Manual processes", dots(3), dots(1), dots(2), dots(2), "8 / 12",
         "Big internal cost, but different in each country. Our layer removes the status chasing."],
        ["Inconsistent operations", dots(2), dots(2), dots(1), dots(1), "6 / 12",
         "Mainly a process-change task; hard to measure quickly."],
        [[("Delivery and fulfilment", {"bold": True})], dots(3), dots(3), dots(3), dots(3),
         [("12 / 12", {"bold": True})], [("Prioritised: ", {"bold": True, "color": ORANGE}),
                                         ("works on top of existing systems and touches all four.", {})]],
        ]
table(s, X0, 2.6, CW, [2.6, 1.55, 1.55, 1.75, 1.75, 0.95, 5.2], rows, size=15, row_h=0.78, header_h=0.75,
      fills={4: PEACH}, bold_cols=(0,))
text(s, X0, 6.55, CW, 0.4,
     "Scored 1–3 by our team from the brief and our assumptions. “Results within ~3 months” means an MVP can show "
     "measurable results without replacing any system.", size=14, color=MUTED)

text(s, X0, 7.2, CW, 0.35, "ONE SOLUTION, A BENEFIT FOR EACH MARKET’S OWN PRIORITY", size=14, bold=True, color=ORANGE)
mk = [("Sweden", "Top priority: delivery and fulfilment",
       "Fewer late and incomplete deliveries; customers warned early."),
      ("Denmark", "Top priority: manual processes",
       "No more searching several systems to answer “where is my order?”."),
      ("Norway", "Top priority: store operations",
       "Every store handles problem orders the same way, from one task list.")]
for i, (c, p, b) in enumerate(mk):
    x = X0 + i * (cw3 + 0.5)
    box(s, x, 7.65, cw3, 2.3, BEIGE)
    text(s, x + 0.3, 7.85, cw3 - 0.6, 0.45, c, size=20, bold=True)
    text(s, x + 0.3, 8.33, cw3 - 0.6, 0.4, p, size=14, bold=True, color=ORANGE)
    text(s, x + 0.3, 8.8, cw3 - 0.6, 1.0, b, size=16, color=MUTED)
footer(s, 3)

# ---------------------------------------------------------------- 4. Assumptions
s = new_slide(BEIGE)
header(s, "Key assumptions", "We state, justify and test every assumption")
rows = [["Assumption", "Why it is reasonable", "How we check it in weeks 1–3"],
        ["One order is often fulfilled from several sources: store, central warehouse, supplier",
         "Building materials are bulky and varied; the brief names store and distribution operations separately",
         "Sample 500 recent orders and count the sources per order"],
        ["Order, stock, purchasing and transport data sit in separate systems",
         "Each country built its own systems over time (brief)",
         "Map the Swedish systems with local IT"],
        ["About 10% of deliveries are late, incomplete or failed today",
         "Typical for bulky deliveries from several sources",
         "Measure from 12 months of delivery history"],
        ["About 60% of those problems start before the truck leaves: missing stock, late supplier, picking not done",
         "A delivery can only leave on time if every part is ready",
         "Classify the causes of last quarter’s problem deliveries"],
        ["Every system can at least export its data (API, database or file export)",
         "Standard for retail order and finance systems",
         "Technical check of each source system"],
        ["Sweden feels fulfilment pain the most",
         "The brief’s own example; long distances and heavy use of external carriers",
         "Compare delivery figures across the three countries"],
        ]
table(s, X0, 2.6, CW, [6.2, 6.0, 4.6], rows, size=15, row_h=0.88, header_h=0.62)
text(s, X0, 8.95, CW, 0.5,
     "All figures in this deck are illustrative assumptions. Weeks 1–3 of the MVP replace them with measured values "
     "before any target is fixed.", size=15, color=MUTED)
footer(s, 4)

# ---------------------------------------------------------------- 5. Solution
s = new_slide()
header(s, "Proposed solution", "A control layer that joins, checks and acts")
text(s, X0, 2.55, 3.4, 0.35, "Existing systems (unchanged)", size=15, bold=True, color=MUTED)
for i, t in enumerate(["Order system", "Stock and warehouse", "Purchasing and suppliers", "Transport and carriers"]):
    box(s, X0, 2.98 + i * 0.78, 3.1, 0.62, BEIGE)
    text(s, X0 + 0.2, 2.98 + i * 0.78, 2.8, 0.62, t, size=16, anchor=MSO_ANCHOR.MIDDLE)
arrow(s, X0 + 3.25, 4.27)
ax = X0 + 3.85
box(s, ax, 3.3, 2.75, 2.35, WHITE, line=NAVY, lw=2)
text(s, ax + 0.25, 3.5, 2.3, 0.45, "Country adapter", size=19, bold=True)
text(s, ax + 0.25, 4.0, 2.3, 1.6, "Reads and translates local data into one shared format. One per country.",
     size=15, color=MUTED)
arrow(s, ax + 2.9, 4.27)
cx = ax + 3.5
box(s, cx, 2.6, 5.4, 3.85, NAVY)
text(s, cx + 0.3, 2.75, 5, 0.4, "Shared core (same in every country)", size=15, bold=True, color=ORANGE_L)
core = [("Join", "one timeline per order, across all systems"),
        ("Check", "each part against the date promised to the customer"),
        ("Act", "a task for the store and an early warning to the customer")]
for i, (k, v) in enumerate(core):
    box(s, cx + 0.3, 3.25 + i * 1.03, 4.8, 0.88, NAVY2)
    text(s, cx + 0.5, 3.25 + i * 1.03, 4.5, 0.88,
         [[(k + ": ", {"bold": True, "color": WHITE}), (v, {"color": SOFT})]], size=16, anchor=MSO_ANCHOR.MIDDLE)
arrow(s, cx + 5.55, 4.27)
ox = cx + 6.15
text(s, ox, 2.55, 20 - X0 - ox, 0.35, "Outputs", size=15, bold=True, color=MUTED)
for i, t in enumerate(["Task list for each store", "Order lookup for staff", "Early updates to customers",
                       "KPI view for management"]):
    box(s, ox, 2.98 + i * 0.78, 20 - X0 - ox, 0.62, WHITE, line=ORANGE, lw=1.5)
    text(s, ox + 0.2, 2.98 + i * 0.78, 20 - X0 - ox - 0.3, 0.62, t, size=16, anchor=MSO_ANCHOR.MIDDLE)

half = (CW - 0.4) / 2
box(s, X0, 6.75, half, 0.95, BEIGE)
text(s, X0 + 0.3, 6.75, half - 0.6, 0.95,
     [[("One strategic solution: ", {"bold": True}), ("the same order model, risk rules and screens in every market.", {})]],
     size=16, anchor=MSO_ANCHOR.MIDDLE)
box(s, X0 + half + 0.4, 6.75, half, 0.95, BEIGE)
text(s, X0 + half + 0.7, 6.75, half - 0.6, 0.95,
     [[("Not one identical implementation: ", {"bold": True}),
       ("own adapter per country; cut-off times, delivery windows, language and channels are settings.", {})]],
     size=16, anchor=MSO_ANCHOR.MIDDLE)

text(s, X0, 7.95, CW, 0.35, "WHY NOT SOMETHING BIGGER FIRST?", size=14, bold=True, color=ORANGE)
alts = [("Replace all systems", "Takes years; conflicts with “time to market is critical”."),
        ("Connect systems to each other", "Connections multiply; still no single view of an order."),
        ("Data warehouse and reports", "Shows problems after they happen; nobody is told to act."),
        ("Full order management system", "Changes systems and processes in all countries at once.")]
aw = (CW - 3 * 0.3) / 4
for i, (h, b) in enumerate(alts):
    x = X0 + i * (aw + 0.3)
    rect(s, x, 8.4, 0.05, 1.45, LINE)
    text(s, x + 0.2, 8.4, aw - 0.3, 0.4, h, size=16, bold=True)
    text(s, x + 0.2, 8.85, aw - 0.3, 1.0, b, size=15, color=MUTED)
footer(s, 5)

# ---------------------------------------------------------------- 6. Order 1001
s = new_slide()
header(s, "How it works: one order", "Order 1001: found on Monday, not on Wednesday")
text(s, X0, 2.55, 10.5, 0.4,
     [[("A construction customer’s order is promised for ", {}), ("Wednesday", {"bold": True}),
       (". Today is ", {}), ("Monday", {"bold": True}), (".", {})]], size=17, color=MUTED)
rows = [["Line", "Product", "Source system", "Status", "Check"],
        ["A", "50 bags of cement", "Store stock", "Picked", "On track"],
        ["B", "20 steel bars", "Central warehouse", "Not yet picked", "Watch: pick by Tue 14:00"],
        ["C", "Concrete mixer", "Supplier", "Confirmed for Thursday", [("At risk: 1 day late", {"bold": True})]],
        ]
table(s, X0, 3.1, 10.5, [0.7, 2.2, 2.2, 2.4, 2.6], rows, size=15, row_h=0.72, header_h=0.62, fills={3: PEACH})
text(s, X0, 5.95, 10.5, 0.5, "Each line lives in a different system. Only the joined timeline shows the conflict.",
     size=16, color=MUTED)

rx = X0 + 11.0
rw = 20 - X0 - rx
box(s, rx, 2.55, rw, 4.1, NAVY)
text(s, rx + 0.4, 2.8, rw - 0.8, 0.4, "What the layer does on Monday", size=17, bold=True, color=ORANGE_L)
steps = [
    "Opens a task for the store’s delivery coordinator: “Line C is one day late”.",
    "Suggests a fix with a simple rule: deliver A and B on Wednesday, C on Thursday.",
    "Once the coordinator confirms, texts the customer the new plan in Swedish.",
]
text(s, rx + 0.4, 3.35, rw - 0.8, 3.2,
     [[(f"{i + 1}.  ", {"bold": True, "color": ORANGE_L}), (t, {"color": WHITE})] for i, t in enumerate(steps)],
     size=17, spacing=1.15, space_after=10)

half = (CW - 0.4) / 2
box(s, X0, 7.0, half, 2.3, BEIGE)
text(s, X0 + 0.35, 7.2, half - 0.7, 0.4, "WITHOUT THE LAYER", size=14, bold=True, color=MUTED)
text(s, X0 + 0.35, 7.65, half - 0.7, 2.1,
     "Wednesday morning the truck arrives without the mixer. The crew waits, the customer calls the store, "
     "and staff search four systems to find out why.", size=17)
box(s, X0 + half + 0.4, 7.0, half, 2.3, PEACH)
text(s, X0 + half + 0.75, 7.2, half - 0.7, 0.4, "WITH THE LAYER", size=14, bold=True, color=ORANGE)
text(s, X0 + half + 0.75, 7.65, half - 0.7, 2.1,
     "Two days to act. The customer re-plans the crew around Thursday, nobody waits on site, and the store "
     "avoids a failed delivery.", size=17)
footer(s, 6)

# ---------------------------------------------------------------- 7. AI
s = new_slide(BEIGE)
header(s, "Where AI creates value", "AI only where fixed rules fall short")
rows = [["AI use", "What it does", "Why fixed rules are not enough", "When"],
        ["Read supplier messages", "Pulls confirmed dates and quantities from supplier emails and PDF confirmations",
         "Every supplier writes differently; today staff read and type these by hand", [("MVP", {"bold": True, "color": ORANGE})]],
        ["Data-mapping assistant", "Helps our engineers connect each new country’s systems to the shared order model",
         "Every country names its data differently; this is the slowest part of each rollout",
         "Phase 2"],
        ["Delay-risk prediction", "Learns which suppliers, products and periods run late even when status looks fine",
         "Rules only see problems that are already visible", "Phase 3"],
        ["Smarter fix suggestions", "Weighs stock in nearby stores, distance and customer priority",
         "Too many combinations to write as fixed rules", "Phase 3"],
        ["Customer replies", "Answers “where is my order?” by chat or email in Danish, Norwegian and Swedish",
         "Questions vary too much for fixed answers", "Phase 3"],
        ]
table(s, X0, 2.55, CW, [3.3, 6.0, 5.9, 2.0], rows, size=15, row_h=0.86, header_h=0.62)
text(s, X0, 7.62, CW, 0.35,
     "MVP = Sweden pilot, weeks 1–12   ·   Phase 2 = Denmark and Norway   ·   Phase 3 = all markets (see slide 9)",
     size=14, color=MUTED)
box(s, X0, 8.1, CW, 1.85, NAVY)
text(s, X0 + 0.4, 8.28, 6, 0.4, "AI ASSISTS, RULES DECIDE", size=14, bold=True, color=ORANGE_L)
text(s, X0 + 0.4, 8.7, CW - 0.8, 1.2,
     [[("Every alert comes from a clear rule, so staff always see why. ", {"bold": True, "color": WHITE}),
       ("AI only reads and suggests: dates it is unsure about go to a person, and if AI is down, staff enter dates "
        "by hand as today. Customer messages use only facts from the order timeline, so AI never invents a delivery "
        "date. Models run in the EU under GDPR.", {"color": SOFT})]], size=16)
footer(s, 7)

# ---------------------------------------------------------------- 8. MVP
s = new_slide()
header(s, "MVP scope", "One market, read-only, 12 weeks")
lw_ = 9.6
box(s, X0, 2.5, lw_, 3.6, NAVY)
text(s, X0 + 0.4, 2.7, 6, 0.45, "In scope", size=20, bold=True, color=ORANGE_L)
text(s, X0 + 0.4, 3.25, lw_ - 0.8, 2.8, bullets([
    "Sweden, 20 pilot stores",
    "One adapter: order, stock, purchasing and transport data",
    "Shared order model and rule-based risk checks",
    "Task list and order lookup for store staff",
    "Delay updates to customers by SMS (fixed templates)",
    "AI: reading supplier emails and PDF confirmations",
], size=18, color=WHITE, mark_color=ORANGE_L), spacing=1.3)
ox = X0 + lw_ + 0.4
ow = 20 - X0 - ox
box(s, ox, 2.5, ow, 3.6, BEIGE)
text(s, ox + 0.4, 2.7, 6, 0.45, "Not in the MVP", size=20, bold=True, color=MUTED)
text(s, ox + 0.4, 3.25, ow - 0.8, 2.8, bullets([
    "Writing back into existing systems",
    "Replacing any existing system",
    "Denmark and Norway (Phase 2)",
    "Live driver tracking",
    "AI delay prediction (Phase 3)",
], size=18, color=MUTED), spacing=1.3)

text(s, X0, 6.35, CW, 0.35, "12-WEEK PLAN", size=14, bold=True, color=ORANGE)
plan = [("Weeks 1–3", "Map Swedish systems, check assumptions, measure the baseline"),
        ("Weeks 4–7", "Build the adapter, order model and risk rules"),
        ("Weeks 8–10", "Staff screens and alerts; test in 2 stores"),
        ("Weeks 11–12", "Live in 20 stores; compare with the baseline")]
pw = (CW - 3 * 0.3) / 4
for i, (h, b) in enumerate(plan):
    x = X0 + i * (pw + 0.3)
    box(s, x, 6.78, pw, 1.3, WHITE, line=NAVY, lw=1.25)
    text(s, x + 0.25, 6.9, pw - 0.5, 0.4, h, size=16, bold=True, color=ORANGE)
    text(s, x + 0.25, 7.3, pw - 0.5, 0.8, b, size=15)

tw = 7.0
box(s, X0, 8.35, tw, 1.6, BEIGE)
text(s, X0 + 0.3, 8.5, tw - 0.6, 1.4,
     [[("Team and cost (assumed)", {"bold": True})],
      [("6 people: product owner, 2 developers, integration engineer, UX designer (part-time) and a Swedish "
        "store-operations lead. About ", {}), ("EUR 250k", {"bold": True}), (".", {})]],
     size=15, spacing=1.15)
gx = X0 + tw + 0.4
gw = 20 - X0 - gx
box(s, gx, 8.35, gw, 1.6, PEACH)
text(s, gx + 0.3, 8.5, gw - 0.6, 1.4,
     [[("Go / no-go for Denmark and Norway after week 12", {"bold": True})],
      [("≥ 60% of problem deliveries flagged at least a day ahead  ·  staff in pilot stores use the task list every "
        "day  ·  data matches the source systems in ≥ 98% of checked orders", {})]],
     size=15, spacing=1.15)
footer(s, 8)

# ---------------------------------------------------------------- 9. Rollout
s = new_slide()
header(s, "Rollout across markets", "One core, adapted to each country")
phases = [(ORANGE, "Phase 1 · months 1–3", "Sweden pilot",
           "Prove the impact where fulfilment hurts most. Store staff co-design the screens."),
          (ORANGE_L, "Phase 2 · months 4–9", "Denmark and Norway",
           "New adapters, built faster with the AI mapping assistant. Denmark: less manual chasing. "
           "Norway: one way for every store to handle problem orders."),
          (NAVY, "Phase 3 · month 10 onwards", "All markets",
           "AI delay prediction, smarter fix suggestions, and write-back into existing systems.")]
pw = CW / 3
for i, (c, t, h, b) in enumerate(phases):
    x = X0 + i * pw
    rect(s, x, 2.55, pw, 0.09, c)
    text(s, x, 2.8, pw - 0.4, 0.35, t, size=15, bold=True, color=ORANGE)
    text(s, x, 3.2, pw - 0.4, 0.5, h, size=22, bold=True)
    text(s, x, 3.75, pw - 0.45, 1.3, b, size=15, color=MUTED)

half = (CW - 0.4) / 2
box(s, X0, 5.2, half, 1.85, BEIGE)
text(s, X0 + 0.35, 5.35, half - 0.7, 1.6,
     [[("Why Sweden first, not the home market Denmark?", {"bold": True})],
      [("Fulfilment hurts most in Sweden, so the effect is clearest to measure. A smaller pilot also keeps early "
        "mistakes away from the largest market.", {"color": MUTED})]], size=16, spacing=1.15, space_after=4)
box(s, X0 + half + 0.4, 5.2, half, 1.85, BEIGE)
text(s, X0 + half + 0.75, 5.35, half - 0.7, 1.6,
     [[("Who acts on the alerts?", {"bold": True})],
      [("Each store’s delivery coordinator owns its task list and handles alerts the same working day. A central "
        "team of 3–4 owns the rules, settings and KPIs for all countries.", {"color": MUTED})]],
     size=16, spacing=1.15, space_after=4)

text(s, X0, 7.3, CW, 0.35, "KEY RISKS AND HOW WE HANDLE THEM", size=14, bold=True, color=ORANGE)
risks = [("Poor or inconsistent data", "Data checks in every adapter; the pilot validates the order model first."),
         ("Old systems without APIs", "Hourly or daily file exports instead; still far better than today."),
         ("Staff do not adopt it", "No extra data entry; it replaces searching. 1-hour training and a super-user per store."),
         ("Too many alerts", "Start with a few rules; tune thresholds weekly with the pilot stores.")]
rw4 = (CW - 3 * 0.3) / 4
for i, (h, b) in enumerate(risks):
    x = X0 + i * (rw4 + 0.3)
    box(s, x, 7.75, rw4, 2.15, WHITE, line=LINE, lw=1)
    text(s, x + 0.25, 7.92, rw4 - 0.5, 0.45, h, size=16, bold=True)
    text(s, x + 0.25, 8.42, rw4 - 0.5, 1.4, b, size=15, color=MUTED)
footer(s, 9)

# ---------------------------------------------------------------- 10. Business impact
s = new_slide(NAVY)
header(s, "Measurable business impact", "Small pilot to prove it, large value at scale", dark=True)
half = (CW - 0.4) / 2
# pilot
box(s, X0, 2.5, half, 3.9, NAVY2)
text(s, X0 + 0.4, 2.7, half - 0.8, 0.4, "SWEDEN PILOT · 20 STORES · PER YEAR", size=14, bold=True, color=ORANGE_L)
text(s, X0 + 0.4, 3.1, 4, 0.9, "1,200", size=50, bold=True, font=SERIF, color=ORANGE_L)
text(s, X0 + 3.6, 3.3, half - 4.0, 0.8, "fewer problem deliveries, about EUR 120k saved", size=17, color=WHITE)
text(s, X0 + 0.4, 4.0, 4, 0.9, "400 h", size=50, bold=True, font=SERIF, color=ORANGE_L)
text(s, X0 + 3.6, 4.2, half - 4.0, 0.8, "of staff time freed from status calls, about EUR 16k", size=17, color=WHITE)
text(s, X0 + 0.4, 5.1, half - 0.8, 1.2,
     [[("Where 30% comes from: ", {"bold": True, "color": WHITE}),
       ("4,000 problem deliveries × 60% start before dispatch × half can be fixed when flagged a day ahead "
        "= 1,200.", {"color": SOFT})]], size=15)
# scale
gx = X0 + half + 0.4
box(s, gx, 2.5, half, 3.9, NAVY2)
text(s, gx + 0.4, 2.7, half - 0.8, 0.4, "GROUP SCALE · ~300 STORES · THREE COUNTRIES", size=14, bold=True, color=ORANGE_L)
text(s, gx + 0.4, 3.1, 4, 0.9, "€2.0M", size=50, bold=True, font=SERIF, color=ORANGE_L)
text(s, gx + 4.0, 3.3, half - 4.4, 0.8, "benefit a year: the pilot result × 15", size=17, color=WHITE)
text(s, gx + 0.4, 4.2, half - 0.8, 1.3,
     [[("Investment: ", {"bold": True, "color": WHITE}),
       ("about EUR 750k (MVP 250k + rollout 500k), plus about EUR 150k a year to run.", {"color": SOFT})],
      [("Payback: ", {"bold": True, "color": WHITE}),
       ("within 6 months of full rollout. The pilot alone is not meant to pay back; it proves the numbers.",
        {"color": SOFT})]], size=15, spacing=1.15, space_after=6)
text(s, gx + 0.4, 5.65, half - 0.8, 0.7,
     [[("Not counted: ", {"bold": True, "color": WHITE}),
       ("sales kept from professional customers who no longer switch to a competitor.", {"color": SOFT})]], size=15)

rows = [["KPI", "Baseline", "Pilot target"],
        ["On-time and complete delivery rate", "90% (assumed)", "93%"],
        ["Problem deliveries flagged at least one day ahead", "≈ 0% today", "60% or more"],
        ["“Where is my order?” contacts", "10,000 a year (assumed)", "−50%"],
        ]
table(s, X0, 6.7, CW, [8.0, 4.5, 4.3], rows, size=15, header_fill=NAVY2, row_h=0.6, header_h=0.55)
text(s, X0, 9.65, CW, 0.4,
     "Assumed: 40,000 deliveries a year in the pilot, 10% problem rate, EUR 100 per problem delivery, 5 minutes per "
     "status call, EUR 40 per staff hour.", size=13, color=SOFT)
text(s, 20 - X0 - 1, 10.45, 1, 0.35, "10", size=14, color=SOFT, align=PP_ALIGN.RIGHT)
text(s, X0, 10.45, 12, 0.35, "Team Old Men · Company A · Round 1 proposal", size=14, color=SOFT)

prs.save(OUT)
print("saved", OUT, len(prs.slides), "slides")
