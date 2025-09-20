import streamlit as st
import json
import os

# --- ĐƯỜNG DẪN FILE JSON ---
STUDENTS_FILE = "students.json"
LESSONS_FILE = "lessons.json"

# --- HÀM ĐỌC FILE JSON ---
def load_json_file(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception as e:
            st.warning(f"⚠️ Lỗi đọc file {filename}: {e}")
            return []
    return []

# --- HÀM GHI FILE JSON ---
def save_json_file(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"❌ Lỗi ghi file {filename}: {e}")

# --- KHỞI TẠO SESSION STATE TỪ FILE JSON ---
if 'students' not in st.session_state:
    st.session_state.students = load_json_file(STUDENTS_FILE)

if 'lessons' not in st.session_state:
    st.session_state.lessons = load_json_file(LESSONS_FILE)

# --- NÚT THÊM DỮ LIỆU DEMO ---
if st.button("🧪 Thêm dữ liệu demo (3 học sinh + 5 buổi học)"):
    demo_students = [
        {"id": 1, "name": "Nguyễn Văn A", "grade": "Lớp 10", "subject": "Toán", "parent_phone": "0912345678"},
        {"id": 2, "name": "Trần Thị B", "grade": "Lớp 11", "subject": "Lý", "parent_phone": "0987654321"},
        {"id": 3, "name": "Lê Văn C", "grade": "Lớp 9", "subject": "Anh", "parent_phone": "0909090909"}
    ]
    demo_lessons = [
        {"student_name": "Nguyễn Văn A", "date": "2025-06-10", "time": "18:00:00", "notes": "Ôn tập chương 1 — tiến bộ tốt."},
        {"student_name": "Nguyễn Văn A", "date": "2025-06-12", "time": "18:00:00", "notes": "Làm bài kiểm tra — đạt 8/10."},
        {"student_name": "Trần Thị B", "date": "2025-06-11", "time": "19:00:00", "notes": "Chưa làm bài tập — nhắc nhở."},
        {"student_name": "Lê Văn C", "date": "2025-06-10", "time": "17:00:00", "notes": "Phát âm tiến bộ — khen thưởng."},
        {"student_name": "Lê Văn C", "date": "2025-06-13", "time": "17:00:00", "notes": "Kiểm tra từ vựng — đạt 9/10."}
    ]
    st.session_state.students = demo_students
    st.session_state.lessons = demo_lessons
    save_json_file(STUDENTS_FILE, demo_students)
    save_json_file(LESSONS_FILE, demo_lessons)
    st.success("🎉 Đã thêm dữ liệu demo! Tải lại trang để xem.")

# --- TIÊU ĐỀ ---
st.title("📚 Gia Sư Manager - Ngày 2")
st.write("### Phiên bản nâng cấp: Dữ liệu được lưu vào file JSON — tắt web vẫn còn!")

# --- TAB 1: QUẢN LÝ HỌC SINH ---
st.header("➕ Thêm Học Sinh Mới")

with st.form("form_add_student"):
    name = st.text_input("Tên học sinh")
    grade = st.selectbox("Lớp", ["Lớp 6", "Lớp 7", "Lớp 8", "Lớp 9", "Lớp 10", "Lớp 11", "Lớp 12"])
    subject = st.text_input("Môn học")
    parent_phone = st.text_input("SĐT phụ huynh")
    submitted = st.form_submit_button("✅ Thêm học sinh")

    if submitted and name.strip():
        new_student = {
            "id": len(st.session_state.students) + 1,
            "name": name.strip(),
            "grade": grade,
            "subject": subject.strip(),
            "parent_phone": parent_phone.strip()
        }
        st.session_state.students.append(new_student)
        save_json_file(STUDENTS_FILE, st.session_state.students)  # 🟢 GHI VÀO FILE
        st.success(f"🎉 Đã thêm học sinh: {name}")


# --- HIỂN THỊ DANH SÁCH HỌC SINH + NÚT XÓA ---
if st.session_state.students:
    st.subheader("📋 Danh sách học sinh")
    for i, student in enumerate(st.session_state.students):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{student['name']}** — {student['grade']} — {student['subject']} — 📞 {student['parent_phone']}")
        with col2:
            if st.button("✏️ Sửa", key=f"edit_{i}"):
                st.info("Tính năng sửa sẽ có trong phiên bản sau!")
        with col3:
            if st.button("🗑️ Xóa", key=f"delete_{i}"):
                # Xóa học sinh khỏi danh sách
                deleted_student = st.session_state.students.pop(i)
                # Ghi đè lại file JSON
                save_json_file(STUDENTS_FILE, st.session_state.students)
                # Xóa luôn các buổi học liên quan đến học sinh này
                st.session_state.lessons = [
                    lesson for lesson in st.session_state.lessons
                    if lesson["student_name"] != deleted_student["name"]
                ]
                save_json_file(LESSONS_FILE, st.session_state.lessons)
                st.success(f"🗑️ Đã xóa học sinh: {deleted_student['name']}")
                st.rerun()  # Làm mới trang để cập nhật giao diện
else:
    st.info("📝 Chưa có học sinh nào — hãy thêm ngay!")

# --- TAB 2: THÊM LỊCH HỌC ---
st.header("📅 Thêm Lịch Học")

if st.session_state.students:
    student_names = [s["name"] for s in st.session_state.students]
    with st.form("form_add_lesson"):
        selected_student = st.selectbox("Chọn học sinh", student_names)
        lesson_date = st.date_input("Ngày học")
        lesson_time = st.time_input("Giờ học")
        notes = st.text_area("Ghi chú buổi học")
        submitted_lesson = st.form_submit_button("✅ Thêm lịch học")

        if submitted_lesson:
            new_lesson = {
                "student_name": selected_student,
                "date": str(lesson_date),
                "time": str(lesson_time),
                "notes": notes.strip()
            }
            st.session_state.lessons.append(new_lesson)
            save_json_file(LESSONS_FILE, st.session_state.lessons)  # 🟢 GHI VÀO FILE
            st.success(f"🎯 Đã thêm lịch học cho {selected_student} vào {lesson_date} lúc {lesson_time}")
else:
    st.warning("⚠️ Hãy thêm ít nhất 1 học sinh trước khi tạo lịch học.")

# --- HIỂN THỊ LỊCH HỌC ---
if st.session_state.lessons:
    st.subheader("🗓️ Lịch học đã tạo")
    for lesson in st.session_state.lessons:
        st.write(f"**{lesson['student_name']}** — {lesson['date']} lúc {lesson['time']} — 📝 {lesson['notes']}")
else:
    st.info("📅 Chưa có lịch học nào — hãy lên lịch ngay!")