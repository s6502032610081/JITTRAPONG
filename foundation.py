import numpy as np

def calculate_pile_reactions(P, Mx_ext, My_ext, pile_coords):
    """
    P: Axial Load จากเสา (kg)
    Mx_ext, My_ext: Moment ภายนอก (kg-m)
    pile_coords: List ของพิกัดเสาเข็ม [(x1, y1), (x2, y2), ...] วัดจากศูนย์กลางเสาตอหม้อ
    """
    n = len(pile_coords)
    coords = np.array(pile_coords)
    
    # 1. หาจุดศูนย์ถ่วง (C.G.) ของกลุ่มเข็ม
    cg_x = np.mean(coords[:, 0])
    cg_y = np.mean(coords[:, 1])
    
    # 2. คำนวณโมเม้นต์ส่วนเพิ่มจากการเยื้องศูนย์ (M = P * e)
    # e คือระยะห่างจาก C.G. กลุ่มเข็ม ถึง ศูนย์กลางเสาตอหม้อ (0,0)
    ex = 0 - cg_x 
    ey = 0 - cg_y
    
    M_total_x = Mx_ext + (P * ey)
    M_total_y = My_ext + (P * ex)
    
    # 3. คำนวณ Sum of Squares (Ixx, Iyy ของกลุ่มเข็ม)
    # ระยะห่างเสาเข็มแต่ละต้นเทียบกับ C.G. กลุ่มเข็ม
    dx = coords[:, 0] - cg_x
    dy = coords[:, 1] - cg_y
    
    sum_x2 = np.sum(dx**2)
    sum_y2 = np.sum(dy**2)
    
    # 4. คำนวณแรงปฏิกิริยาในเข็มแต่ละต้น
    reactions = []
    for i in range(n):
        # สูตร: P/n + (Mx * y / sum_y2) + (My * x / sum_x2)
        # หมายเหตุ: การใช้เครื่องหมาย +/- ขึ้นอยู่กับทิศทางพิกัด
        Ri = (P / n) + (M_total_x * dy[i] / sum_y2) + (M_total_y * dx[i] / sum_x2)
        reactions.append(Ri)
        
    return reactions, cg_x, cg_y, M_total_x, M_total_y

# --- ตัวอย่างการใช้งาน (Example) ---
load_p = 50000  # 50 ตัน
mx_ext = 0      # ไม่มีโมเม้นต์ภายนอก
my_ext = 0

# สมมติฐานรากเข็มคู่ เดิมควรอยู่ที่ x = -0.4, 0.4 แต่ตอกเบี้ยวไปทางขวา 10 ซม. ทั้งคู่
# พิกัดเข็มที่ตอกจริง (เทียบกับศูนย์กลางตอหม้อ 0,0)
piles = [
    (-0.30, 0.0), # ต้นที่ 1 (เบี้ยวจาก -0.4 เป็น -0.3)
    ( 0.50, 0.0)  # ต้นที่ 2 (เบี้ยวจาก 0.4 เป็น 0.5)
]

res, cg_x, cg_y, mx_t, my_t = calculate_pile_reactions(load_p, mx_ext, my_ext, piles)

print(f"--- ผลการคำนวณ ---")
print(f"จุด C.G. กลุ่มเข็มอยู่ที่: x = {cg_x:.3f} m, y = {cg_y:.3f} m")
print(f"Moment รวมที่เกิดขึ้น: Mx = {mx_t:.2f} kg-m, My = {my_t:.2f} kg-m")
print("-" * 30)
for i, r in enumerate(res):
    print(f"เสาเข็มต้นที่ {i+1} รับแรง: {r:,.2f} kg")
