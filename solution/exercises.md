# Ngay 1 - Bai Tap & Phan Anh
## Nen Tang LLM API | Phieu Thuc Hanh

**Thoi luong:** 1:30 gio  
**Cau truc:** Lap trinh cot loi (60 phut) -> Bai tap mo rong (30 phut)

---

## Phan 1 - Lap Trinh Cot Loi (0:00-1:00)

Da trien khai cac TODO trong `solution.py` va chay kiem thu bang:

```bash
pytest tests/ -v
```

---

## Phan 2 - Bai Tap Mo Rong (1:00-1:30)

### Bai tap 2.1 - Do Nhay Cua Temperature

Goi `call_openai` voi cac gia tri temperature 0.0, 0.5, 1.0 va 1.5 su dung prompt **"Hay ke cho toi mot su that thu vi ve Viet Nam."**

**Ban nhan thay quy luat gi qua bon phan hoi?** (2-3 cau)
> Khi temperature thap, cau tra loi thuong on dinh, truc tiep va it bat ngo hon; neu goi lai nhieu lan thi noi dung co xu huong lap lai. Khi temperature tang len, mo hinh de dua ra cach dien dat da dang hon, co the sang tao hon nhung cung tang rui ro lan man hoac kem nhat quan.

**Ban se dat temperature bao nhieu cho chatbot ho tro khach hang, va tai sao?**
> Toi se chon khoang 0.2 den 0.5 cho chatbot ho tro khach hang. Muc nay giup cau tra loi tu nhien vua du, nhung van uu tien tinh chinh xac, nhat quan va it tao ra thong tin qua sang tao.

---

### Bai tap 2.2 - Danh Doi Chi Phi

Kich ban: 10.000 nguoi dung hoat dong moi ngay, moi nguoi thuc hien 3 lan goi API, moi lan trung binh ~350 token output.

**Uoc tinh xem GPT-4o dat hon GPT-4o-mini bao nhieu lan cho workload nay:**
> Tong so token output moi ngay la 10.000 * 3 * 350 = 10.500.000 token. GPT-4o co gia $0.010 / 1K token nen chi phi output khoang $105/ngay; GPT-4o-mini co gia $0.0006 / 1K token nen chi phi output khoang $6.30/ngay. Vi vay GPT-4o dat hon GPT-4o-mini khoang 16.67 lan.

**Mo ta mot truong hop ma chi phi cao hon cua GPT-4o la xung dang, va mot truong hop GPT-4o-mini la lua chon tot hon:**
> GPT-4o xung dang khi tac vu can chat luong lap luan cao, do chinh xac tot va cau tra loi co anh huong lon, vi du phan tich tai lieu phuc tap, tu van quy trinh nghiep vu, hoac xu ly yeu cau khach hang kho. GPT-4o-mini phu hop hon cho tac vu khoi luong lon, rut gon, phan loai, hoi dap FAQ, chatbot noi bo hoac cac cau hoi don gian can toc do va chi phi thap.

---

### Bai tap 2.3 - Trai Nghiem Nguoi Dung voi Streaming

**Streaming quan trong nhat trong truong hop nao, va khi nao thi non-streaming lai phu hop hon?** (1 doan van)
> Streaming quan trong nhat khi phan hoi dai hoac nguoi dung can cam giac he thong dang xu ly ngay lap tuc, vi du chatbot tu van, tro ly lap trinh, viet noi dung dai, hoac giai thich tung buoc. Viec hien thi token lien tuc lam giam cam giac cho doi va giup nguoi dung co the doc som truoc khi cau tra loi hoan tat. Non-streaming phu hop hon khi can ket qua ngan, can xu ly toan bo response truoc khi hien thi, can validate JSON/schema, hoac khi ung dung chi can mot ket qua hoan chinh de dung trong pipeline tu dong.

---

## Danh Sach Kiem Tra Nop Bai

- [x] Tat ca tests pass: `pytest tests/ -v`
- [x] `call_openai` da trien khai va kiem thu
- [x] `call_openai_mini` da trien khai va kiem thu
- [x] `compare_models` da trien khai va kiem thu
- [x] `streaming_chatbot` da trien khai va kiem thu
- [x] `retry_with_backoff` da trien khai va kiem thu
- [x] `batch_compare` da trien khai va kiem thu
- [x] `format_comparison_table` da trien khai va kiem thu
- [x] `exercises.md` da dien day du
- [x] Sao chep bai lam vao folder `solution` va dat ten theo quy dinh
