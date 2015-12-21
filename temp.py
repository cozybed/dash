from gameobjects.vector2 import Vector2

def judge(p1, p2, p3, p4):
        if p1.x != p2.x and p3.x == p4.x:
            k1 = (p1.y - p2.y) / (p1.x - p2.x)
            b1 = (p1.x * p2.y - p1.y * p2.x) / (p1.x - p2.x)
            x = p3.x
            y = k1 * x + b1
        elif p1.x == p2.x and p3.x != p4.x:
            k2 = (p3.y - p4.y) / (p3.x - p4.x)
            b2 = (p3.x * p4.y - p3.y * p4.x) / (p3.x - p4.x)
            x = p1.x
            y = k2 * x + b2
        elif p1.x != p2.x and p3.x != p4.x:
            k1 = (p1.y - p2.y) / (p1.x - p2.x)
            k2 = (p3.y - p4.y) / (p3.x - p4.x)
            if k1 == k2:
                return 0
            b1 = (p1.x * p2.y - p1.y * p2.x) / (p1.x - p2.x)
            b2 = (p3.x * p4.y - p3.y * p4.x) / (p3.x - p4.x)
            x = (b2 - b1) / (k1 - k2)
            y = k1 * x + b1
        else:
            return 0
        if x >= min(p1.x, p2.x) and x <= max(p1.x, p2.x) and y >= min(p1.y, p2.y) and y <= max(p1.y, p2.y) and x >= min(p3.x, p4.x) and x <= max(p3.x, p4.x) and y >= min(p3.y, p4.y) and y <= max(p3.y, p4.y):
            return 1
        else:
            return 0

#2 [Vector2(320.533114382, 265.835153386), Vector2(348.279246614, 294.647514382), Vector2(319.466885618, 322.393646614), Vector2(291.720753386, 293.581285618)] [Vector2(332.8, 308.0), Vector2(373.8, 308.0), Vector2(373.8, 323.0), Vector2(332.8, 323.0)]
print judge((348.283713, 292.323886), (320.177714, 320.785313), (331.6, 308), (372.6, 308))
