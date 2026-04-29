"""
ออกแบบฐานรากรับโมเม้นต์ กรณีเสาเข็มเยื้องศูนย์ (2 ต้น)
Eccentric Pile Cap Design — P + M Loading (2 Piles)

สูตร:  Pi = P/n  ±  M·ei / Σei²
"""

import math


# ─────────────────────────────────────────────
#  INPUT DATA  (แก้ไขค่าตรงนี้)
# ─────────────────────────────────────────────
P        = 800.0   # kN  — แรงในแนวดิ่ง
M        = 120.0   # kN·m — โมเม้นต์
s        = 1.50    # m   — ระยะห่างระหว่างเสาเข็ม (centre-to-centre)

Q_comp   = 600.0   # kN  — กำลังรับแรงกดที่ยอมรับของเสาเข็มแต่ละต้น
Q_tens   = 0.0     # kN  — กำลังรับแรงดึงที่ยอมรับ (0 = ไม่รับแรงดึง)

pile_dia = 0.30    # m   — เส้นผ่านศูนย์กลางเสาเข็ม
# ─────────────────────────────────────────────


SEP = "─" * 55


def check(condition, label):
    status = "PASS ✓" if condition else "FAIL ✗"
    return f"  [{status}]  {label}"


def design():
    n = 2

    # ระยะจากจุดศูนย์กลางกลุ่มเสาเข็มถึงเสาเข็มแต่ละต้น
    e1 = s / 2   # เสาเข็มต้นที่ 1 (ด้านรับแรงอัด)
    e2 = s / 2   # เสาเข็มต้นที่ 2 (ด้านตรงข้าม)

    sum_e2 = e1**2 + e2**2   # = 2·(s/2)²  = s²/2

    # ─── แรงในเสาเข็ม ───────────────────────────────
    P_avg = P / n
    delta = M * e1 / sum_e2

    P1 = P_avg + delta   # เสาเข็มต้นที่ 1 (แรงกดสูงสุด)
    P2 = P_avg - delta   # เสาเข็มต้นที่ 2 (อาจมีแรงดึง)

    # ─── ระยะเยื้องศูนย์ ────────────────────────────
    e_ecc = M / P if P != 0 else float("inf")
    kern  = s / 6   # ขอบ kern ของกลุ่มเสาเข็ม 2 ต้น

    # ─── การตรวจสอบ ──────────────────────────────────
    ok_comp  = P1 <= Q_comp
    ok_tens  = P2 >= -Q_tens
    ok_kern  = e_ecc <= kern

    all_ok = ok_comp and ok_tens

    # ─── พิมพ์ผลลัพธ์ ────────────────────────────────
    print(SEP)
    print("  ออกแบบฐานรากรับโมเม้นต์ — เสาเข็ม 2 ต้น")
    print(SEP)

    print("\n[1] ข้อมูลรับเข้า")
    print(f"  P       = {P:.2f}  kN")
    print(f"  M       = {M:.2f}  kN·m")
    print(f"  s       = {s:.3f} m  (ระยะห่างเสาเข็ม c/c)")
    print(f"  Q_comp  = {Q_comp:.2f} kN  (กำลังรับแรงกด)")
    print(f"  Q_tens  = {Q_tens:.2f} kN  (กำลังรับแรงดึง)")

    print("\n[2] ค่าเรขาคณิตและสูตร")
    print(f"  n       = {n} ต้น")
    print(f"  e₁ = e₂ = s/2 = {e1:.4f} m")
    print(f"  Σeᵢ²   = 2·e² = {sum_e2:.6f} m²")
    print(f"  สูตร:   Pᵢ = P/n  ±  M·eᵢ / Σeᵢ²")
    print(f"  P_avg  = {P}/{n} = {P_avg:.3f} kN")
    print(f"  ΔP     = {M}×{e1:.4f}/{sum_e2:.6f} = {delta:.3f} kN")

    print("\n[3] แรงในเสาเข็ม")
    print(f"  P₁ (กดสูงสุด)  = {P_avg:.3f} + {delta:.3f} = {P1:.3f} kN")
    p2_sign = "+" if delta <= 0 else "−"
    print(f"  P₂ (กดน้อย/ดึง) = {P_avg:.3f} − {delta:.3f} = {P2:.3f} kN"
          + ("  ← แรงดึง!" if P2 < 0 else ""))

    print("\n[4] ระยะเยื้องศูนย์")
    print(f"  e = M/P = {M}/{P} = {e_ecc:.4f} m")
    print(f"  kern    = s/6  = {s:.3f}/6 = {kern:.4f} m")
    if ok_kern:
        print(f"  e ≤ kern  → ไม่มีแรงดึง (กดทั้ง 2 ต้น)")
    else:
        print(f"  e > kern  → เกิดแรงดึงในเสาเข็มต้นที่ 2 ({P2:.2f} kN)")

    print("\n[5] การตรวจสอบ")
    print(check(ok_comp, f"P₁ = {P1:.2f} kN ≤ Q_comp = {Q_comp:.2f} kN"))
    if P2 < 0:
        print(check(ok_tens,
              f"P₂ = {P2:.2f} kN  |P₂| ≤ Q_tens = {Q_tens:.2f} kN"))
    else:
        print(check(True, f"P₂ = {P2:.2f} kN (กด) ≥ 0"))

    print()
    if all_ok:
        print("  ► ผ่านการตรวจสอบทั้งหมด")
    else:
        print("  ► ไม่ผ่าน — ดูคำแนะนำด้านล่าง")
        if not ok_comp:
            needed_s = math.sqrt(2 * M / (Q_comp - P / n))
            print(f"    • เพิ่ม Q_comp หรือเพิ่มระยะ s ≥ {needed_s:.3f} m")
        if not ok_tens and P2 < 0:
            needed_qt = abs(P2)
            print(f"    • ต้องการ Q_tens ≥ {needed_qt:.2f} kN "
                  f"หรือเพิ่มจำนวนเสาเข็มเป็น 3 ต้น")

    print(SEP)


