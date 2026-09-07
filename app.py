import streamlit as st


def initialize_state() -> None:
    """세션에서 사용할 할 일 목록을 처음 한 번만 준비합니다."""
    if "todos" not in st.session_state:
        st.session_state.todos = []
    for todo in st.session_state.todos:
        if "status" not in todo:
            todo["status"] = "완료" if todo.get("completed", False) else "미완료"


def add_todo(title: str) -> None:
    """새 할 일을 세션 목록에 추가합니다."""
    cleaned_title = title.strip()
    if cleaned_title:
        st.session_state.todos.append(
            {
                "id": st.session_state.next_todo_id,
                "title": cleaned_title,
                "completed": False,
                "status": "미완료",
            }
        )
        st.session_state.next_todo_id += 1


def toggle_todo(todo_id: int, completed: bool) -> None:
    """지정한 할 일의 완료 상태를 변경합니다."""
    for todo in st.session_state.todos:
        if todo["id"] == todo_id:
            todo["completed"] = completed
            todo["status"] = "완료" if completed else "미완료"
            break


def update_todo_status(todo_id: int, status: str) -> None:
    """지정한 할 일의 진행 상태를 변경합니다."""
    for todo in st.session_state.todos:
        if todo["id"] == todo_id:
            todo["status"] = status
            todo["completed"] = status == "완료"
            break


def delete_todo(todo_id: int) -> None:
    """지정한 할 일을 목록에서 삭제합니다."""
    st.session_state.todos = [
        todo for todo in st.session_state.todos if todo["id"] != todo_id
    ]


def main() -> None:
    st.set_page_config(page_title="할 일 관리", page_icon="✅", layout="centered")
    initialize_state()

    if "next_todo_id" not in st.session_state:
        st.session_state.next_todo_id = 1

    st.title("할 일 관리")
    st.caption("오늘 해야 할 일을 한 곳에서 정리해 보세요.")

    with st.form("add_todo_form", clear_on_submit=True):
        new_todo = st.text_input("새 할 일", placeholder="예: 주간 보고서 작성")
        submitted = st.form_submit_button("할 일 추가", use_container_width=True)

    if submitted:
        if new_todo.strip():
            add_todo(new_todo)
            st.success("할 일을 추가했습니다.")
        else:
            st.warning("할 일 내용을 입력해 주세요.")

    total_count = len(st.session_state.todos)
    completed_count = sum(
        todo.get("status") == "완료" for todo in st.session_state.todos
    )
    in_progress_count = sum(
        todo.get("status") == "진행중" for todo in st.session_state.todos
    )
    incomplete_count = total_count - completed_count - in_progress_count

    summary_columns = st.columns(4)
    summary_columns[0].metric("전체", total_count)
    summary_columns[1].metric("미완료", incomplete_count)
    summary_columns[2].metric("진행중", in_progress_count)
    summary_columns[3].metric("완료", completed_count)

    st.subheader("목록")
    if not st.session_state.todos:
        st.info("아직 등록된 할 일이 없습니다.")
        return

    for todo in st.session_state.todos:
        todo_columns = st.columns([0.12, 0.48, 0.25, 0.15])
        is_completed = todo_columns[0].checkbox(
            "완료",
            value=todo.get("status") == "완료",
            key=f"completed_{todo['id']}",
            label_visibility="collapsed",
        )
        if is_completed != (todo.get("status") == "완료"):
            toggle_todo(todo["id"], is_completed)
            st.rerun()

        title = f"~~{todo['title']}~~" if todo.get("status") == "완료" else todo["title"]
        todo_columns[1].markdown(title)
        status = todo_columns[2].selectbox(
            "상태",
            options=["미완료", "진행중", "완료"],
            index=["미완료", "진행중", "완료"].index(todo.get("status", "미완료")),
            key=f"status_{todo['id']}",
            label_visibility="collapsed",
        )
        if status != todo.get("status", "미완료"):
            update_todo_status(todo["id"], status)
            st.rerun()

        if todo_columns[3].button("삭제", key=f"delete_{todo['id']}"):
            delete_todo(todo["id"])
            st.rerun()


if __name__ == "__main__":
    main()