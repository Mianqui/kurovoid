import json

log_file = "/home/jhonnikek/.gemini/antigravity-cli/brain/62ed1fde-dc05-438b-a394-4b9ca8aea45a/.system_generated/logs/transcript_full.jsonl"
with open(log_file, "r") as f:
    lines = f.readlines()

for line in lines:
    try:
        data = json.loads(line)
        if data.get("type") == "GENERIC" and data.get("source") == "MODEL":
            content = data.get("content", "")
            if "Total Lines: 333" in content:
                print("FOUND!")
                # Split at 'space.\n'
                idx = content.find("leading space.\n")
                if idx != -1:
                    lines_content = content[idx + len("leading space.\n"):]
                    clean_lines = []
                    for cl in lines_content.split("\n"):
                        if cl.strip():
                            if ": " in cl:
                                clean_lines.append(cl.split(": ", 1)[1])
                            else:
                                clean_lines.append(cl)
                    with open("templates/index_original.html", "w") as out:
                        out.write("\n".join(clean_lines))
                    print("Extracted!")
                    break
    except Exception as e:
        print("Error:", e)
