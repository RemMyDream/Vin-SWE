# Pre-check — bản trình bày trực tiếp

Kiểm tra ngày 8/11/2026. Bản dùng để trình bày: `COMP5320_Agentic_Security.pptx` và PDF cùng tên, **29 slide**. Speaker notes đã đồng bộ trong `COMP5320_Agentic_Security_Speaker_Notes.md`.

## Nội dung và cấu trúc

- Đã bỏ nhãn Chapter 9, prefix §9.x, thời lượng, Member 1/2, LO và các nhãn phân công khỏi nội dung hiển thị.
- Mục lục: **Part 1 / 1.1–1.3** và **Part 2 / 2.1–2.6**.
- Trang mở đầu: **Bui Khac Chien — V2026003377**, cùng ba ô `[Name] — [Student ID]` có thể sửa trực tiếp.
- Nội dung: **Montserrat Medium**; tiêu đề và thông tin nhấn mạnh: **Poppins**; code: Consolas.
- PowerPoint chứa **10 font parts được nhúng**. Kiểm tra font thực tế trong PDF chỉ có Poppins, Montserrat và Consolas; không có nội dung bị thay bằng Calibri/Arial.

## Kiểm tra ví dụ, luồng và phân tích — 9/9 nhóm đạt

Mỗi dòng dưới đây có ví dụ, chuỗi hành động và giải thích cơ chế ngay trên slide. Các slide case chi tiết còn có trust boundary, nguyên nhân, impact và control hạn chế luồng.

| Nhóm | Slide | Ví dụ / flow | Phân tích nguyên nhân | Nguồn / trạng thái |
|---|---:|---|---|---|
| Direct prompt injection | 10 | Task độc hại → agent làm theo → đọc SSH key + gọi network tool → gửi dữ liệu ra ngoài | Nội dung task bị coi là quyền cho một hành động; cần giới hạn quyền đọc và đầu ra | Ví dụ giả định, defanged; [OWASP LLM01](https://genai.owasp.org/llm-top-10/) |
| Indirect prompt injection | 10–13 | Public issue → agent đọc private repo → public PR chứa dữ liệu | Credential nối đầu vào công khai, dữ liệu riêng tư và đầu ra công khai | GitHub MCP, nghiên cứu có kiểm soát; [Invariant](https://invariantlabs.ai/blog/mcp-github-vulnerability) |
| Confused deputy | 17–18 | Ticket → developer agent → service_role đọc private tokens → ghi về ticket → customer đọc | Customer có quyền trên ticket riêng; deputy mượn quyền database mạnh hơn | Supabase/Cursor, dummy-data demonstration; [General Analysis](https://generalanalysis.com/blog/supabase-mcp-blog/) |
| Instruction-hierarchy violation | 21 | File/README → instruction giả mạo → đổi auto-approval → shell execution | Dữ liệu repo điều khiển cơ chế phê duyệt của agent; dòng SYSTEM vẫn là dữ liệu | Copilot CVE-2025-53773, đã vá; [Rehberger](https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/) |
| Covert-channel exfiltration | 22 | Source file → đọc secret → DNS lookup chứa dữ liệu mã hoá → DNS của attacker nhận tên truy vấn | Allowlist command bỏ sót tác động mạng và destination/argument do attacker kiểm soát | Claude Code CVE-2025-55284, vá ở 1.0.4; [advisory](https://github.com/anthropics/claude-code/security/advisories/GHSA-x5gv-jw7f-j6xj) |
| Configuration supply chain | 23 | Rule bị đầu độc → agent nạp guidance → HTML chứa script ngoài ý muốn → rủi ro khi trang chạy | Shared config được dùng như policy; Unicode che giấu instruction | Rules File Backdoor, controlled demonstration; [Pillar](https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents) |
| MCP tool poisoning | 24 | Tool metadata → planning context → trusted file tool → secret trong argument gửi đến server độc hại | Metadata của một trust domain chỉ đạo tool có quyền ở domain khác | Controlled demonstration; [Invariant](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) |
| MCP server compromise | 25 | Cài connector giả → cập nhật 1.0.16 → gọi email tool hợp lệ → server tự thêm BCC | Hành vi độc hại nằm trong implementation; không cần model bị prompt injection | postmark-mcp không chính thức; [Postmark alert](https://postmarkapp.com/blog/information-regarding-malicious-postmark-mcp-package) |
| Autonomous amplification | 26 | Record có hidden text → agent đổi mục tiêu → discovery/delegation gọi agent khác → downstream authority được dùng | Nguồn dữ liệu ít tin cậy bị mất provenance khi chuyển thành task cho agent khác | ServiceNow/AppOmni research; [AppOmni](https://appomni.com/ao-labs/ai-agent-to-agent-discovery-prompt-injection/) |

**Bổ sung kiểm tra:** slide 6 có flow minh hoạ cho cả sáu chữ STRIDE. Slide 13 có mini-flow riêng cho issue, README/code comment, webpage, email, rules file và tool metadata; phần bên trái giải thích cơ chế chung. Slide 20 là bản đồ tổng quan, nối trực tiếp tới các case 21–26.

Giữ nguyên các phân biệt cần thiết: case nghiên cứu không được trình bày như customer breach; ví dụ trực tiếp là giả định; Rules File Backdoor quan sát thay đổi code, không khẳng định người dùng thực tế đã chạy script; postmark-mcp không phải dịch vụ Postmark chính thức; amplification phụ thuộc quyền và mức tin cậy ở từng agent.

## Kiểm tra file cuối

| Kiểm tra | Kết quả |
|---|---|
| PowerPoint / PDF | 29 slide / 29 trang |
| Slide-note sections | 29; nội dung khớp file speaker notes |
| Scan metadata hiển thị | 0 nhãn Chapter 9, §9.x, Member, LO, thời lượng hoặc Part 3 |
| Package validation | **All validations PASSED!** |
| Text-fit audit | **668 vùng chữ, 0 overflow**; đo glyph hiển thị từng dòng, bỏ khoảng trắng cuối dòng soft-wrap |
| Font portability | 10 embedded font parts; font PDF thực tế đúng các family đã chọn |
| Visual review | Render PowerPoint 1600 × 900; đã xem từng slide và contact sheet của bản cuối |
| Attack execution | Không chạy hoặc tải exploit; chỉ mô tả flow và payload defanged |

Build tái lập từ `lecture/build`: `python build_deck.py`, sau đó `python finalize_live.py` để nhúng font và xuất PDF. Ảnh kiểm tra nằm tại `lecture/build/_render_live/`; contact sheets `grid-01.png` đến `grid-08.png`.

**Kết luận: sẵn sàng để nhóm điền ba tên/mã sinh viên còn lại và trình bày.**
