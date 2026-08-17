# Lab 17 - Submission Notes

## Ket qua va phan tich

Benchmark student dat **11/11 PASS (100%)**, trong khi baseline no-memory dat **2/11 (18,2%)**: chi E01 va E10 (short-term) PASS. Khong co layer student nao thap nhat: short-term 2/2, long-term 4/4, episodic 2/2, semantic 2/2 va mixed 1/1.

Case retrieve nhieu token nhat la **E03 (1.348 token)**. E07 bat buoc ket hop **long-term** (`Python`, preference cua Minh) va **semantic** (`Idempotency-Key`, payment retry policy); mot layer rieng le khong du evidence.

Memory-enabled giam trung binh **14,2% token**, con no-memory giam **81,8%**. No-memory reduction cao vi phan lon context bi bo hoan toan nen hit rate chi 18,2%; token reduction chi co y nghia khi doc cung evidence hit rate.

Long-term la layer quan trong nhat trong bo test nay: E02, E03, E08 va E09 kiem tra cross-session preference, open loop, recency/scope va user isolation, tong 20 diem. O E08, rang buoc moi theo project `BLUEBIRD-42` (`TypeScript`/`NestJS`) thang preference Python cu trong dung scope; fact cu van duoc giu provenance cho `ORCHID-27`.

E10 cho thay compaction phai giu state/constraint, khong chi tom tat van xuoi. Sliding memory loai raw turn cu nhung durable note van giu `REVIEW-DEADLINE-1600`, `Friday`, `16:00`; buffer thi tang token tuyen tinh.

## Trade-off va guardrail

Zep Context Block va user graph cung cap cross-session relevance, provenance, recency va namespace managed, giam cong tu lap retrieval pipeline. Redis + Qdrant minh bach, tu chu chi phi/schema/TTL va co the chay local, nhung phai tu giai quyet extraction, conflict, ranking, isolation, deletion va van hanh index.

De chong memory poisoning, moi durable write phai qua consent/type allowlist, PII minimization, scope user/org/shared ro rang, va luu source, timestamp, confidence, validity. Preference/rang buoc tac dong cao can human review; thong tin mau thuan dung recency + scope, khong xoa provenance. Heartbeat chi deduplicate/expire/recap, tuyet doi khong tu cap quyen hay ghi instruction moi.

## Evidence

- `submission/long_term.png`: E02, E03, E08, E09
- `submission/episodic.png`: E04, E05
- `submission/semantic.png`: E06, E11
- `submission/privacy.png`: post-deletion verification (`Zep user absent: True`, Redis keys `0`)
