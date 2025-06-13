
import streamlit as st

st.set_page_config(page_title="ごみ分別クイズ", page_icon="🗑️")

st.title("🧒 ごみ分別クイズ")
st.write("正しいごみの分け方を学ぼう！")

# クイズデータ（アイテム、選択肢、正解、解説）
quiz_data = [
    {
        "question": "バナナの皮はどのごみ？",
        "options": ["可燃ごみ", "不燃ごみ", "資源ごみ"],
        "answer": "可燃ごみ",
        "explanation": "バナナの皮は生ごみなので可燃ごみです。"
    },
    {
        "question": "空き缶はどのごみ？",
        "options": ["可燃ごみ", "不燃ごみ", "資源ごみ"],
        "answer": "資源ごみ",
        "explanation": "缶はリサイクルできるので資源ごみです。"
    },
    {
        "question": "割れたガラスはどのごみ？",
        "options": ["可燃ごみ", "不燃ごみ", "資源ごみ"],
        "answer": "不燃ごみ",
        "explanation": "ガラスは燃やせないので不燃ごみです。"
    },
    {
        "question": "新聞紙はどのごみ？",
        "options": ["可燃ごみ", "不燃ごみ", "資源ごみ"],
        "answer": "資源ごみ",
        "explanation": "新聞紙は紙類の資源ごみとしてリサイクルできます。"
    }
]

score = 0

st.subheader("クイズに答えてみよう！")

for i, quiz in enumerate(quiz_data):
    st.markdown(f"**Q{i+1}. {quiz['question']}**")
    user_answer = st.radio("こたえをえらんでね：", quiz["options"], key=i)
    if st.button(f"こたえあわせ {i+1}", key=f"check_{i}"):
        if user_answer == quiz["answer"]:
            st.success("⭕ せいかい！")
            score += 1
        else:
            st.error("❌ ざんねん…")
        st.info(f"💡 かいせつ：{quiz['explanation']}")

st.markdown("---")
if st.button("けっかをみる"):
    st.subheader("🎉 クイズのけっか")
    st.write(f"あなたのスコア：{score} / {len(quiz_data)}")
    if score == len(quiz_data):
        st.balloons()
        st.success("すごい！ぜんもんせいかい！")
