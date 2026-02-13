import streamlit as st
from components import Chart

st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
        div[data-testid="stMetric"] {
            border-left: 0.5rem solid #13957b !important;
            box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;
            padding: 0 0 0 2% !important;
            border-radius: 12px !important;
            background-color: transparent !important;
        }
        div[data-testid="stMetric"] label{
            margin-bottom: 5px;
         }

         #e-commerce-sales-dashboard{
         margin-bottom:12px;
         }

        /* Reduce top padding */
        .block-container {
            padding-top: 2rem;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
            font-weight: 500;
        }
        
        /* Primary color customization */
        :root {
            --primary-color: #13957b;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 E-Commerce Sales Dashboard")

c = Chart('data/ecommerce_sales_data.csv')
with st.sidebar:
    st.header("🔍 Filters")

    st.subheader("Date Range")
    min_date = c.df['order_date'].min()
    max_date = c.df['order_date'].max()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key='date_range'
    )

    st.subheader("Region")
    regions = st.multiselect(
        "Select Regions",
        options=c.unique_values('customer_region'),
        default=c.unique_values('customer_region'),
        key='region_filter'
    )

    st.subheader("Category")
    categories = st.multiselect(
        "Select Categories",
        options=c.unique_values('category_name'),
        default=c.unique_values('category_name'),
        key='category_filter'
    )

    st.subheader("Customer Segment")
    segments = st.multiselect(
        "Select Segments",
        options=c.unique_values('customer_segment'),
        default=c.unique_values('customer_segment'),
        key='segment_filter'
    )

    st.subheader("Delivery Status")
    delivery_status = st.multiselect(
        "Select Status",
        options=c.unique_values('delivery_status'),
        default=c.unique_values('delivery_status'),
        key='status_filter'
    )

    st.subheader("Shipping Type")
    shipping_types = st.multiselect(
        "Select Shipping Types",
        options=c.unique_values('shipping_type'),
        default=c.unique_values('shipping_type'),
        key='shipping_filter'
    )

    if st.button("🔄 Reset All Filters", width='stretch'):
        st.rerun()

c.set_filters(
    date_range=date_range,
    customer_region=regions,
    category_name=categories,
    customer_segment=segments,
    delivery_status=delivery_status,
    shipping_type=shipping_types
)

total_revenue, total_profit, total_orders, profit_margin, avg_order_value, on_time_rate, late_deliveries = c.compute_kpis()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 Total Revenue",
        value=f"${total_revenue/1000000:.2f}M" if total_revenue >= 1000000 else f"${total_revenue/1000:.0f}K",
        delta="",  # You can add period comparison here
        help="Total sales across all orders"
    )

with col2:
    st.metric(
        label="📈 Total Profit",
        value=f"${total_profit/1000000:.2f}M" if total_profit >= 1000000 else f"${total_profit/1000:.0f}K",
        delta=f"{profit_margin:.1f}% margin",
        help="Net profit after costs"
    )

with col3:
    st.metric(
        label="📦 Total Orders",
        value=f"{total_orders:,}",
        delta=f"${avg_order_value:.2f} AOV",
        help="Number of orders placed"
    )

with col4:
    # Color coding for on-time rate
    if on_time_rate >= 95:
        delta_color = "normal"
    elif on_time_rate >= 90:
        delta_color = "off"
    else:
        delta_color = "inverse"

    st.metric(
        label="🚚 On-Time Delivery",
        value=f"{on_time_rate:.1f}%",
        delta=f"{late_deliveries:,} late",
        delta_color=delta_color,
        help="Orders delivered on schedule"
    )


tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Overview",
    "💼 Sales Analysis",
    "💰 Profitability",
    "🚚 Shipping",
    "👥 Customer & Geographic",
    "📦 Product Performance",
    "📅 Time Series"
])

with tab1:
    st.header("Overview Dashboard")
    st.caption("Main KPIs are displayed above the tabs and apply to all views")

    colA1, colA2 = st.columns([2, 1])

    with colA1:
        st.plotly_chart(
            c.create_revenue_trend_chart(),
            width='stretch',
        )

    with colA2:
        st.plotly_chart(
            c.create_sales_by_category_chart(),
            width='stretch',
        )

    colB1, colB2 = st.columns([1, 1])

    with colB1:
        st.plotly_chart(
            c.create_revenue_by_region_chart(),
            width='stretch',
        )

    with colB2:
        st.plotly_chart(
            c.create_top_states_treemap(),
            width='stretch',
        )


