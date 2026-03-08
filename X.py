import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="AvoidLove", layout="centered")

FILE_NAME = "posts.json"

# ----------------------------
# データ読み書き
# ----------------------------
def load_posts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_posts(posts):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

def get_next_id(posts):
    if not posts:
        return 1
    return max(post["id"] for post in posts) + 1

# ----------------------------
# 初期表示
# ----------------------------
st.title("🌸 AvoidLove")
st.subheader("悩みを投稿する")
st.write("匿名で投稿できます。あなたの気持ちをそのまま書いてみてください。")

tag_options = [
    "回避型パートナー",
    "遠距離",
    "別れそう",
    "連絡こない",
    "自然消滅",
    "急な距離の取り方",
    "話し合いができない"
]

selected_tags = st.multiselect("① タグを選ぶ（複数可）", tag_options)

post_content = st.text_area(
    "② 悩みを書く",
    placeholder="今どんな気持ちですか？状況を教えてください...",
    height=180
)

posts = load_posts()

# 古いデータに reactions/comments/id がない場合に補完
updated = False
for i, post in enumerate(posts):
    if "id" not in post:
        post["id"] = i + 1
        updated = True
    if "reactions" not in post:
        post["reactions"] = {"共感": 0, "応援": 0, "わかる": 0}
        updated = True
    if "comments" not in post:
        post["comments"] = []
        updated = True

if updated:
    save_posts(posts)

# ----------------------------
# 投稿作成
# ----------------------------
if st.button("③ 送信する 💌"):
    if post_content.strip() == "":
        st.warning("投稿内容を入力してください。")
    else:
        posts = load_posts()

        # 古いデータ補完
        for i, post in enumerate(posts):
            if "id" not in post:
                post["id"] = i + 1
            if "reactions" not in post:
                post["reactions"] = {"共感": 0, "応援": 0, "わかる": 0}
            if "comments" not in post:
                post["comments"] = []

        new_post = {
            "id": get_next_id(posts),
            "tags": selected_tags,
            "content": post_content,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reactions": {"共感": 0, "応援": 0, "わかる": 0},
            "comments": []
        }

        posts.insert(0, new_post)
        save_posts(posts)
        st.success("投稿が完了しました！")
        st.rerun()

# ----------------------------
# 投稿一覧
# ----------------------------
st.markdown("---")
st.subheader("みんなの投稿")

posts = load_posts()

if not posts:
    st.write("まだ投稿はありません。")
else:
    for post in posts:
        st.write(f"**投稿日:** {post['created_at']}")

        if post["tags"]:
            st.write("**タグ:** " + " / ".join(post["tags"]))

        st.write(post["content"])

        # リアクション
        st.write("**リアクション**")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button(f"共感 ❤️ {post['reactions']['共感']}", key=f"empathy_{post['id']}"):
                posts = load_posts()
                for p in posts:
                    if p["id"] == post["id"]:
                        if "reactions" not in p:
                            p["reactions"] = {"共感": 0, "応援": 0, "わかる": 0}
                        p["reactions"]["共感"] += 1
                        break
                save_posts(posts)
                st.rerun()
        with col2:
            if st.button(f"応援 📣 {post['reactions']['応援']}", key=f"cheer_{post['id']}"):
                posts = load_posts()
                for p in posts:
                    if p["id"] == post["id"]:
                        if "reactions" not in p:
                            p["reactions"] = {"共感": 0, "応援": 0, "わかる": 0}
                        p["reactions"]["応援"] += 1
                        break
                save_posts(posts)
                st.rerun()

        with col3:
            if st.button(f"わかる 🫶 {post['reactions']['わかる']}", key=f"understand_{post['id']}"):
                posts = load_posts()
                for p in posts:
                    if p["id"] == post["id"]:
                        if "reactions" not in p:
                            p["reactions"] = {"共感": 0, "応援": 0, "わかる": 0}
                        p["reactions"]["わかる"] += 1
                        break
                save_posts(posts)
                st.rerun()

        # コメント表示
        st.write("**コメント**")
        if post["comments"]:
            for comment in post["comments"]:
                st.write(f"- {comment['text']} ({comment['created_at']})")
        else:
            st.write("まだコメントはありません。")

        # コメント入力
        comment_text = st.text_input(
            "コメントを書く",
            key=f"comment_input_{post['id']}"
        )

        if st.button("コメント送信", key=f"comment_button_{post['id']}"):
            if comment_text.strip() == "":
                st.warning("コメントを入力してください。")
            else:
                posts = load_posts()
                for p in posts:
                    if p["id"] == post["id"]:
                        if "comments" not in p:
                            p["comments"] = []
                        p["comments"].append({
                            "text": comment_text,
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        break
                save_posts(posts)
                st.success("コメントを追加しました。")
                st.rerun()

        st.markdown("---")