def draw_diagram():
    """วาด ASCII diagram แสดงตำแหน่งเสาเข็มและทิศทางแรง"""

    e_ecc = M / P if P != 0 else 0
    e     = s / 2
    P_avg = P / 2
    delta = M * e / (2 * e**2)
    P1    = P_avg + delta
    P2    = P_avg - delta

    bar_max = 12
    def bar(v, mx):
        filled = int(abs(v) / mx * bar_max) if mx > 0 else 0
        filled = min(filled, bar_max)
        return ("█" * filled).ljust(bar_max) if v >= 0 else ("░" * filled).ljust(bar_max)

    mx = max(abs(P1), abs(P2), 1)
    b1 = bar(P1, mx)
    b2 = bar(P2, mx)

    p1_label = f"P₁={P1:6.1f} kN"
    p2_label = f"P₂={P2:6.1f} kN {'← ดึง' if P2 < 0 else ''}"

    ecc_offset = int(e_ecc / (s / 2) * 4)
    ecc_offset = max(-8, min(8, ecc_offset))
    arrow_col  = 20 + ecc_offset

    top_line   = " " * arrow_col + "↓ P+M"
    pile_line  = f"  ■{'─'*8}■   ← pile cap"
    pile1_line = f"  │{' '*8}│"
    pile2_line = f"  ●{' '*8}●   ← เสาเข็ม"
    bar1_line  = f"  {b1}  {p1_label}"
    bar2_line  = f"  {' '*bar_max}  {b2}  {p2_label}"

    print("\n[6] Diagram (แผนผังเสาเข็มด้านข้าง)")
    print()
    print(f"  {'─'*40}")
    print(f"  {'':>20}↓ P={P:.0f} kN, M={M:.0f} kN·m")
    print(f"  {'':>20}(e={e_ecc:.3f} m)")
    print(f"  {'─'*40}")
    print(f"  ┌{'─'*12}┐  ← pile cap")
    print(f"  │            │")
    print(f"  └──────┬─────┘")
    print(f"         │")
    print(f"    ─────┼─────  ← ระดับหัวเสาเข็ม")
    print(f"    │         │")
    print(f"    ●         ●")
    print(f"   เสา1      เสา2")
    print(f"  |←── s={s:.2f} m ──→|")
    print()
    print(f"  แรงในเสาเข็ม:")
    print(f"  เสา1 [{'█'*int(P1/mx*10):10s}] {P1:7.2f} kN (กด)")
    if P2 >= 0:
        print(f"  เสา2 [{'█'*int(P2/mx*10):10s}] {P2:7.2f} kN (กด)")
    else:
        print(f"  เสา2 [{'░'*int(abs(P2)/mx*10):10s}] {P2:7.2f} kN (ดึง)")
    print(SEP)


if __name__ == "__main__":
    design()
    draw_diagram()