with tab2:
    st.header("Sales Analysis")

    st.plotly_chart(
        c.create_sales_trend_by_category_chart(),
        width='stretch',
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.plotly_chart(
            c.create_top_products_chart(),
            width='stretch',
        )

    with col2:
        st.plotly_chart(
            c.create_sales_by_segment_chart(),
            width='stretch',
        )

        st.plotly_chart(
            c.create_quantity_distribution_chart(),
            width='stretch',
        )

    st.plotly_chart(
        c.create_monthly_sales_heatmap(),
        width='stretch',
    )

with tab3:
    st.header("Profitability Analysis")

    # Row 1: Scatter plot
    st.plotly_chart(
        c.create_profit_vs_revenue_scatter(),
        width='stretch',
    )

    # Row 2: Box plot and discount impact
    col1, col2 = st.columns([1, 1])

    with col1:
        st.plotly_chart(
            c.create_profit_margin_by_category_chart(),
            width='stretch',
        )

    with col2:
        st.plotly_chart(
            c.create_discount_impact_chart(),
            width='stretch',
        )

    # Row 3: Waterfall and trend
    col1, col2 = st.columns([1, 1])

    with col1:
        st.plotly_chart(
            c.create_top_profitable_products_chart(),
            width='stretch',
        )

    with col2:
        st.plotly_chart(
            c.create_profit_margin_trend_chart(),
            width='stretch',
        )

with tab4:
    st.header("Shipping & Delivery Performance")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.plotly_chart(
            c.create_delivery_status_chart(),
            width='stretch',
        )

    with col2:
        st.plotly_chart(
            c.create_delivery_by_shipping_type_chart(),
            width='stretch',
        )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.plotly_chart(
            c.create_delivery_time_by_region_chart(),
            width='stretch',
        )

    with col2:
        st.plotly_chart(
            c.create_delivery_time_by_shipping_chart(),
            width='stretch',
        )

    st.plotly_chart(
        c.create_late_delivery_trend_chart(),
        width='stretch',
    )

    st.plotly_chart(
        c.create_state_delivery_map(),
        width='stretch',
    )

with tab5:
    st.header("Customer & Geographic Analysis")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.plotly_chart(
            c.create_revenue_by_segment_funnel(),
            width='stretch'
        )

    with col2:
        st.plotly_chart(
            c.create_regional_radar_chart(),
            width='stretch'
        )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.plotly_chart(
            c.create_top_cities_chart(),
            width='stretch'
        )

    with col2:
        st.plotly_chart(
            c.create_segment_category_preference_chart(),
            width='stretch'
        )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.plotly_chart(
            c.create_state_revenue_map(),
            width='stretch'
        )

    with col2:
        st.plotly_chart(
            c.create_pareto_chart(),
            width='stretch'
        )

with tab6:
    st.header("Product Performance")

    st.plotly_chart(
        c.create_product_matrix_chart(),
        width='stretch',
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.plotly_chart(
            c.create_top_quantity_products_chart(),
            width='stretch',
        )

    with col2:
        st.plotly_chart(
            c.create_category_sunburst_chart(),
            width='stretch',
        )

    st.plotly_chart(
        c.create_product_trend_chart(),
        width='stretch',
    )

    st.plotly_chart(
        c.create_low_performers_table(),
        width='stretch',
    )

with tab7:
    st.header("Time Series Analysis")

    st.plotly_chart(
        c.create_daily_sales_chart(),
        width='stretch',
    )
    col1, col2 = st.columns([2, 1])

    with col1:
        st.plotly_chart(
            c.create_monthly_revenue_profit_chart(),
            width='stretch',
        )

    with col2:
        st.plotly_chart(
            c.create_day_of_week_chart(),
            width='stretch',
        )

    col1, col2 = st.columns([1, 1])

    with col1:
        st.plotly_chart(
            c.create_weekly_heatmap(),
            width='stretch',
        )

    with col2:
        st.plotly_chart(
            c.create_quarterly_analysis_chart(),
            width='stretch',
        )

    st.plotly_chart(
        c.create_trend_decomposition_chart(),
        width='stretch',
    )
