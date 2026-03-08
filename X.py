import streamlit as st

st.set_page_config(page_title="AvoidLove Login", layout="centered")

# ----------------------------
# 疑似ログイン状態
# ----------------------------
if "mode" not in st.session_state:
    st.session_state.mode = "login"   # "login" or "signup"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ----------------------------
# CSS
# ----------------------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f7e6ee 0%, #f1ddeb 100%);
}

.main > div {
    max-width: 560px;
    margin: 0 auto;
    padding-top: 40px;
}

.login-card {
    background: #fffafd;
    border-radius: 32px;
    padding: 42px 36px 30px 36px;
    box-shadow: 0 12px 40px rgba(180, 70, 130, 0.12);
    border: 1px solid rgba(220, 170, 200, 0.35);
}

.logo-wrap {
    text-align: center;
    margin-bottom: 24px;
}

.logo-icon {
    font-size: 44px;
    margin-bottom: 6px;
}

.logo-title {
    font-size: 44px;
    font-weight: 800;
    color: #b11f7b;
    line-height: 1.1;
    margin: 0;
}

.logo-sub {
    color: #9c939b;
    font-size: 16px;
    margin-top: 10px;
    margin-bottom: 0;
}

.tab-wrap {
    display: flex;
    gap: 0;
    background: #f1ecf7;
    border-radius: 18px;
    padding: 6px;
    margin: 30px 0 28px 0;
}

.tab-active {
    flex: 1;
    background: linear-gradient(90deg, #eb1e79, #9127d6);
    color: white;
    text-align: center;
    padding: 14px 0;
    border-radius: 14px;
    font-weight: 700;
    box-shadow: 0 6px 16px rgba(190, 40, 120, 0.25);
}

.tab-inactive {
    flex: 1;
    color: #9b96a3;
    text-align: center;
    padding: 14px 0;
    font-weight: 700;
}

.form-label {
    font-size: 15px;
    font-weight: 700;
    color: #6f6670;
    margin-top: 8px;
    margin-bottom: 8px;
}

.forgot-text {
    text-align: right;
    color: #e54886;
    font-size: 14px;
    margin-top: 8px;
    margin-bottom: 18px;
    font-weight: 600;
}

.welcome-box {
    background: white;
    border-radius: 24px;
    padding: 28px;
    box-shadow: 0 12px 40px rgba(180, 70, 130, 0.10);
    border: 1px solid rgba(220, 170, 200, 0.35);
    text-align: center;
}

.small-note {
    color: #8a808a;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# ログイン後画面
# ----------------------------
if st.session_state.logged_in:
    st.markdown("""
    <div class="welcome-box">
        <div style="font-size:42px;">🌸</div>
        <h1 style="color:#b11f7b; margin-bottom:8px;">AvoidLove</h1>
        <p class="small-note">ログインに成功しました</p>
    </div>
    """, unsafe_allow_html=True)

    st.success(f"ようこそ、{st.session_state.user_email} さん")
    if st.button("ログアウト"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.rerun()

else:
    st.markdown('<div class="login-card">', unsafe_allow_html=True)

    # ロゴ
    st.markdown("""
    <div class="logo-wrap">
        <div class="logo-icon">🌸</div>
        <h1 class="logo-title">AvoidLove</h1>
        <p class="logo-sub">気持ちを、ここで話せる</p>
    </div>
    """, unsafe_allow_html=True)

    # タブ見た目
    if st.session_state.mode == "login":
        st.markdown("""
        <div class="tab-wrap">
            <div class="tab-active">ログイン</div>
            <div class="tab-inactive">新規登録</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="tab-wrap">
            <div class="tab-inactive">ログイン</div>
            <div class="tab-active">新規登録</div>
        </div>
        """, unsafe_allow_html=True)

    # タブ切り替えボタン
    col1, col2 = st.columns(2)
    with col1:
        if st.button("ログイン画面にする", use_container_width=True):
            st.session_state.mode = "login"
            st.rerun()
    with col2:
        if st.button("新規登録画面にする", use_container_width=True):
            st.session_state.mode = "signup"
            st.rerun()

    st.write("")

    # ----------------------------
    # ログインフォーム
    # ----------------------------
    if st.session_state.mode == "login":
        st.markdown('<div class="form-label">メールアドレス</div>', unsafe_allow_html=True)
        email = st.text_input(
            label="メールアドレス",
            placeholder="example@mail.com",
            label_visibility="collapsed"
        )

        st.markdown('<div class="form-label">パスワード</div>', unsafe_allow_html=True)
        password = st.text_input(
            label="パスワード",
            placeholder="••••••••",
            type="password",
            label_visibility="collapsed"
        )

        st.markdown('<div class="forgot-text">パスワードを忘れた方</div>', unsafe_allow_html=True)

        if st.button("ログイン", use_container_width=True):
            if not email or not password:
                st.warning("メールアドレスとパスワードを入力してください。")
            else:
                # 仮の認証
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.rerun()

    # ----------------------------
    # 新規登録フォーム
    # ----------------------------
    else:
        st.markdown('<div class="form-label">メールアドレス</div>', unsafe_allow_html=True)
        new_email = st.text_input(
            label="新規メールアドレス",
            placeholder="example@mail.com",
            label_visibility="collapsed"
        )

        st.markdown('<div class="form-label">パスワード</div>', unsafe_allow_html=True)
        new_password = st.text_input(
            label="新規パスワード",
            placeholder="8文字以上で入力",
            type="password",
            label_visibility="collapsed"
        )

        st.markdown('<div class="form-label">パスワード確認</div>', unsafe_allow_html=True)
        confirm_password = st.text_input(
            label="パスワード確認",
            placeholder="もう一度入力",
            type="password",
            label_visibility="collapsed"
        )

        if st.button("新規登録", use_container_width=True):
            if not new_email or not new_password or not confirm_password:
                st.warning("すべて入力してください。")
            elif new_password != confirm_password:
                st.error("パスワードが一致しません。")
            elif len(new_password) < 8:
                st.warning("パスワードは8文字以上にしてください。")
            else:
                st.success("新規登録が完了した想定です。")
                st.session_state.mode = "login"
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)