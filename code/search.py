import json
from pathlib import Path
from rapidfuzz import fuzz
import re


def load_data():
 
  base_dir = Path(__file__).resolve().parent.parent
  file_path = base_dir / "data" / "filter.json"

  with open(file_path, "r", encoding="utf-8") as f:
    return json.load(f)

# print(load_data())

def search_filter(query: str, filter: list):
  if not query.strip():
    return filter

  scored_results = []
  for item in filter:
    # รวมชื่อหนังกับแนวหนังเข้าด้วยกันเพื่อใช้เทียบคำค้นหา
    searchable_text = f"{item['title']} {item['use_case']} {item['template']}".lower()
    score = fuzz.partial_ratio(query.lower(), searchable_text)

    if score >= 60:
      scored_results.append((score, item))  # เก็บเป็นคู่ (คะแนน, ข้อมูล)

  # เรียงลำดับตามตัวแรกของ Tuple (score) จากมากไปน้อย
  scored_results.sort(key=lambda x: x[0], reverse=True)

  # ดึงเฉพาะตัวข้อมูล (item) คืนกลับไป
  return [item for score, item in scored_results]



def find_placeholders(text: str) -> list:
  # ดึงข้อความทุกตัวที่อยู่ข้างใน { } ออกมาเป็น List
  return re.findall(r"\{(.*?)\}", text)


def fill_template(text: str, user_inputs: dict) -> str:
  result = text
  for key, val in user_inputs.items():
    # ต้องใส่ปีกกาครอบ key กลับเข้าไปตอน replace เช่น "{NAME}" -> "Sirisart"
    result = result.replace(f"{{{key}}}", val)
  return result


# find_placeholders("Hello {NAME}, from {CITY}")  --> ได้ ['NAME', 'CITY']
# fill_template("Hello {NAME}", {"NAME": "Alex"}) --> ได้ "Hello Alex"

# terminal searchEngine test
if __name__ == "__main__":

    filter = load_data()

    query = input("Search :")
    results = search_filter(query,filter)

    if not results:
      print("nothing found")
      exit()

    for index, item in enumerate(results,start=1):
        
        print(f"[{index}] {item['template']}  -->  {item['use_case']}")

    choice = int(input("Select number :"))
    if type(choice) == int and choice > 0:
        
      if choice > len(results) and choice > 0:
        print("Error")
        exit()

      select = results[choice -1]

      print(f"Expected: {select['expected_output']}\n")

      params = find_placeholders(select['template'])

      user_input = {}
      for p in params:
        val = input(f"Enter {p}: ")
        user_input[p] = val

      final_command = fill_template(select['template'],user_input)
      print("\nReady to inject:", final_command)

    else:
      print("Error wrong choice");
      exit()