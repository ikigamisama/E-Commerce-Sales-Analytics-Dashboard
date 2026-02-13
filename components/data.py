import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


US_STATE_ABBREV = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT",
    "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL",
    "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME",
    "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI",
    "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND",
    "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
    "Pennsylvania": "PA", "Rhode Island": "RI",
    "South Carolina": "SC", "South Dakota": "SD",
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}


@st.cache_data
def load_data(csv_file: str) -> pd.DataFrame:
    df = pd.read_csv(csv_file, encoding="cp1252")
    df['order_date'] = pd.to_datetime(df['order_date'], format="%d-%m-%Y")
    return df


class Data:
    def __init__(self, csv_file):
        self.df = load_data(csv_file)
        self.filtered_df = self.df.copy()

        # store filters internally
        self.filters = {
            "customer_region": None,
            "category_name": None,
            "customer_segment": None,
            "delivery_status": None,
            "shipping_type": None,
            "date_range": None,
        }

        self.df['order_date'] = pd.to_datetime(
            self.df['order_date'], format='%d-%m-%Y')

    def set_filters(self, **kwargs):
        self.filters.update(kwargs)
        self.apply_filters()

    def apply_filters(self):
        df = self.df.copy()

        date_range = self.filters.get("date_range")
        if date_range:
            start_date, end_date = pd.to_datetime(
                date_range[0]), pd.to_datetime(date_range[1])
            df = df[(df['order_date'] >= start_date)
                    & (df['order_date'] <= end_date)]

        for column in ["customer_region", "category_name", "customer_segment", "delivery_status", "shipping_type"]:
            values = self.filters.get(column)
            if values and len(values) > 0:
                df = df[df[column].isin(values)]

        self.filtered_df = df

    def unique_values(self, column):
        return sorted(self.df[column].unique())

    def compute_kpis(self):
        df = self.filtered_df

        total_revenue = df['sales_per_order'].sum()
        total_profit = df['profit_per_order'].sum()
        total_orders = len(df)
        profit_margin = (total_profit / total_revenue *
                         100) if total_revenue > 0 else 0
        avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
        on_time_rate = (df['delivery_status'] == 'Shipping on time').sum(
        ) / total_orders * 100 if total_orders > 0 else 0
        late_deliveries = (df['delivery_status'] == 'Late delivery').sum()

        return total_revenue, total_profit, total_orders, profit_margin, avg_order_value, on_time_rate, late_deliveries


