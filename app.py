import streamlit as st
import pandas as pd
from datetime import datetime

from main import BankSystem, Account, Audit
from database import connect_to_database


# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="NexaBank | Banking Management",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# MODERN UI
# ============================================================
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background: #f7f8fc;
        }

        [data-testid="stSidebar"] {
            background: #111827;
            border-right: 1px solid #202938;
        }

        [data-testid="stSidebar"] * {
            color: #f9fafb;
        }

        .brand {
            font-size: 25px;
            font-weight: 800;
            letter-spacing: -0.8px;
            margin-bottom: 3px;
        }

        .brand-sub {
            color: #9ca3af;
            font-size: 12px;
            margin-bottom: 28px;
        }

        .hero {
            background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
            border-radius: 22px;
            padding: 30px 32px;
            color: white;
            margin-bottom: 22px;
            box-shadow: 0 12px 35px rgba(17, 24, 39, 0.12);
        }

        .hero h1 {
            font-size: 31px;
            margin: 0 0 8px 0;
            font-weight: 800;
            letter-spacing: -1px;
        }

        .hero p {
            color: #d1d5db;
            margin: 0;
            font-size: 14px;
        }

        .metric-card {
            background: white;
            border: 1px solid #e7eaf0;
            border-radius: 18px;
            padding: 21px;
            min-height: 120px;
            box-shadow: 0 5px 18px rgba(15, 23, 42, 0.04);
        }

        .metric-label {
            color: #6b7280;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .metric-value {
            color: #111827;
            font-size: 25px;
            font-weight: 800;
        }

        .metric-small {
            color: #9ca3af;
            font-size: 12px;
            margin-top: 5px;
        }

        .section-title {
            font-size: 20px;
            font-weight: 800;
            color: #111827;
            margin: 22px 0 12px 0;
        }

        .account-card {
            background: white;
            border: 1px solid #e7eaf0;
            border-radius: 18px;
            padding: 20px;
            margin-bottom: 16px;
        }

        .account-number {
            color: #6b7280;
            font-size: 12px;
            margin-bottom: 4px;
        }

        .account-name {
            color: #111827;
            font-size: 22px;
            font-weight: 800;
        }

        .info-pill {
            display: inline-block;
            background: #f3f4f6;
            color: #374151;
            padding: 7px 11px;
            border-radius: 9px;
            font-size: 12px;
            margin-right: 6px;
        }

        .login-box {
            background: white;
            border: 1px solid #e7eaf0;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 30px rgba(15, 23, 42, 0.06);
        }

        /* Authentication tabs: strong contrast so both options are obvious */
        div[data-testid="stTabs"] {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            padding: 8px 14px 18px 14px;
            box-shadow: 0 8px 28px rgba(15, 23, 42, 0.07);
        }

        div[data-testid="stTabs"] button {
            color: #6b7280 !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            padding: 12px 18px !important;
            border-radius: 10px 10px 0 0 !important;
        }

        div[data-testid="stTabs"] button[aria-selected="true"] {
            color: #111827 !important;
            background: #f3f4f6 !important;
        }

        div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
            background-color: #111827 !important;
            height: 3px !important;
        }

        div[data-testid="stTabs"] [data-baseweb="tab-border"] {
            background-color: #e5e7eb !important;
        }

        div.stButton > button {
            border-radius: 10px;
            font-weight: 600;
            min-height: 42px;
            border: 1px solid #e5e7eb;
        }

        div.stButton > button[kind="primary"] {
            background: #111827;
            color: white;
            border: none;
        }

        div.stButton > button[kind="primary"]:hover {
            background: #1f2937;
            color: white;
        }

        .success-box {
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            color: #065f46;
            padding: 14px 16px;
            border-radius: 12px;
            margin: 10px 0;
        }

        .warning-box {
            background: #fffbeb;
            border: 1px solid #fde68a;
            color: #92400e;
            padding: 14px 16px;
            border-radius: 12px;
            margin: 10px 0;
        }

        .footer {
            color: #9ca3af;
            font-size: 12px;
            text-align: center;
            padding: 28px 0 10px;
        }


        /* ==================================================
           HIGH-CONTRAST FIXES (readable in light AND dark OS/browser theme)
           ================================================== */

        /* Main-area text: always dark on the light background */
        .stApp, .stApp p, .stApp label, .stApp span, .stApp li,
        .stApp h1, .stApp h2, .stApp h3, .stApp h4,
        [data-testid="stMarkdownContainer"],
        [data-testid="stWidgetLabel"] p,
        [data-testid="stCaptionContainer"] {
            color: #111827;
        }

        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p {
            color: #4b5563 !important;
        }

        /* Hero keeps white text on dark card */
        .hero h1 { color: #ffffff !important; }
        .hero p  { color: #e5e7eb !important; }

        /* Cards */
        .metric-label { color: #4b5563 !important; }
        .metric-value { color: #111827 !important; }
        .metric-small { color: #6b7280 !important; }

        /* ---------- TABS (Sign in / Create account) ---------- */
        div[data-testid="stTabs"] button,
        div[data-testid="stTabs"] button p {
            color: #374151 !important;
            font-weight: 700 !important;
        }
        div[data-testid="stTabs"] button[role="tab"] {
            background: #eef0f4 !important;
            border: 1px solid #d1d5db !important;
            margin-right: 6px !important;
        }
        div[data-testid="stTabs"] button[aria-selected="true"],
        div[data-testid="stTabs"] button[aria-selected="true"] p {
            color: #ffffff !important;
        }
        div[data-testid="stTabs"] button[aria-selected="true"] {
            background: #111827 !important;
            border-color: #111827 !important;
        }

        /* ---------- INPUTS ---------- */
        div[data-baseweb="input"],
        div[data-baseweb="base-input"],
        div[data-testid="stNumberInput"] div[data-baseweb="input"] {
            background: #ffffff !important;
            border: 1px solid #9ca3af !important;
            border-radius: 10px !important;
        }
        div[data-baseweb="input"] input,
        div[data-baseweb="base-input"] input,
        input[type="password"], input[type="text"], input[type="number"] {
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
            background: #ffffff !important;
        }
        input::placeholder {
            color: #6b7280 !important;
            -webkit-text-fill-color: #6b7280 !important;
            opacity: 1 !important;
        }
        div[data-baseweb="input"]:focus-within {
            border-color: #111827 !important;
            box-shadow: 0 0 0 2px rgba(17, 24, 39, 0.20) !important;
        }
        /* password show/hide eye + number +/- buttons */
        div[data-baseweb="input"] button,
        div[data-testid="stNumberInput"] button {
            background: #f3f4f6 !important;
            color: #111827 !important;
        }
        div[data-baseweb="input"] svg { fill: #374151 !important; }

        /* Form container */
        [data-testid="stForm"] {
            background: #ffffff !important;
            border: 1px solid #d1d5db !important;
            border-radius: 14px !important;
        }

        /* Checkbox text */
        [data-testid="stCheckbox"] p { color: #111827 !important; }

        /* ---------- BUTTONS (main area) ---------- */
        .stApp div.stButton > button,
        .stApp div[data-testid="stFormSubmitButton"] > button {
            background: #ffffff;
            color: #111827 !important;
            border: 1px solid #9ca3af;
        }
        .stApp div.stButton > button[kind="primary"],
        .stApp div[data-testid="stFormSubmitButton"] > button[kind="primary"],
        .stApp button[data-testid="stBaseButton-primary"],
        .stApp button[data-testid="stBaseButton-primaryFormSubmit"] {
            background: #111827 !important;
            border: 1px solid #111827 !important;
        }
        .stApp div.stButton > button[kind="primary"] p,
        .stApp div[data-testid="stFormSubmitButton"] > button[kind="primary"] p,
        .stApp button[data-testid="stBaseButton-primary"] p,
        .stApp button[data-testid="stBaseButton-primaryFormSubmit"] p {
            color: #ffffff !important;
        }

        /* ---------- SIDEBAR ---------- */
        [data-testid="stSidebar"] .brand { color: #ffffff !important; }
        [data-testid="stSidebar"] .brand-sub { color: #cbd5e1 !important; }
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
            color: #f1f5f9 !important;
        }
        /* Sidebar buttons: visible text on dark background */
        [data-testid="stSidebar"] div.stButton > button {
            background: #1f2937 !important;
            color: #ffffff !important;
            border: 1px solid #4b5563 !important;
            text-align: left;
        }
        [data-testid="stSidebar"] div.stButton > button p {
            color: #ffffff !important;
        }
        [data-testid="stSidebar"] div.stButton > button:hover {
            background: #374151 !important;
            border-color: #9ca3af !important;
        }
        /* Active menu item = bright blue so it stands out */
        [data-testid="stSidebar"] button[data-testid="stBaseButton-primary"],
        [data-testid="stSidebar"] div.stButton > button[kind="primary"] {
            background: #2563eb !important;
            border: 1px solid #60a5fa !important;
            color: #ffffff !important;
        }
        [data-testid="stSidebar"] hr { border-color: #4b5563 !important; }

        /* ---------- ALERTS (info / success / warning / error) ---------- */
        [data-testid="stAlert"] p,
        [data-testid="stAlert"] span,
        [data-testid="stAlert"] code {
            color: #111827 !important;
        }
        [data-testid="stAlert"] {
            border: 1px solid #9ca3af;
            border-radius: 12px;
        }
        div[data-testid="stAlertContentInfo"]    { color: #111827 !important; }
        div[data-testid="stAlertContentSuccess"] { color: #111827 !important; }
        div[data-testid="stAlertContentWarning"] { color: #111827 !important; }
        div[data-testid="stAlertContentError"]   { color: #111827 !important; }
        [data-testid="stAlert"] code {
            background: #ffffff !important;
            padding: 2px 6px;
            border-radius: 6px;
            font-weight: 700;
        }

        /* Tables */
        [data-testid="stDataFrame"] { border: 1px solid #d1d5db; border-radius: 12px; }

        .info-pill { color: #1f2937 !important; background: #e5e7eb !important; }
        .footer { color: #6b7280 !important; }

        /* Remove excessive Streamlit top spacing */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================
if "bank" not in st.session_state:
    try:
        st.session_state.bank = BankSystem()
    except Exception as e:
        st.session_state.bank = None
        st.session_state.startup_error = str(e)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "account" not in st.session_state:
    st.session_state.account = None

if "pin" not in st.session_state:
    st.session_state.pin = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ============================================================
# HELPERS
# ============================================================
def get_current_account():
    return st.session_state.get("account")


def logout():
    st.session_state.logged_in = False
    st.session_state.account = None
    st.session_state.pin = None
    st.session_state.page = "Dashboard"


def refresh_account():
    """Reload the current account from PostgreSQL."""
    account = get_current_account()
    pin = st.session_state.get("pin")

    if not account or not pin:
        return False

    fresh_account = Account.load_from_db(account.get_account_number(), pin)

    if fresh_account:
        st.session_state.account = fresh_account
        return True

    return False


def get_balance_safely():
    """Read balance without relying on the existing balance method's None edge case."""
    account = get_current_account()
    pin = st.session_state.get("pin")

    if not account or not pin:
        return None

    fresh_account = Account.load_from_db(account.get_account_number(), pin)

    if fresh_account:
        st.session_state.account = fresh_account
        return fresh_account.get_balance()

    return None


def get_transaction_logs(account_number):
    logs = Audit.get_single_audit_logs(account_number)
    return logs if logs else []


def money(value):
    return f"₹{float(value):,.2f}"


def valid_pin(pin):
    return pin.isdigit() and len(pin) == 4


def database_status():
    connection = connect_to_database()

    if connection:
        connection.close()
        return True

    return False


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown('<div class="brand">NexaBank</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="brand-sub">Banking Management System</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.logged_in:
        account = get_current_account()

        st.markdown("### Account")
        st.markdown(
            f"""
            <div style="
                background:#1f2937;
                border:1px solid #374151;
                border-radius:14px;
                padding:14px;
                margin-bottom:18px;
            ">
                <div style="font-size:15px;font-weight:700;color:#ffffff;">{account.get_name()}</div>
                <div style="font-size:12px;color:#cbd5e1;margin-top:4px;">
                    {account.get_account_number()}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        menu = {
            "Dashboard": "🏠",
            "Deposit": "＋",
            "Withdraw": "−",
            "Transactions": "↗",
            "Account Settings": "⚙",
        }

        for item, icon in menu.items():
            if st.button(
                f"{icon}  {item}",
                key=f"nav_{item}",
                use_container_width=True,
                type="primary" if st.session_state.page == item else "secondary",
            ):
                st.session_state.page = item
                st.rerun()

        st.markdown("---")

        if st.button("Log out", use_container_width=True):
            logout()
            st.rerun()

    else:
        st.markdown(
            """
            <div style="color:#e2e8f0;font-size:13px;line-height:1.6;">
                Securely manage accounts, balances, deposits, withdrawals
                and transaction history.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.caption("PostgreSQL • Python • Streamlit")


# ============================================================
# STARTUP / DATABASE ERROR
# ============================================================
if st.session_state.bank is None:
    st.error(
        "The banking system could not initialize. "
        "Please make sure PostgreSQL is running and the database credentials "
        "in `database.py` are correct."
    )

    if "startup_error" in st.session_state:
        with st.expander("Technical details"):
            st.code(st.session_state.startup_error)

    st.stop()


# ============================================================
# LOGGED-OUT HOME PAGE
# ============================================================
if not st.session_state.logged_in:

    st.markdown(
        """
        <div class="hero">
            <h1>Simple banking. Clear control.</h1>
            <p>
                A modern interface for your Python + PostgreSQL Banking
                System Management application.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1.15, 0.85], gap="large")

    with col1:
        st.markdown("### Welcome to NexaBank")
        st.write(
            "Manage your bank account from one clean dashboard. "
            "Create an account, securely log in, manage your balance, "
            "and review your transaction history."
        )

        st.markdown("")
        a, b, c = st.columns(3)

        with a:
            st.markdown(
                '<div class="metric-card"><div class="metric-label">Storage</div>'
                '<div class="metric-value">SQL</div>'
                '<div class="metric-small">PostgreSQL database</div></div>',
                unsafe_allow_html=True,
            )

        with b:
            st.markdown(
                '<div class="metric-card"><div class="metric-label">Security</div>'
                '<div class="metric-value">SHA-256</div>'
                '<div class="metric-small">PIN hashing</div></div>',
                unsafe_allow_html=True,
            )

        with c:
            st.markdown(
                '<div class="metric-card"><div class="metric-label">Activity</div>'
                '<div class="metric-value">Audit</div>'
                '<div class="metric-small">Transaction logs</div></div>',
                unsafe_allow_html=True,
            )

    with col2:
        tab_login, tab_create = st.tabs(["Sign in", "Create account"])

        # ----------------------------------------------------
        # LOGIN
        # ----------------------------------------------------
        with tab_login:
            st.markdown("### Sign in")
            st.caption("Access your existing bank account.")

            with st.form("login_form"):
                account_number = st.text_input(
                    "Account number",
                    placeholder="Enter your account number",
                )

                pin = st.text_input(
                    "4-digit PIN",
                    type="password",
                    max_chars=4,
                    placeholder="••••",
                )

                submitted = st.form_submit_button(
                    "Sign in",
                    use_container_width=True,
                    type="primary",
                )

            if submitted:
                account_number = account_number.strip()
                pin = pin.strip()

                if not account_number:
                    st.error("Please enter your account number.")
                elif not valid_pin(pin):
                    st.error("PIN must be exactly 4 digits.")
                else:
                    with st.spinner("Signing in..."):
                        account = st.session_state.bank.read_account(
                            account_number, pin
                        )

                    if account:
                        st.session_state.account = account
                        st.session_state.pin = pin
                        st.session_state.logged_in = True
                        st.session_state.page = "Dashboard"
                        st.success("Login successful.")
                        st.rerun()
                    else:
                        st.error("Invalid account number or PIN.")

        # ----------------------------------------------------
        # CREATE ACCOUNT
        # ----------------------------------------------------
        with tab_create:
            st.markdown("### Create account")
            st.caption("Open a new bank account in a few seconds.")

            with st.form("create_account_form"):
                name = st.text_input(
                    "Full name",
                    placeholder="Enter your name",
                )

                new_pin = st.text_input(
                    "Create 4-digit PIN",
                    type="password",
                    max_chars=4,
                    placeholder="••••",
                )

                confirm_pin = st.text_input(
                    "Confirm PIN",
                    type="password",
                    max_chars=4,
                    placeholder="••••",
                )

                submitted = st.form_submit_button(
                    "Create account",
                    use_container_width=True,
                    type="primary",
                )

            if submitted:
                name = name.strip()
                new_pin = new_pin.strip()
                confirm_pin = confirm_pin.strip()

                if not name:
                    st.error("Name cannot be empty.")
                elif not valid_pin(new_pin):
                    st.error("PIN must be exactly 4 digits.")
                elif new_pin != confirm_pin:
                    st.error("PINs do not match.")
                else:
                    with st.spinner("Creating your account..."):
                        account = st.session_state.bank.create_account(
                            name, new_pin
                        )

                    if account:
                        st.success("Account created successfully.")
                        st.info(
                            f"Your account number is: "
                            f"`{account.get_account_number()}`"
                        )
                        st.warning(
                            "Save your account number and PIN securely."
                        )
                    else:
                        st.error("Account could not be created. Please try again.")

    st.markdown(
        '<div class="footer">NexaBank • Python + PostgreSQL Banking System</div>',
        unsafe_allow_html=True,
    )

    st.stop()


# ============================================================
# AUTHENTICATED APP
# ============================================================
account = get_current_account()
if not account:
    logout()
    st.rerun()

# ============================================================
# DASHBOARD
# ============================================================
if st.session_state.page == "Dashboard":

    balance = get_balance_safely()
    logs = get_transaction_logs(account.get_account_number())

    st.markdown(
        f"""
        <div class="hero">
            <h1>Good to see you, {account.get_name().split()[0]}.</h1>
            <p>Your account is ready. Manage your money from one place.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Available balance</div>
                <div class="metric-value">{money(balance or 0)}</div>
                <div class="metric-small">Current account balance</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Account number</div>
                <div class="metric-value" style="font-size:19px;">
                    {account.get_account_number()}
                </div>
                <div class="metric-small">Your unique account ID</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Transactions</div>
                <div class="metric-value">{len(logs)}</div>
                <div class="metric-small">Recorded account activities</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">Quick actions</div>', unsafe_allow_html=True)

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        if st.button("＋ Deposit", use_container_width=True, type="primary"):
            st.session_state.page = "Deposit"
            st.rerun()

    with q2:
        if st.button("− Withdraw", use_container_width=True):
            st.session_state.page = "Withdraw"
            st.rerun()

    with q3:
        if st.button("↗ Transactions", use_container_width=True):
            st.session_state.page = "Transactions"
            st.rerun()

    with q4:
        if st.button("⚙ Settings", use_container_width=True):
            st.session_state.page = "Account Settings"
            st.rerun()

    st.markdown('<div class="section-title">Recent activity</div>', unsafe_allow_html=True)

    if logs:
        recent = logs[:5]

        rows = []
        for log in recent:
            rows.append(
                {
                    "Date & time": log["timestamp"],
                    "Action": log["action"],
                    "Amount": money(log["amount"]),
                }
            )

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No transaction activity yet.")


# ============================================================
# DEPOSIT
# ============================================================
elif st.session_state.page == "Deposit":

    st.markdown("## Deposit money")
    st.caption("Add money to your account.")

    col1, col2 = st.columns([0.9, 1.1], gap="large")

    with col1:
        with st.form("deposit_form"):
            amount = st.number_input(
                "Deposit amount",
                min_value=1.0,
                step=100.0,
                value=1000.0,
                format="%.2f",
            )

            submitted = st.form_submit_button(
                "Deposit money",
                use_container_width=True,
                type="primary",
            )

        if submitted:
            with st.spinner("Processing deposit..."):
                success = st.session_state.bank.deposit(
                    account.get_account_number(),
                    st.session_state.pin,
                    amount,
                )

            if success:
                refresh_account()
                st.success(f"{money(amount)} deposited successfully.")
                st.rerun()
            else:
                st.error("Deposit failed. Please check the amount and try again.")

    with col2:
        balance = get_balance_safely()
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Current balance</div>
                <div class="metric-value">{money(balance or 0)}</div>
                <div class="metric-small">
                    Account ending in {account.get_account_number()[-4:]}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# WITHDRAW
# ============================================================
elif st.session_state.page == "Withdraw":

    st.markdown("## Withdraw money")
    st.caption("Withdraw money from your account.")

    balance = get_balance_safely()

    col1, col2 = st.columns([0.9, 1.1], gap="large")

    with col1:
        with st.form("withdraw_form"):
            amount = st.number_input(
                "Withdrawal amount",
                min_value=1.0,
                max_value=float(balance or 1),
                step=100.0,
                value=min(1000.0, float(balance or 1)),
                format="%.2f",
            )

            submitted = st.form_submit_button(
                "Withdraw money",
                use_container_width=True,
                type="primary",
            )

        if submitted:
            with st.spinner("Processing withdrawal..."):
                success = st.session_state.bank.withdraw(
                    account.get_account_number(),
                    st.session_state.pin,
                    amount,
                )

            if success:
                refresh_account()
                st.success(f"{money(amount)} withdrawn successfully.")
                st.rerun()
            else:
                st.error(
                    "Withdrawal failed. The amount may be invalid "
                    "or greater than your available balance."
                )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Available balance</div>
                <div class="metric-value">{money(balance or 0)}</div>
                <div class="metric-small">Do not withdraw more than this amount.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# TRANSACTIONS
# ============================================================
elif st.session_state.page == "Transactions":

    st.markdown("## Transaction history")
    st.caption("A record of activities associated with your account.")

    logs = get_transaction_logs(account.get_account_number())

    if logs:
        rows = []

        for log in logs:
            rows.append(
                {
                    "ID": log["id"],
                    "Date & time": log["timestamp"],
                    "Action": log["action"],
                    "Amount": money(log["amount"]),
                    "Account holder": log["holder_name"],
                }
            )

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "ID": st.column_config.NumberColumn(width="small"),
                "Date & time": st.column_config.DatetimeColumn(
                    format="DD MMM YYYY, HH:mm"
                ),
                "Amount": st.column_config.TextColumn(),
            },
        )
    else:
        st.info("No transaction history found.")


# ============================================================
# ACCOUNT SETTINGS
# ============================================================
elif st.session_state.page == "Account Settings":

    st.markdown("## Account settings")
    st.caption("Update your account information or close your account.")

    tab_profile, tab_pin, tab_close = st.tabs(
        ["Profile", "Change PIN", "Close account"]
    )

    # --------------------------------------------------------
    # PROFILE
    # --------------------------------------------------------
    with tab_profile:
        st.markdown("### Personal information")

        with st.form("update_profile_form"):
            new_name = st.text_input(
                "Account holder name",
                value=account.get_name(),
            )

            submitted = st.form_submit_button(
                "Save changes",
                use_container_width=True,
                type="primary",
            )

        if submitted:
            new_name = new_name.strip()

            if not new_name:
                st.error("Name cannot be empty.")
            else:
                account.set_name(new_name)

                if st.session_state.bank.update_account(account):
                    Audit.log_action(
                        account.get_account_number(),
                        account.get_name(),
                        "Account Name Updated",
                        0.00,
                    )
                    refresh_account()
                    st.success("Account information updated successfully.")
                    st.rerun()
                else:
                    st.error("Unable to update account information.")

    # --------------------------------------------------------
    # CHANGE PIN
    # --------------------------------------------------------
    with tab_pin:
        st.markdown("### Change account PIN")
        st.warning(
            "Changing your PIN will require you to sign in again."
        )

        with st.form("change_pin_form"):
            old_pin = st.text_input(
                "Current PIN",
                type="password",
                max_chars=4,
            )

            new_pin = st.text_input(
                "New 4-digit PIN",
                type="password",
                max_chars=4,
            )

            confirm_new_pin = st.text_input(
                "Confirm new PIN",
                type="password",
                max_chars=4,
            )

            submitted = st.form_submit_button(
                "Change PIN",
                use_container_width=True,
                type="primary",
            )

        if submitted:
            if old_pin != st.session_state.pin:
                st.error("Current PIN is incorrect.")
            elif not valid_pin(new_pin):
                st.error("New PIN must be exactly 4 digits.")
            elif new_pin != confirm_new_pin:
                st.error("New PINs do not match.")
            else:
                account.set_pinhash(new_pin)

                if st.session_state.bank.update_account(account):
                    Audit.log_action(
                        account.get_account_number(),
                        account.get_name(),
                        "PIN Changed Auto Logout",
                        0.00,
                    )

                    logout()
                    st.success(
                        "PIN changed successfully. "
                        "Please sign in again using your new PIN."
                    )
                    st.rerun()
                else:
                    st.error("Unable to change PIN.")

    # --------------------------------------------------------
    # CLOSE ACCOUNT
    # --------------------------------------------------------
    with tab_close:
        st.markdown("### Close account")
        st.warning(
            "Closing your account permanently deletes the account and "
            "its audit history from the database."
        )

        confirm = st.checkbox(
            "I understand that this action cannot be undone."
        )

        if st.button(
            "Close account permanently",
            use_container_width=True,
            type="primary",
        ):
            if not confirm:
                st.error("Please confirm the action first.")
            else:
                with st.spinner("Closing account..."):
                    success = st.session_state.bank.delete_account(
                        account.get_account_number(),
                        st.session_state.pin,
                    )

                if success:
                    logout()
                    st.success("Your account has been closed successfully.")
                    st.rerun()
                else:
                    st.error("Unable to close the account. Please try again.")


# ============================================================
# FOOTER
# ============================================================
st.markdown(
    '<div class="footer">NexaBank • Banking System Management • PostgreSQL</div>',
    unsafe_allow_html=True,
)
