
import json
import random
from faker import Faker

fake = Faker("ko_KR")

banks = ["국민은행", "신한은행", "우리은행", "하나은행", "농협은행", "카카오뱅크", "토스뱅크"]
product_suffix = ["플러스정기예금", "스마트정기예금", "프리미엄예금", "더드림예금", "슈퍼정기예금", "청년우대예금"]
join_members = ["개인", "개인/법인", "청년", "시니어"]
join_ways = ["비대면", "대면", "온라인", "모바일앱", "전화"]
spcl_conds = ["청년우대 조건 있음", "인터넷 가입 시 우대", "자동이체 등록 시 우대", "없음"]
save_terms = [6, 12, 24, 36]
rate_type_names = ["단리", "복리"]

used_codes = set()

def generate_unique_code():
    while True:
        code = f"{random.randint(100, 999)}-{fake.lexify(text='???').upper()}"
        if code not in used_codes:
            used_codes.add(code)
            return code

products = []
options = []

for _ in range(30):
    code = generate_unique_code()
    bank = random.choice(banks)
    product_name = f"{bank} {random.choice(product_suffix)}"
    
    product = {
        "fin_prdt_cd": code,
        "kor_co_nm": bank,
        "fin_prdt_nm": product_name,
        "etc_note": fake.sentence(),
        "join_deny": random.choice([1, 2, 3]),
        "join_member": random.choice(join_members),
        "join_way": random.choice(join_ways),
        "spcl_cnd": random.choice(spcl_conds)
    }
    products.append(product)

    for _ in range(random.randint(1, 3)):
        term = str(random.choice(save_terms))
        rate = round(random.uniform(1.5, 3.5), 2)
        rate2 = round(rate + random.uniform(0.1, 1.0), 2)
        option = {
            "product": code,
            "intr_rate_type_nm": random.choice(rate_type_names),
            "save_trm": f"{term}개월",
            "intr_rate": rate,
            "intr_rate2": rate2
        }
        options.append(option)

dummy_data = {
    "products": products,
    "options": options
}
## 저장
with open("dummy_deposit_products.json", "w", encoding="utf-8") as f:
    json.dump(dummy_data, f, ensure_ascii=False, indent=2)
