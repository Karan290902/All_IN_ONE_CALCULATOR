import streamlit as st


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Insurance Premium Calculator",
    page_icon="💰",
    layout="centered"
)


# ---------------------------------------------------------
# INSURER RATES
# ---------------------------------------------------------

INSURER_RATES = {
    "Care": 8.5,
    "Cigna Manipal": 25.0,
    "Aditya Birla": 25.0,
    "Magma": 10.0,
    "IPRU": 25.0,
    "Aviva": 10.0,
    "Digit": 32.5
}

GST_RATE = 18.0


# ---------------------------------------------------------
# HELPER FUNCTION - INDIAN CURRENCY FORMAT
# ---------------------------------------------------------

def format_currency(amount):
    """
    Format number using Indian numbering system.
    Example:
    1000000 -> ₹10,00,000
    """

    amount = round(amount, 2)

    if amount == int(amount):
        amount = int(amount)

    number = str(amount)

    if "." in number:
        integer_part, decimal_part = number.split(".")
    else:
        integer_part = number
        decimal_part = ""

    # Handle negative values
    negative = integer_part.startswith("-")

    if negative:
        integer_part = integer_part[1:]

    if len(integer_part) <= 3:
        formatted = integer_part
    else:
        last_three = integer_part[-3:]
        remaining = integer_part[:-3]

        groups = []

        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]

        if remaining:
            groups.insert(0, remaining)

        formatted = ",".join(groups) + "," + last_three

    if negative:
        formatted = "-" + formatted

    if decimal_part:
        formatted += "." + decimal_part

    return f"₹{formatted}"


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("💰 Insurance Premium Calculator")

st.caption("Calculate premium before GST, GST amount and premium including GST.")

st.divider()


# ---------------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------------

st.subheader("Quotation Details")

insurer = st.selectbox(
    "Insurer Name",
    list(INSURER_RATES.keys())
)

sum_assured = st.number_input(
    "Sum Assured (₹)",
    min_value=0.0,
    value=500000.0,
    step=50000.0
)

premium_rate = st.number_input(
    "Premium Rate (%)",
    min_value=0.0,
    value=float(INSURER_RATES[insurer]),
    step=0.5
)

loading = st.number_input(
    "Loading (%)",
    min_value=0.0,
    value=0.0,
    step=0.5
)


# ---------------------------------------------------------
# CALCULATE BUTTON
# ---------------------------------------------------------

calculate = st.button(
    "Calculate Premium",
    type="primary",
    use_container_width=True
)


# ---------------------------------------------------------
# CALCULATION
# ---------------------------------------------------------

if calculate:

    if sum_assured <= 0:
        st.error("Please enter a Sum Assured greater than ₹0.")

    elif premium_rate < 0:
        st.error("Premium Rate cannot be negative.")

    elif loading < 0:
        st.error("Loading cannot be negative.")

    else:

        # Base premium
        base_premium = (
            sum_assured * premium_rate / 100
        )

        # Loading amount
        loading_amount = (
            base_premium * loading / 100
        )

        # Premium before GST
        premium_before_gst = (
            base_premium + loading_amount
        )

        # GST
        gst_amount = (
            premium_before_gst * GST_RATE / 100
        )

        # Premium including GST
        premium_with_gst = (
            premium_before_gst + gst_amount
        )


        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        st.divider()

        st.subheader("Premium Quotation")

        st.write(f"**Insurer:** {insurer}")
        st.write(f"**Sum Assured:** {format_currency(sum_assured)}")
        st.write(f"**Premium Rate:** {premium_rate:.2f}%")
        st.write(f"**Loading:** {loading:.2f}%")

        st.divider()

        # Breakdown
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Base Premium",
                format_currency(base_premium)
            )

        with col2:
            st.metric(
                "Loading Amount",
                format_currency(loading_amount)
            )

        st.divider()

        # Main quotation
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Premium Before GST",
                format_currency(premium_before_gst)
            )

        with col2:
            st.metric(
                "GST @ 18%",
                format_currency(gst_amount)
            )

        with col3:
            st.metric(
                "Premium Including GST",
                format_currency(premium_with_gst)
            )