PRIMARY_COLOR = '#13957b'
SECONDARY_COLORS = ['#13957b', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']


def apply_chart_styling(fig, title=""):
    fig.update_layout(
        title={
            'text': title,
            'font': {'size': 24, 'color': 'white' if st.get_option(
                "theme.base") != "dark" else "#2d3748"}
        } if title else None,
        font=dict(color='#2d3748'),
        margin=dict(l=10, r=10, t=50 if title else 10, b=10),
    )

    fig.update_xaxes(
        showgrid=True, gridcolor='rgba(128,128,128,0.2)', gridwidth=1)
    fig.update_yaxes(
        showgrid=True, gridcolor='rgba(128,128,128,0.2)', gridwidth=1)

    return fig


class Chart(Data):
    def __init__(self, csv_file: str, theme: str = "plotly"):
        super().__init__(csv_file)
        self.theme = theme

    def create_revenue_trend_chart(self):
        df_monthly = self.filtered_df.groupby(pd.Grouper(key='order_date', freq='ME')).agg({
            'sales_per_order': 'sum',
            'profit_per_order': 'sum'
        }).reset_index()

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(
                x=df_monthly['order_date'],
                y=df_monthly['sales_per_order'],
                name="Revenue",
                fill='tozeroy',
                line=dict(color='#13957b', width=3),
                hovertemplate='<b>Revenue</b><br>Date: %{x|%B %Y}<br>Amount: $%{y:,.0f}<extra></extra>'
            ),
            secondary_y=False
        )

        fig.add_trace(
            go.Scatter(
                x=df_monthly['order_date'],
                y=df_monthly['profit_per_order'],
                name="Profit",
                line=dict(color='#2ca02c', width=3),
                hovertemplate='<b>Profit</b><br>Date: %{x|%B %Y}<br>Amount: $%{y:,.0f}<extra></extra>'
            ),
            secondary_y=True
        )

        fig.update_layout(
            hovermode='x unified',
            height=500,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom",
                        y=1.02, xanchor="right", x=1),
        )

        fig.update_xaxes(title_text="Date", showgrid=True,
                         gridcolor='rgba(128,128,128,0.2)')

        apply_chart_styling(fig, "Revenue & Profit Trend Over Time")

        return fig

    def create_sales_by_category_chart(self):
        category_sales = self.filtered_df.groupby(
            'category_name')['sales_per_order'].sum().reset_index()

        fig = go.Figure(data=[go.Pie(
            labels=category_sales['category_name'],
            values=category_sales['sales_per_order'],
            hole=0.4,
            marker=dict(colors=['#13957b', '#ff7f0e', '#2ca02c']),
            hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
        )])

        fig.update_layout(
            title={
                'text': "Sales by Category",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            height=400,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom",
                        y=-0.2, xanchor="center", x=0.5),
        )

        return fig

    def create_revenue_by_region_chart(self):
        region_sales = self.filtered_df.groupby('customer_region')[
            'sales_per_order'].sum().sort_values(ascending=True).reset_index()

        fig = go.Figure(go.Bar(
            x=region_sales['sales_per_order'],
            y=region_sales['customer_region'],
            orientation='h',
            marker=dict(
                color=region_sales['sales_per_order'],
                colorscale='Blues',
                showscale=False
            ),
            text=region_sales['sales_per_order'].apply(
                lambda x: f'${x/1000000:.2f}M' if x >= 1000000 else f'${x/1000:.0f}K'),
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': "Revenue by Region",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title={'text': "Revenue ($)", 'font': {
                'size': 18, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}},
            yaxis_title={'text': "Region", 'font': {
                'size': 18, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}},
            height=400,
        )

        return fig

    def create_top_states_treemap(self):
        state_data = self.filtered_df.groupby(['customer_region', 'customer_state']).agg({
            'sales_per_order': 'sum',
            'profit_per_order': 'sum',
            'order_id': 'count'
        }).reset_index()

        state_data['profit_margin'] = (
            state_data['profit_per_order'] / state_data['sales_per_order'] * 100)
        top_states = state_data.nlargest(20, 'sales_per_order')

        fig = px.treemap(
            top_states,
            path=[px.Constant("All"), 'customer_region', 'customer_state'],
            values='sales_per_order',
            color='profit_margin',
            color_continuous_scale='RdYlGn',
            color_continuous_midpoint=top_states['profit_margin'].median(),
            hover_data={
                'sales_per_order': ':,.0f',
                'profit_per_order': ':,.0f',
                'profit_margin': ':.1f',
                'order_id': ':,',
                'customer_region': False
            },
            labels={
                'sales_per_order': 'Revenue',
                'profit_per_order': 'Profit',
                'profit_margin': 'Margin %',
                'order_id': 'Orders',
                'customer_state': 'State'
            }
        )

        fig.update_traces(
            hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.0f}<br>Profit: $%{customdata[0]:,.0f}<br>Margin: %{customdata[1]:.1f}%<br>Orders: %{customdata[2]:,}<extra></extra>',
            marker=dict(
                line=dict(width=2, color='white'),
                colorbar=dict(
                    title="Profit Margin %",
                    thickness=20,
                    len=0.7
                )
            )
        )

        fig.update_layout(
            title={
                'text': "Top 20 States by Revenue (Color = Profit Margin)",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            height=450,
        )

        return fig

    def create_sales_trend_by_category_chart(self):
        df_weekly = self.filtered_df.groupby([pd.Grouper(key='order_date', freq='W'), 'category_name'])[
            'sales_per_order'].sum().reset_index()

        fig = px.line(
            df_weekly,
            x='order_date',
            y='sales_per_order',
            color='category_name',
            labels={'order_date': 'Date',
                    'sales_per_order': 'Revenue ($)', 'category_name': 'Category'},
            color_discrete_sequence=['#13957b', '#ff7f0e', '#2ca02c']
        )

        fig.update_traces(mode='lines', hovertemplate='%{y:$,.0f}')

        fig.update_layout(
            title={
                'text': "Sales Trend by Category",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            height=400,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom",
                        y=1.02, xanchor="right", x=1,),
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month",
                             stepmode="backward"),
                        dict(count=3, label="3m", step="month",
                             stepmode="backward"),
                        dict(count=6, label="6m", step="month",
                             stepmode="backward"),
                        dict(step="all", label="All")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
        )

        return fig

    def create_top_products_chart(self):
        product_sales = self.filtered_df.groupby(['product_name', 'category_name'])[
            'sales_per_order'].sum().reset_index()
        top_products = product_sales.nlargest(
            20, 'sales_per_order').sort_values('sales_per_order', ascending=True)

        # Truncate long product names
        top_products['product_name_short'] = top_products['product_name'].apply(
            lambda x: x[:50] + '...' if len(x) > 50 else x
        )

        fig = px.bar(
            top_products,
            x='sales_per_order',
            y='product_name_short',
            color='category_name',
            orientation='h',
            labels={
                'sales_per_order': 'Revenue ($)', 'product_name_short': 'Product', 'category_name': 'Category'},
            color_discrete_sequence=['#13957b', '#ff7f0e', '#2ca02c']
        )

        fig.update_traces(
            hovertemplate='%{y}<br>Revenue: $%{x:,.0f}<extra></extra>')

        fig.update_layout(
            title={
                'text': "Top 20 Products by Revenue",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            height=600,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom",
                        y=1.02, xanchor="right", x=1)
        )

        return fig

    def create_sales_by_segment_chart(self):
        segment_sales = self.filtered_df.groupby(['category_name', 'customer_segment'])[
            'sales_per_order'].sum().reset_index()

        fig = px.bar(
            segment_sales,
            x='category_name',
            y='sales_per_order',
            color='customer_segment',
            barmode='group',
            labels={'category_name': 'Category',
                    'sales_per_order': 'Revenue ($)', 'customer_segment': 'Segment'},
            color_discrete_sequence=['#13957b', '#ff7f0e', '#2ca02c']
        )

        fig.update_traces(
            hovertemplate='%{x}<br>%{data.name}<br>Revenue: $%{y:,.0f}<extra></extra>')

        fig.update_layout(
            title={
                'text': "Sales by Customer Segment & Category",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            height=400,
            legend=dict(orientation="h", yanchor="bottom",
                        y=1.02, xanchor="right", x=1)
        )

        return fig

    def create_quantity_distribution_chart(self):
        quantity_dist = self.filtered_df['order_quantity'].value_counts(
        ).sort_index().reset_index()
        quantity_dist.columns = ['quantity', 'count']

        # Calculate percentages
        quantity_dist['percentage'] = (
            quantity_dist['count'] / quantity_dist['count'].sum() * 100).round(1)

        fig = go.Figure(go.Bar(
            x=quantity_dist['quantity'],
            y=quantity_dist['count'],
            marker=dict(
                color=['#13957b', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
            ),
            text=quantity_dist['percentage'].apply(lambda x: f'{x}%'),
            textposition='auto',
            hovertemplate='Quantity: %{x}<br>Orders: %{y:,}<br>Percentage: %{text}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': "Order Quantity Distribution",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                        "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title={'text': "Quantity per Order",
                         'font': {'size': 18, 'color': 'white' if st.get_option(
                             "theme.base") != "dark" else "#2d3748"}},
            yaxis_title={'text': "Number of Orders",
                         'font': {'size': 18, 'color': 'white' if st.get_option(
                             "theme.base") != "dark" else "#2d3748"}},
            height=400
        )

        return fig

    def create_monthly_sales_heatmap(self):
        df_copy = self.filtered_df.copy()

        df_copy['month'] = df_copy['order_date'].dt.month_name()
        df_copy['day_of_week'] = df_copy['order_date'].dt.day_name()

        # Aggregate
        heatmap_data = df_copy.groupby(['day_of_week', 'month'])[
            'sales_per_order'].sum().reset_index()

        # Pivot for heatmap
        heatmap_pivot = heatmap_data.pivot(
            index='day_of_week', columns='month', values='sales_per_order')

        # Reorder days and months
        days_order = ['Monday', 'Tuesday', 'Wednesday',
                      'Thursday', 'Friday', 'Saturday', 'Sunday']
        months_order = ['January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December']

        heatmap_pivot = heatmap_pivot.reindex(days_order)
        heatmap_pivot = heatmap_pivot[[
            m for m in months_order if m in heatmap_pivot.columns]]

        fig = go.Figure(data=go.Heatmap(
            z=heatmap_pivot.values,
            x=heatmap_pivot.columns,
            y=heatmap_pivot.index,
            colorscale='Blues',
            hovertemplate='%{y}, %{x}<br>Revenue: $%{z:,.0f}<extra></extra>',
            colorbar=dict(title={'text': "Revenue ($)", 'font': {
                        'size': 18, 'color': 'white' if st.get_option(
                            "theme.base") != "dark" else "#2d3748"}})
        ))

        fig.update_layout(
            title={
                'text': "Sales Heatmap: Day of Week vs Month",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title={'text': "Month", 'font': {
                'size': 18, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}},
            yaxis_title={'text': "Day of Week", 'font': {
                'size': 18, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}},
            height=700
        )

        return fig

    def create_profit_vs_revenue_scatter(self):
        df_sample = self.filtered_df.sample(n=min(5000, len(self.filtered_df)), random_state=42) if len(
            self.filtered_df) > 5000 else self.filtered_df

        fig = px.scatter(
            df_sample,
            x='sales_per_order',
            y='profit_per_order',
            color='category_name',
            size='order_quantity',
            labels={
                'sales_per_order': 'Revenue ($)', 'profit_per_order': 'Profit ($)', 'category_name': 'Category'},
            color_discrete_sequence=['#13957b', '#ff7f0e', '#2ca02c'],
            opacity=0.6
        )

        max_val = max(df_sample['sales_per_order'].max(),
                      df_sample['profit_per_order'].max())
        fig.add_trace(go.Scatter(
            x=[0, max_val],
            y=[0, max_val],
            mode='lines',
            name='Break-even Line',
            line=dict(color='red', dash='dash', width=2),
            hoverinfo='skip'
        ))

        fig.update_layout(
            title={
                'text': "Profit vs Revenue Analysis",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            height=500,
            legend=dict(orientation="h", yanchor="bottom",
                        y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        return fig

    def create_profit_margin_by_category_chart(self):
        df_copy = self.filtered_df.copy()
        df_copy['profit_margin'] = (
            df_copy['profit_per_order'] / df_copy['sales_per_order'] * 100)

        # Remove extreme outliers for better visualization
        df_copy = df_copy[df_copy['profit_margin'].between(-100, 100)]

        fig = px.box(
            df_copy,
            x='category_name',
            y='profit_margin',
            color='category_name',
            labels={'category_name': 'Category',
                    'profit_margin': 'Profit Margin (%)'},
            color_discrete_sequence=['#13957b', '#ff7f0e', '#2ca02c']
        )

        fig.update_layout(
            title={
                'text': "Profit Margin Distribution by Category",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            height=400,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        return fig

    def create_discount_impact_chart(self):
        fig = px.scatter(
            self.filtered_df,
            x='order_item_discount',
            y='profit_per_order',
            color='category_name',
            trendline='ols',
            labels={
                'order_item_discount': 'Discount (%)', 'profit_per_order': 'Profit ($)', 'category_name': 'Category'},
            color_discrete_sequence=['#13957b', '#ff7f0e', '#2ca02c'],
            opacity=0.5
        )

        fig.update_layout(
            title={
                'text': "Discount Impact on Profitability",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            height=400,
            legend=dict(orientation="h", yanchor="bottom",
                        y=1.02, xanchor="right", x=1)
        )

        return fig

    def create_top_profitable_products_chart(self):
        product_profit = self.filtered_df.groupby(
            'product_name')['profit_per_order'].sum().reset_index()
        top_products = product_profit.nlargest(10, 'profit_per_order').sort_values(
            'profit_per_order', ascending=False)

        # Truncate long names
        top_products['product_name_short'] = top_products['product_name'].apply(
            lambda x: x[:40] + '...' if len(x) > 40 else x
        )

        # Create waterfall values
        values = top_products['profit_per_order'].tolist()
        text = [f'${v:,.0f}' for v in values]

        fig = go.Figure(go.Waterfall(
            name="Profit",
            orientation="v",
            measure=["relative"] * len(values),
            x=top_products['product_name_short'],
            y=values,
            text=text,
            textposition="outside",
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "#2ca02c"}},
            decreasing={"marker": {"color": "#d62728"}},
            totals={"marker": {"color": "#13957b"}}
        ))

        fig.update_layout(
            title={
                'text': "Top 10 Most Profitable Products",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Product",
            yaxis_title="Profit ($)",
            height=500,
            showlegend=False
        )

        return fig

    def create_profit_margin_trend_chart(self):
        df_monthly = self.filtered_df.groupby(pd.Grouper(key='order_date', freq='ME')).agg({
            'sales_per_order': 'sum',
            'profit_per_order': 'sum',
            'order_item_discount': 'mean'
        }).reset_index()

        # Calculate profit margin
        df_monthly['profit_margin'] = (
            df_monthly['profit_per_order'] / df_monthly['sales_per_order'] * 100)

        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add profit margin trace
        fig.add_trace(
            go.Scatter(
                x=df_monthly['order_date'],
                y=df_monthly['profit_margin'],
                name="Profit Margin",
                line=dict(color='#2ca02c', width=3),
                hovertemplate='Profit Margin: %{y:.2f}%<extra></extra>'
            ),
            secondary_y=False
        )

        # Add average discount trace
        fig.add_trace(
            go.Scatter(
                x=df_monthly['order_date'],
                y=df_monthly['order_item_discount'],
                name="Avg Discount",
                line=dict(color='#ff7f0e', width=3, dash='dot'),
                hovertemplate='Avg Discount: %{y:.2f}%<extra></extra>'
            ),
            secondary_y=True
        )

        fig.update_layout(
            title={
                'text': "Profit Margin & Discount Trends",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified',
            height=400,
            legend=dict(orientation="h", yanchor="bottom",
                        y=1.02, xanchor="right", x=1)
        )

        fig.update_xaxes(title_text="Date", showgrid=True,
                         gridcolor='rgba(128,128,128,0.2)')

        return fig

    def create_delivery_status_chart(self):
        status_counts = self.filtered_df['delivery_status'].value_counts(
        ).reset_index()
        status_counts.columns = ['status', 'count']

        # Define colors
        colors = {
            'Shipping on time': '#2ca02c',
            'Late delivery': '#d62728',
            'Advance shipping': '#13957b',
            'Shipping canceled': '#7f7f7f'
        }

        color_list = [colors.get(status, '#13957b')
                      for status in status_counts['status']]

        # Create pull effect for late delivery
        pull = [0.1 if status ==
                'Late delivery' else 0 for status in status_counts['status']]

        fig = go.Figure(data=[go.Pie(
            labels=status_counts['status'],
            values=status_counts['count'],
            marker=dict(colors=color_list),
            pull=pull,
            hovertemplate='<b>%{label}</b><br>Orders: %{value:,}<br>Percentage: %{percent}<extra></extra>'
        )])

        fig.update_layout(
            title={
                'text': "Delivery Status Distribution",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom",
                        y=-0.1, xanchor="center", x=0.5)
        )

        return fig

    def create_delivery_by_shipping_type_chart(self):
        delivery_shipping = pd.crosstab(
            self.filtered_df['shipping_type'], self.filtered_df['delivery_status'], normalize='index') * 100

        colors = {
            'Shipping on time': '#2ca02c',
            'Late delivery': '#d62728',
            'Advance shipping': '#13957b',
            'Shipping canceled': '#7f7f7f'
        }

        fig = go.Figure()

        for status in delivery_shipping.columns:
            fig.add_trace(go.Bar(
                name=status,
                x=delivery_shipping.index,
                y=delivery_shipping[status],
                marker_color=colors.get(status, '#13957b'),
                hovertemplate='%{x}<br>%{data.name}: %{y:.1f}%<extra></extra>'
            ))

        fig.update_layout(
            title={
                'text': "Delivery Performance by Shipping Type",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Shipping Type",
            yaxis_title="Percentage (%)",
            barmode='stack',
            height=400,
            legend=dict(orientation="h", yanchor="bottom",
                        y=1.02, xanchor="right", x=1)
        )

        return fig

    def create_delivery_time_by_region_chart(self):
        region_stats = self.filtered_df.groupby('customer_region')[
            'days_for_shipment_real'].agg(['mean', 'std']).reset_index()
        region_stats.columns = ['region', 'mean_days', 'std_days']
        region_stats = region_stats.sort_values('mean_days', ascending=False)

        # Overall average
        overall_avg = self.filtered_df['days_for_shipment_real'].mean()

        fig = go.Figure()

        # Add bars with error bars
        fig.add_trace(go.Bar(
            x=region_stats['region'],
            y=region_stats['mean_days'],
            error_y=dict(
                type='data', array=region_stats['std_days'], visible=True),
            marker=dict(
                color=['#13957b', '#ff7f0e', '#2ca02c', '#d62728']
            ),
            text=region_stats['mean_days'].apply(lambda x: f'{x:.1f} days'),
            textposition='auto',
            hovertemplate='%{x}<br>Avg Days: %{y:.2f}<br>Std Dev: %{error_y.array:.2f}<extra></extra>'
        ))

        # Add overall average line
        fig.add_hline(
            y=overall_avg,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Overall Avg: {overall_avg:.1f} days",
            annotation_position="top right"
        )

        fig.update_layout(
            title={
                'text': "Average Delivery Time by Region (with Std Dev)",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title="Region",
            yaxis_title="Average Days",
            height=400,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        return fig

    def create_delivery_time_by_shipping_chart(self):
        fig = px.box(
            self.filtered_df,
            x='shipping_type',
            y='days_for_shipment_real',
            color='shipping_type',
            labels={'shipping_type': 'Shipping Type',
                    'days_for_shipment_real': 'Delivery Days'},
            color_discrete_sequence=['#13957b',
                                     '#ff7f0e', '#2ca02c', '#d62728']
        )

        fig.update_layout(
            title={
                'text': "Delivery Time Distribution by Shipping Type",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            height=400,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        return fig

    def create_late_delivery_trend_chart(self):
        df_weekly = (
            self.filtered_df
            .groupby(pd.Grouper(key='order_date', freq='W'))
            .agg(
                total_orders=('order_date', 'size'),
                late_deliveries=('delivery_status',
                                 lambda x: (x == 'Late delivery').sum()),
                canceled=('delivery_status',
                          lambda x: (x == 'Shipping canceled').sum())
            )
            .reset_index()
        )

        # Calculate rates
        df_weekly['late_rate'] = (
            df_weekly['late_deliveries'] / df_weekly['total_orders'] * 100)
        df_weekly['cancel_rate'] = (
            df_weekly['canceled'] / df_weekly['total_orders'] * 100)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_weekly['order_date'],
            y=df_weekly['late_rate'],
            name="Late Delivery Rate",
            line=dict(color='#d62728', width=2),
            hovertemplate='Late Rate: %{y:.2f}%<extra></extra>'
        ))

        fig.add_trace(go.Scatter(
            x=df_weekly['order_date'],
            y=df_weekly['cancel_rate'],
            name="Cancellation Rate",
            line=dict(color='#7f7f7f', width=2),
            hovertemplate='Cancel Rate: %{y:.2f}%<extra></extra>'
        ))

        fig.update_layout(
            title={'text': "Late Delivery & Cancellation Rate Trends (Weekly",
                   'font': {'size': 24, 'color': 'white' if st.get_option(
                       "theme.base") != "dark" else "#2d3748"}
                   },
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Date",
            yaxis_title="Rate (%)",
            hovermode='x unified',
            height=400,
            legend=dict(orientation="h", yanchor="bottom",
                        y=1.02, xanchor="right", x=1)
        )

        return fig

    def create_state_delivery_map(self):
        state_delivery = (
            self.filtered_df
            .groupby('customer_state')
            .agg(
                total_orders=('customer_state', 'size'),
                on_time=('delivery_status',
                         lambda x: (x == 'Shipping on time').sum()),
                late=('delivery_status',
                      lambda x: (x == 'Late delivery').sum())
            )
            .reset_index()
        )

        state_delivery['on_time_rate'] = (
            state_delivery['on_time'] / state_delivery['total_orders'] * 100)

        state_delivery['state_code'] = (
            state_delivery['customer_state']
            .str.strip()
            .map(US_STATE_ABBREV)
        )

        fig = go.Figure(data=go.Choropleth(
            locations=state_delivery['state_code'],
            z=state_delivery['on_time_rate'],
            locationmode='USA-states',
            colorscale='RdYlGn',
            colorbar_title="On-Time %",
            marker_line_color='white',
            customdata=np.column_stack((
                state_delivery['total_orders'],
                state_delivery['on_time'],
                state_delivery['late']
            )),
            hovertemplate='<b>%{location}</b><br>On-Time Rate: %{z:.1f}%<br>Total Orders: %{customdata[0]:,}<br>On-Time: %{customdata[1]:,}<br>Late: %{customdata[2]:,}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'On-Time Delivery Rate by State',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            geo_scope='usa',
            height=500
        )

        return fig

    def create_revenue_by_segment_funnel(self):
        segment_data = self.filtered_df.groupby('customer_segment').agg({
            'sales_per_order': 'sum',
            'order_id': 'count'
        }).reset_index()
        segment_data['aov'] = segment_data['sales_per_order'] / \
            segment_data['order_id']

        segment_data = segment_data.sort_values(
            'sales_per_order', ascending=False)

        fig = go.Figure(go.Funnel(
            y=segment_data['customer_segment'],
            x=segment_data['sales_per_order'],
            textinfo="value+percent initial",
            marker=dict(color=['#13957b', '#ff7f0e', '#2ca02c']),
            customdata=np.column_stack((
                segment_data['order_id'],
                segment_data['aov']
            )),
            hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.0f}<br>Orders: %{customdata[0]:,}<br>AOV: $%{customdata[1]:.2f}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': "Revenue by Customer Segment",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            height=400
        )

        return fig

    def create_top_cities_chart(self):
        city_sales = self.filtered_df.groupby(['customer_city', 'customer_state', 'customer_region'])[
            'sales_per_order'].sum().reset_index()
        top_cities = city_sales.nlargest(20, 'sales_per_order').sort_values(
            'sales_per_order', ascending=True)

        top_cities['city_state'] = top_cities['customer_city'] + \
            ', ' + top_cities['customer_state']

        fig = px.bar(
            top_cities,
            x='sales_per_order',
            y='city_state',
            color='customer_region',
            orientation='h',
            labels={
                'sales_per_order': 'Revenue ($)', 'city_state': 'City, State', 'customer_region': 'Region'},
            color_discrete_sequence=['#13957b',
                                     '#ff7f0e', '#2ca02c', '#d62728']
        )

        fig.update_traces(
            hovertemplate='%{y}<br>Revenue: $%{x:,.0f}<extra></extra>')

        fig.update_layout(
            title={
                'text': "Top 20 Cities by Revenue",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            height=600,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                        )
        )

        return fig

    def create_regional_radar_chart(self):
        region_metrics = (
            self.filtered_df
            .groupby('customer_region')
            .agg(
                revenue=('sales_per_order', 'sum'),
                profit=('profit_per_order', 'sum'),
                orders=('sales_per_order', 'size'),
                on_time=('delivery_status', lambda x: (
                    x == 'Shipping on time').sum())
            )
            .reset_index()
        )

        region_metrics['aov'] = region_metrics['revenue'] / \
            region_metrics['orders']
        region_metrics['on_time_pct'] = (
            region_metrics['on_time'] / region_metrics['orders'] * 100
        )

        # Normalize each metric to 0-100 scale
        for col in ['revenue', 'profit', 'orders', 'aov', 'on_time_pct']:
            max_val = region_metrics[col].max()
            if max_val > 0:
                region_metrics[f'{col}_norm'] = (
                    region_metrics[col] / max_val * 100)

        categories = ['Revenue', 'Profit', 'Orders',
                      'Avg Order Value', 'On-Time Delivery']

        fig = go.Figure()

        colors = ['#13957b', '#ff7f0e', '#2ca02c', '#d62728']

        for idx, region in enumerate(region_metrics['customer_region']):
            values = [
                region_metrics.loc[region_metrics['customer_region']
                                   == region, 'revenue_norm'].values[0],
                region_metrics.loc[region_metrics['customer_region']
                                   == region, 'profit_norm'].values[0],
                region_metrics.loc[region_metrics['customer_region']
                                   == region, 'orders_norm'].values[0],
                region_metrics.loc[region_metrics['customer_region']
                                   == region, 'aov_norm'].values[0],
                region_metrics.loc[region_metrics['customer_region']
                                   == region, 'on_time_pct_norm'].values[0]
            ]

            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=region,
                line=dict(color=colors[idx])
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100],
                                )
            ),
            title={'text': "Regional Performance Comparison (Normalized Metrics)", 'font': {'size': 24, 'color': 'white' if st.get_option(
                "theme.base") != "dark" else "#2d3748"}},
            height=500,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom",
                        y=-0.15, xanchor="center", x=0.5)
        )

        return fig

    def create_segment_category_preference_chart(self):
        segment_category = self.filtered_df.groupby(['customer_segment', 'category_name'])[
            'sales_per_order'].sum().reset_index()

        fig = px.bar(
            segment_category,
            x='customer_segment',
            y='sales_per_order',
            color='category_name',
            barmode='group',
            labels={'customer_segment': 'Customer Segment',
                    'sales_per_order': 'Revenue ($)', 'category_name': 'Category'},
            color_discrete_sequence=['#13957b', '#ff7f0e', '#2ca02c']
        )

        fig.update_traces(
            hovertemplate='%{x}<br>%{data.name}<br>Revenue: $%{y:,.0f}<extra></extra>')

        fig.update_layout(
            title={
                'text': "Category Preference by Customer Segment",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            height=400,
            legend=dict(orientation="h", yanchor="bottom",
                        y=1.02, xanchor="right", x=1)
        )

        return fig

    def create_state_revenue_map(self):
        state_revenue = self.filtered_df.groupby('customer_state').agg({
            'sales_per_order': 'sum',
            'profit_per_order': 'sum',
            'order_id': 'count'
        }).reset_index()

        state_revenue['state_code'] = (
            state_revenue['customer_state']
            .str.strip()
            .map(US_STATE_ABBREV)
        )

        fig = go.Figure(data=go.Choropleth(
            locations=state_revenue['state_code'],
            z=state_revenue['sales_per_order'],
            locationmode='USA-states',
            colorscale='Blues',
            colorbar_title="Revenue ($)",
            marker_line_color='white',
            customdata=np.column_stack((
                state_revenue['profit_per_order'],
                state_revenue['order_id']
            )),
            hovertemplate='<b>%{location}</b><br>Revenue: $%{z:,.0f}<br>Profit: $%{customdata[0]:,.0f}<br>Orders: %{customdata[1]:,}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': 'Revenue by State',
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            geo_scope='usa',
            height=500
        )

        return fig

    def create_pareto_chart(self):
        state_revenue = self.filtered_df.groupby('customer_state')[
            'sales_per_order'].sum().sort_values(ascending=False).reset_index()

        state_revenue['cumulative_revenue'] = state_revenue['sales_per_order'].cumsum()
        total_revenue = state_revenue['sales_per_order'].sum()
        state_revenue['cumulative_pct'] = (
            state_revenue['cumulative_revenue'] / total_revenue * 100)

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add bars
        fig.add_trace(
            go.Bar(
                x=state_revenue['customer_state'],
                y=state_revenue['sales_per_order'],
                name="Revenue",
                marker_color='#13957b',
                hovertemplate='%{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
            ),
            secondary_y=False
        )

        # Add cumulative line
        fig.add_trace(
            go.Scatter(
                x=state_revenue['customer_state'],
                y=state_revenue['cumulative_pct'],
                name="Cumulative %",
                line=dict(color='#ff7f0e', width=3),
                hovertemplate='Cumulative: %{y:.1f}%<extra></extra>'
            ),
            secondary_y=True
        )

        # Add 80% reference line
        fig.add_hline(
            y=80,
            line_dash="dash",
            line_color="red",
            secondary_y=True,
            annotation_text="80%",
            annotation_position="right"
        )

        fig.update_layout(
            title={'text': "Revenue Pareto Chart (80/20 Analysis by State",
                   'font': {'size': 24, 'color': 'white' if st.get_option(
                       "theme.base") != "dark" else "#2d3748"}
                   },
            hovermode='x unified',
            height=500,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom",
                        y=1.02, xanchor="right", x=1)
        )

        fig.update_xaxes(title_text="State", tickangle=45,
                         showgrid=True, gridcolor='rgba(128,128,128,0.2)')

        return fig

    def create_product_matrix_chart(self):

        product_data = self.filtered_df.groupby(['product_name', 'category_name']).agg({
            'sales_per_order': 'sum',
            'profit_per_order': 'sum',
            'order_id': 'count'
        }).reset_index()

        product_data = product_data.nlargest(100, 'sales_per_order')

        avg_revenue = product_data['sales_per_order'].median()
        avg_profit = product_data['profit_per_order'].median()

        fig = px.scatter(
            product_data,
            x='sales_per_order',
            y='profit_per_order',
            size='order_id',
            color='category_name',
            hover_name='product_name',
            labels={'sales_per_order': 'Total Revenue ($)', 'profit_per_order': 'Total Profit ($)',
                    'category_name': 'Category', 'order_id': 'Orders'},
            color_discrete_sequence=['#13957b', '#ff7f0e', '#2ca02c'],
            opacity=0.7
        )

        # Add quadrant lines
        fig.add_vline(x=avg_revenue, line_dash="dash",
                      line_color="gray", opacity=0.5)
        fig.add_hline(y=avg_profit, line_dash="dash",
                      line_color="gray", opacity=0.5)

        # Add quadrant labels
        max_revenue = product_data['sales_per_order'].max()
        max_profit = product_data['profit_per_order'].max()
        min_profit = product_data['profit_per_order'].min()

        annotations = [
            dict(x=max_revenue * 0.85, y=max_profit * 0.9, text="Stars", showarrow=False,
                 font=dict(size=14, color="green"), opacity=0.5),
            dict(x=avg_revenue * 0.3, y=max_profit * 0.9, text="Profitable Niche", showarrow=False,
                 font=dict(size=14, color="blue"), opacity=0.5),
            dict(x=max_revenue * 0.85, y=avg_profit * 0.3, text="Volume Drivers", showarrow=False,
                 font=dict(size=14, color="orange"), opacity=0.5),
            dict(x=avg_revenue * 0.3, y=avg_profit * 0.3, text="Low Performers", showarrow=False,
                 font=dict(size=14, color="red"), opacity=0.5)
        ]

        fig.update_layout(
            title={
                'text': "Product Performance Matrix (Top 100 Products)",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            annotations=annotations,
            height=600,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                        )
        )

        return fig

    def create_top_quantity_products_chart(self):
        product_qty = self.filtered_df.groupby(['product_name', 'category_name'])[
            'order_quantity'].sum().reset_index()
        top_products = product_qty.nlargest(20, 'order_quantity').sort_values(
            'order_quantity', ascending=True)

        # Truncate names
        top_products['product_name_short'] = top_products['product_name'].apply(
            lambda x: x[:50] + '...' if len(x) > 50 else x
        )

        fig = px.bar(
            top_products,
            x='order_quantity',
            y='product_name_short',
            color='category_name',
            orientation='h',
            labels={'order_quantity': 'Total Units Sold',
                    'product_name_short': 'Product', 'category_name': 'Category'},
            color_discrete_sequence=['#13957b', '#ff7f0e', '#2ca02c']
        )

        fig.update_traces(hovertemplate='%{y}<br>Units: %{x:,}<extra></extra>')

        fig.update_layout(
            title={
                'text': "Top 20 Products by Units Sold",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            height=600,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                        )
        )

        return fig

    def create_category_sunburst_chart(self):
        product_data = self.filtered_df.groupby(['category_name', 'product_name']).agg({
            'sales_per_order': 'sum',
            'profit_per_order': 'sum'
        }).reset_index()

        product_data['profit_margin'] = (
            product_data['profit_per_order'] / product_data['sales_per_order'] * 100)

        top_products = product_data.groupby('category_name').apply(
            lambda x: x.nlargest(5, 'sales_per_order')
        ).reset_index(drop=True)

        category_totals = self.filtered_df.groupby('category_name').agg({
            'sales_per_order': 'sum',
            'profit_per_order': 'sum'
        }).reset_index()
        category_totals['profit_margin'] = (
            category_totals['profit_per_order'] / category_totals['sales_per_order'] * 100)
        category_totals['product_name'] = ''

        labels = ['All Categories'] + category_totals['category_name'].tolist() + \
            top_products['product_name'].tolist()
        parents = [''] + ['All Categories'] * \
            len(category_totals) + top_products['category_name'].tolist()
        values = [category_totals['sales_per_order'].sum(
        )] + category_totals['sales_per_order'].tolist() + top_products['sales_per_order'].tolist()

        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            branchvalues="total",
            marker=dict(
                colorscale='RdYlGn',
                cmid=0,
                colorbar=dict(title="Profit Margin %")
            ),
            hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.0f}<extra></extra>'
        ))

        fig.update_layout(
            title={'text': "Product Category Deep Dive (Top 5 Products per Category",
                   'font': {'size': 24, 'color': 'white' if st.get_option(
                       "theme.base") != "dark" else "#2d3748"}
                   },
            height=600
        )

        return fig

    def create_product_trend_chart(self, selected_products=None):
        if selected_products is None:
            top_products = self.filtered_df.groupby(
                'product_name')['sales_per_order'].sum().nlargest(5).index.tolist()
            selected_products = top_products

        df_filtered = self.filtered_df[self.filtered_df['product_name'].isin(
            selected_products)]

        df_monthly = df_filtered.groupby([pd.Grouper(key='order_date', freq='ME'), 'product_name'])[
            'sales_per_order'].sum().reset_index()

        fig = px.line(
            df_monthly,
            x='order_date',
            y='sales_per_order',
            color='product_name',
            labels={'order_date': 'Date',
                    'sales_per_order': 'Revenue ($)', 'product_name': 'Product'}
        )

        fig.update_traces(mode='lines+markers', hovertemplate='%{y:$,.0f}')

        fig.update_layout(
            title={
                'text': "Product Performance Over Time (Top 5 Products)",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            height=400,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                        )
        )

        return fig

    def create_low_performers_table(self):
        product_data = self.filtered_df.groupby(['product_name', 'category_name']).agg({
            'order_id': 'count',
            'sales_per_order': 'sum',
            'profit_per_order': 'sum'
        }).reset_index()

        product_data['profit_margin'] = (
            product_data['profit_per_order'] / product_data['sales_per_order'] * 100)
        low_performers = product_data[
            (product_data['profit_per_order'] < 0) |
            (product_data['sales_per_order'] <
             product_data['sales_per_order'].quantile(0.1))
        ].sort_values('profit_per_order')

        low_performers = low_performers.head(20)

        fig = go.Figure(data=[go.Table(
            header=dict(
                values=['<b>Product</b>', '<b>Category</b>', '<b>Orders</b>',
                        '<b>Revenue</b>', '<b>Profit</b>', '<b>Margin %</b>'],
                fill_color='#13957b',
                font=dict(color='white', size=12),
                align='left'
            ),
            cells=dict(
                values=[
                    low_performers['product_name'].apply(
                        lambda x: x[:40] + '...' if len(x) > 40 else x),
                    low_performers['category_name'],
                    low_performers['order_id'],
                    low_performers['sales_per_order'].apply(
                        lambda x: f'${x:,.0f}'),
                    low_performers['profit_per_order'].apply(
                        lambda x: f'${x:,.0f}'),
                    low_performers['profit_margin'].apply(
                        lambda x: f'{x:.1f}%')
                ],
                fill_color=[['white', '#f0f0f0'] * len(low_performers)],
                font=dict(color=[
                    'black', 'black', 'black', 'black',
                    ['red' if x < 0 else 'black' for x in low_performers['profit_per_order']],
                    ['red' if x < 0 else 'black' for x in low_performers['profit_margin']]
                ]),
                align='left'
            )
        )])

        fig.update_layout(
            title={'text': "Low Performing Products (Negative Profit or Bottom 10% Sales",
                   'font': {'size': 24, 'color': 'white' if st.get_option(
                       "theme.base") != "dark" else "#2d3748"}
                   },
            height=500
        )

        return fig

    def create_daily_sales_chart(self):
        df_daily = self.filtered_df.groupby(
            'order_date')['sales_per_order'].sum().reset_index()

        df_daily['ma_7'] = df_daily['sales_per_order'].rolling(
            window=7, min_periods=1).mean()
        df_daily['ma_30'] = df_daily['sales_per_order'].rolling(
            window=30, min_periods=1).mean()

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_daily['order_date'],
            y=df_daily['sales_per_order'],
            name="Daily Sales",
            line=dict(color='lightblue', width=1),
            hovertemplate='Daily: $%{y:,.0f}<extra></extra>'
        ))

        fig.add_trace(go.Scatter(
            x=df_daily['order_date'],
            y=df_daily['ma_7'],
            name="7-Day Moving Avg",
            line=dict(color='#13957b', width=2),
            hovertemplate='7-Day MA: $%{y:,.0f}<extra></extra>'
        ))

        fig.add_trace(go.Scatter(
            x=df_daily['order_date'],
            y=df_daily['ma_30'],
            name="30-Day Moving Avg",
            line=dict(color='#ff7f0e', width=3),
            hovertemplate='30-Day MA: $%{y:,.0f}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': "Daily Sales Pattern with Moving Averages",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title="Date",
            yaxis_title="Revenue ($)",
            hovermode='x unified',
            height=400,
            legend=dict(orientation="h", yanchor="bottom",
                        y=1.02, xanchor="right", x=1),
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month",
                             stepmode="backward"),
                        dict(count=3, label="3m", step="month",
                             stepmode="backward"),
                        dict(count=6, label="6m", step="month",
                             stepmode="backward"),
                        dict(step="all", label="All")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
        )

        return fig

    def create_monthly_revenue_profit_chart(self):
        df_monthly = self.filtered_df.groupby(pd.Grouper(key='order_date', freq='ME')).agg({
            'sales_per_order': 'sum',
            'profit_per_order': 'sum'
        }).reset_index()

        df_monthly['profit_margin'] = (
            df_monthly['profit_per_order'] / df_monthly['sales_per_order'] * 100)

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(
                x=df_monthly['order_date'],
                y=df_monthly['sales_per_order'],
                name="Revenue",
                marker_color='#13957b',
                hovertemplate='Revenue: $%{y:,.0f}<extra></extra>'
            ),
            secondary_y=False
        )

        # Add profit bars
        fig.add_trace(
            go.Bar(
                x=df_monthly['order_date'],
                y=df_monthly['profit_per_order'],
                name="Profit",
                marker_color='#2ca02c',
                hovertemplate='Profit: $%{y:,.0f}<extra></extra>'
            ),
            secondary_y=False
        )

        # Add profit margin line
        fig.add_trace(
            go.Scatter(
                x=df_monthly['order_date'],
                y=df_monthly['profit_margin'],
                name="Profit Margin",
                line=dict(color='#ff7f0e', width=3),
                hovertemplate='Margin: %{y:.2f}%<extra></extra>'
            ),
            secondary_y=True
        )

        fig.update_layout(
            title={
                'text': "Monthly Revenue, Profit & Margin",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            hovermode='x unified',
            height=400,
            barmode='group',
            legend=dict(orientation="h", yanchor="bottom",
                        y=1.02, xanchor="right", x=1)
        )

        fig.update_xaxes(title_text="Month", showgrid=True,
                         gridcolor='rgba(128,128,128,0.2)')

        return fig

    def create_day_of_week_chart(self):
        df_copy = self.filtered_df.copy()
        df_copy['day_of_week'] = df_copy['order_date'].dt.day_name()
        df_copy['day_num'] = df_copy['order_date'].dt.dayofweek

        # Aggregate by day of week
        dow_sales = df_copy.groupby(['day_num', 'day_of_week'])[
            'sales_per_order'].mean().reset_index()
        dow_sales = dow_sales.sort_values('day_num')

        fig = go.Figure(go.Bar(
            x=dow_sales['day_of_week'],
            y=dow_sales['sales_per_order'],
            marker=dict(
                color=dow_sales['sales_per_order'],
                colorscale='Blues',
                showscale=False
            ),
            text=dow_sales['sales_per_order'].apply(lambda x: f'${x:,.0f}'),
            textposition='auto',
            hovertemplate='%{x}<br>Avg Revenue: $%{y:,.0f}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': "Average Revenue by Day of Week",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title="Day of Week",
            yaxis_title="Average Revenue ($)",
            height=400
        )

        return fig

    def create_weekly_heatmap(self):
        df_copy = self.filtered_df.copy()
        df_copy['week'] = df_copy['order_date'].dt.isocalendar().week
        df_copy['day_of_week'] = df_copy['order_date'].dt.day_name()

        heatmap_data = df_copy.groupby(['day_of_week', 'week'])[
            'sales_per_order'].sum().reset_index()

        heatmap_pivot = heatmap_data.pivot(
            index='day_of_week', columns='week', values='sales_per_order')

        days_order = ['Monday', 'Tuesday', 'Wednesday',
                      'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_pivot = heatmap_pivot.reindex(days_order)

        fig = go.Figure(data=go.Heatmap(
            z=heatmap_pivot.values,
            x=heatmap_pivot.columns,
            y=heatmap_pivot.index,
            colorscale='Blues',
            hovertemplate='Week %{x}, %{y}<br>Revenue: $%{z:,.0f}<extra></extra>',
            colorbar=dict(title="Revenue ($)")
        ))

        fig.update_layout(
            title={
                'text': "Weekly Sales Heatmap: Week Number vs Day of Week",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            xaxis_title="Week Number",
            yaxis_title="Day of Week",
            height=400
        )

        return fig

    def create_quarterly_analysis_chart(self):
        df_copy = self.filtered_df.copy()
        df_copy['quarter'] = df_copy['order_date'].dt.quarter
        df_copy['month'] = df_copy['order_date'].dt.month

        # Aggregate by quarter and month
        quarterly_data = df_copy.groupby(['quarter', 'month'])[
            'sales_per_order'].sum().reset_index()
        quarterly_data['quarter_label'] = 'Q' + \
            quarterly_data['quarter'].astype(str)

        fig = px.line(
            quarterly_data,
            x='month',
            y='sales_per_order',
            color='quarter_label',
            markers=True,
            labels={'month': 'Month',
                    'sales_per_order': 'Revenue ($)', 'quarter_label': 'Quarter'}
        )

        fig.update_layout(
            title={
                'text': "Quarterly Revenue Comparison",
                'font': {'size': 24, 'color': 'white' if st.get_option(
                    "theme.base") != "dark" else "#2d3748"}
            },
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                        )
        )

        return fig

    def create_trend_decomposition_chart(self):
        df_weekly = self.filtered_df.groupby(pd.Grouper(key='order_date', freq='W'))[
            'sales_per_order'].sum().reset_index()

        df_weekly['trend'] = df_weekly['sales_per_order'].rolling(
            window=4, center=True, min_periods=1).mean()
        df_weekly['seasonal'] = df_weekly['sales_per_order'] - \
            df_weekly['trend']
        df_weekly['residual'] = df_weekly['sales_per_order'] - \
            df_weekly['trend'] - df_weekly['seasonal']

        fig = make_subplots(
            rows=4, cols=1,
            subplot_titles=('Original', 'Trend', 'Seasonal', 'Residual'),
            vertical_spacing=0.08
        )

        fig.add_trace(
            go.Scatter(x=df_weekly['order_date'], y=df_weekly['sales_per_order'],
                       name='Original', line=dict(color='#13957b')),
            row=1, col=1
        )

        # Trend
        fig.add_trace(
            go.Scatter(x=df_weekly['order_date'], y=df_weekly['trend'],
                       name='Trend', line=dict(color='#ff7f0e')),
            row=2, col=1
        )

        # Seasonal
        fig.add_trace(
            go.Scatter(x=df_weekly['order_date'], y=df_weekly['seasonal'],
                       name='Seasonal', line=dict(color='#2ca02c')),
            row=3, col=1
        )

        # Residual
        fig.add_trace(
            go.Scatter(x=df_weekly['order_date'], y=df_weekly['residual'],
                       name='Residual', line=dict(color='#d62728')),
            row=4, col=1
        )

        fig.update_layout(
            title_text="Sales Trend Decomposition (Weekly)",
            height=800,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        return fig
