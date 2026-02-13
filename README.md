# 📊 E-Commerce Sales Analytics Dashboard

A comprehensive, interactive dashboard for analyzing e-commerce sales performance, built with Streamlit and Plotly. This dashboard provides deep insights into sales, profitability, customer behavior, shipping performance, and time-based trends.

---

## 🎯 Purpose

This dashboard is designed to help e-commerce businesses:

- **Monitor Key Performance Indicators** in real-time
- **Identify sales trends and patterns** across products, categories, and regions
- **Optimize profitability** by understanding discount impacts and margin drivers
- **Improve delivery performance** by tracking shipping metrics
- **Understand customer behavior** across different segments and geographies
- **Make data-driven decisions** with comprehensive visualizations

---

## 📈 Dashboard Structure

### Main KPIs (Always Visible)

Four critical metrics displayed prominently at the top of every view:

1. **Total Revenue** - Overall sales performance with period comparison
2. **Total Profit** - Net profitability with margin percentage
3. **Total Orders** - Order volume with average order value
4. **On-Time Delivery Rate** - Shipping performance with target indicators

These KPIs update dynamically based on filter selections and provide an at-a-glance view of business health.

---

## 🔍 Sidebar Filters

Interactive filters allow you to slice and dice the data:

- **Date Range** - Analyze any time period
- **Region** - East, Central, South, West
- **Category** - Office Supplies, Furniture, Technology
- **Customer Segment** - Corporate, Consumer, Home Office
- **Delivery Status** - On-time, Late, Advance, Canceled
- **Shipping Type** - Standard, Second Class, First Class, Same Day
- **State & City** - Drill down to specific locations

All filters apply across all tabs and update all visualizations simultaneously.

---

## 📑 Tab 1: Overview Dashboard

**Purpose**: Provide a high-level summary of business performance

### Revenue & Profit Trend Over Time

**What it shows**: Monthly revenue and profit progression throughout the year

**Business value**:

- Identify seasonal patterns and growth trends
- Spot anomalies or unexpected drops
- Compare revenue vs. profit trajectory
- Plan for high and low seasons

### Sales by Category

**What it shows**: Revenue distribution across product categories (donut chart)

**Business value**:

- Understand which categories drive the most revenue
- Identify portfolio concentration or diversification
- Make inventory and marketing decisions
- Spot category performance shifts

### Revenue by Region

**What it shows**: Total sales for each geographic region (horizontal bars)

**Business value**:

- Identify strongest and weakest regional markets
- Allocate marketing budgets effectively
- Plan regional expansion or consolidation
- Compare regional performance at a glance

### Top 10 States by Revenue

**What it shows**: Hierarchical view of top-performing states grouped by region (treemap)

**Business value**:

- Visualize geographic concentration of sales
- Identify high-value state markets
- Understand profit margins by location (color-coded)
- Plan state-level strategies and resources

---

## 📑 Tab 2: Sales Analysis

**Purpose**: Deep dive into sales patterns, product performance, and customer preferences

### Sales Trend by Category

**What it shows**: Weekly revenue trends for each product category over time

**Business value**:

- Compare category performance side-by-side
- Identify which categories are growing or declining
- Spot seasonal demand patterns by category
- Adjust inventory and procurement strategies

### Top 20 Products by Revenue

**What it shows**: Highest-grossing products with category breakdown

**Business value**:

- Focus on bestsellers for promotions and stock
- Understand which products drive the most value
- Identify star products vs. underperformers
- Make product mix decisions

### Sales by Customer Segment & Category

**What it shows**: Revenue split across Corporate, Consumer, and Home Office buyers by category

**Business value**:

- Understand who buys what products
- Tailor marketing messages to specific segments
- Identify cross-selling opportunities
- Optimize product offerings per segment

### Order Quantity Distribution

**What it shows**: How many items customers typically buy per order

**Business value**:

- Understand buying behavior patterns
- Set bulk discount thresholds intelligently
- Optimize packaging and shipping strategies
- Identify opportunities for bundle promotions

### Monthly Sales Heatmap

**What it shows**: Sales intensity by day of week and month

**Business value**:

- Identify peak sales days and periods
- Optimize staffing and inventory for busy times
- Plan promotions during slow periods
- Understand weekly and monthly patterns

---

## 📑 Tab 3: Profitability Analysis

**Purpose**: Understand what drives profit and where margins are strongest or weakest

### Profit vs Revenue Scatter Plot

**What it shows**: Relationship between sales and profit for individual orders

**Business value**:

- Identify profitable vs. unprofitable sales patterns
- Spot orders that generate revenue but lose money
- Understand the break-even relationship
- Find optimal pricing sweet spots

### Profit Margin by Category

**What it shows**: Profit margin distribution and variability across categories (box plot)

**Business value**:

- Compare profitability across product categories
- Identify consistent vs. volatile margin categories
- Spot outliers and investigate causes
- Set category-specific pricing strategies

### Discount Impact on Profitability

**What it shows**: How discount levels correlate with profit (scatter with trendline)

**Business value**:

- Understand if discounts are eroding profits
- Find the optimal discount range
- Identify which categories can sustain discounts
- Make data-driven promotional decisions

### Top 10 Most Profitable Products

**What it shows**: Products contributing the most to bottom-line profit (waterfall chart)

**Business value**:

- Focus on high-profit products
- Understand cumulative profit contribution
- Protect and promote profit drivers
- Balance profit vs. volume strategies

### Profit Margin & Discount Trends

**What it shows**: How margins and average discounts have evolved over time

**Business value**:

- Identify if aggressive discounting is hurting margins
- Spot trends and turning points
- Align promotional calendars with margin goals
- Monitor the health of pricing strategy

---

## 📑 Tab 4: Shipping & Delivery Performance

**Purpose**: Monitor and improve delivery operations and customer satisfaction

### Delivery Status Distribution

**What it shows**: Breakdown of on-time, late, advance, and canceled deliveries (pie chart)

**Business value**:

- Monitor overall delivery performance
- Track service level targets
- Identify problem areas needing attention
- Understand customer experience quality

### Delivery Performance by Shipping Type

**What it shows**: On-time rates for Standard, Second Class, First Class, and Same Day shipping

**Business value**:

- Compare service levels across shipping methods
- Identify which shipping types need improvement
- Make informed carrier and service decisions
- Set customer expectations accurately

### Average Delivery Time by Region

**What it shows**: Mean delivery days for each region with variability indicators

**Business value**:

- Understand regional logistics challenges
- Set region-specific delivery promises
- Identify areas for warehouse expansion
- Optimize distribution networks

### Delivery Time Distribution by Shipping Type

**What it shows**: Spread of delivery times for each shipping method (box plot)

**Business value**:

- Understand consistency of each shipping option
- Identify unreliable services
- Set realistic delivery estimates
- Improve carrier selection

### Late Delivery & Cancellation Rate Trends

**What it shows**: Weekly trends in problematic deliveries

**Business value**:

- Spot deteriorating delivery performance early
- Correlate with operational changes
- Set improvement targets and track progress
- Identify seasonal delivery challenges

### On-Time Delivery Rate by State

**What it shows**: Geographic map of delivery performance across the US

**Business value**:

- Identify problem states for logistics
- Plan regional improvements
- Understand geographic service quality
- Make location-based operational decisions

---

## 📑 Tab 5: Customer & Geographic Analysis

**Purpose**: Understand customer segments and geographic performance patterns

### Revenue by Customer Segment

**What it shows**: Total revenue contribution from Corporate, Consumer, and Home Office buyers (funnel)

**Business value**:

- Understand segment importance and priority
- Allocate sales and marketing resources
- Identify high-value customer types
- Track segment-specific metrics like AOV

### Top 20 Cities by Revenue

**What it shows**: Highest-revenue cities with regional grouping

**Business value**:

- Identify key urban markets
- Plan city-specific marketing campaigns
- Consider local warehouse or fulfillment centers
- Target high-potential markets

### Regional Performance Comparison

**What it shows**: Multi-dimensional comparison of regions across revenue, profit, orders, AOV, and delivery (radar chart)

**Business value**:

- Compare regions holistically, not just on revenue
- Identify well-rounded vs. one-dimensional regions
- Set balanced regional goals
- Understand regional strengths and weaknesses

### Category Preference by Customer Segment

**What it shows**: Which product categories each customer type prefers

**Business value**:

- Tailor product recommendations by segment
- Create segment-specific catalogs
- Optimize marketing messages and channels
- Understand segment buying behavior

### Revenue by State

**What it shows**: US heat map showing sales concentration

**Business value**:

- Visualize geographic sales distribution
- Identify expansion opportunities
- Understand market penetration
- Plan state-level strategies

### Revenue Pareto Chart

**What it shows**: 80/20 analysis showing how revenue is concentrated across states

**Business value**:

- Identify the vital few states driving most revenue
- Focus resources on high-impact markets
- Understand revenue concentration risk
- Make strategic market prioritization decisions

---

## 📑 Tab 6: Product Performance

**Purpose**: Analyze individual product success and identify opportunities

### Product Performance Matrix

**What it shows**: Products plotted by revenue vs. profit with order volume (bubble chart)

**Business value**:

- Categorize products as Stars, Volume Drivers, Niche, or Low Performers
- Make portfolio management decisions
- Identify products to promote, optimize, or discontinue
- Balance high-volume vs. high-margin products

### Top 20 Products by Units Sold

**What it shows**: Best-selling products by quantity rather than dollars

**Business value**:

- Understand volume movers for inventory planning
- Identify products with mass appeal
- Plan production and procurement
- Consider bundling high-volume products

### Product Category Deep Dive

**What it shows**: Hierarchical view of categories and their top products (sunburst)

**Business value**:

- Explore product hierarchy interactively
- Understand product mix within categories
- Identify dominant products per category
- Make assortment planning decisions

### Product Performance Over Time

**What it shows**: Revenue trends for top products month-by-month

**Business value**:

- Identify products with growing vs. declining sales
- Spot seasonal product patterns
- Compare product trajectories
- Time product promotions and lifecycle decisions

### Low Performing Products

**What it shows**: Products with negative profit or bottom-tier sales (table)

**Business value**:

- Identify candidates for discontinuation
- Investigate causes of poor performance
- Consider repricing or repositioning
- Free up resources for better opportunities

---

## 📑 Tab 7: Time Series Analysis

**Purpose**: Understand temporal patterns and forecast future trends

### Daily Sales Pattern

**What it shows**: Day-by-day revenue with 7-day and 30-day moving averages

**Business value**:

- Smooth out noise to see true trends
- Identify underlying growth or decline
- Spot unusual spikes or drops
- Support short-term forecasting

### Monthly Revenue & Profit Bars

**What it shows**: Month-by-month performance with profit margin overlay

**Business value**:

- Compare monthly performance year-to-date
- Understand seasonal patterns
- Track margin evolution over time
- Plan annual budgets and forecasts

### Average Revenue by Day of Week

**What it shows**: Which days of the week generate the most sales

**Business value**:

- Optimize promotional timing
- Plan staffing and inventory by day
- Understand customer shopping habits
- Schedule maintenance during slow days

### Weekly Sales Heatmap

**What it shows**: Sales intensity by week number and day of week

**Business value**:

- Visualize seasonal and weekly patterns simultaneously
- Identify busy vs. slow weeks
- Plan promotions for low-activity periods
- Understand annual sales rhythm

### Quarterly Revenue Comparison

**What it shows**: How each quarter performed throughout the year

**Business value**:

- Compare quarterly performance
- Identify strongest and weakest quarters
- Set quarterly targets and goals
- Understand business seasonality

### Sales Trend Decomposition

**What it shows**: Sales broken down into trend, seasonal, and residual components

**Business value**:

- Separate long-term trends from seasonal effects
- Understand true growth after removing seasonality
- Identify irregular events and anomalies
- Build more accurate forecasts

---

## 🎯 Key Business Questions This Dashboard Answers

### Revenue & Growth

- What is our total revenue and how is it trending?
- Which products, categories, and regions drive the most sales?
- Are we growing or declining month-over-month?
- What are our seasonal sales patterns?

### Profitability

- What is our overall profit margin?
- Which products and categories are most profitable?
- Are discounts helping or hurting profitability?
- Where are we losing money?

### Customer Insights

- Who are our most valuable customer segments?
- What do different segments buy?
- Where are our customers located?
- What is our average order value?

### Operational Excellence

- Are we delivering orders on time?
- Which regions have the best/worst delivery performance?
- What percentage of orders are canceled?
- Which shipping methods are most reliable?

### Product Strategy

- What are our bestselling products?
- Which products should we promote or discontinue?
- How is our product mix performing?
- What is the lifecycle stage of each product?

### Geographic Strategy

- Which states and cities are our strongest markets?
- Where should we expand or focus resources?
- Are there untapped geographic opportunities?
- How concentrated is our revenue geographically?

---

## 💡 Use Cases

### For Executives

- Monitor overall business health through main KPIs
- Understand high-level trends and patterns
- Make strategic decisions on markets and products
- Track progress toward company goals

### For Sales Teams

- Identify top-performing products to push
- Understand customer segment preferences
- Find geographic opportunities
- Track sales performance over time

### For Marketing Teams

- Understand which products and categories to promote
- Optimize discount and promotional strategies
- Target the right customer segments
- Time campaigns based on seasonal patterns

### For Operations Teams

- Monitor and improve delivery performance
- Identify logistics bottlenecks by region
- Optimize inventory based on demand patterns
- Plan staffing and resources for peak periods

### For Finance Teams

- Track profitability and margins
- Understand discount impacts on bottom line
- Analyze revenue concentration and risk
- Support budgeting and forecasting

### For Product Teams

- Identify product winners and losers
- Make portfolio management decisions
- Understand product lifecycles
- Prioritize product development resources

---

## 🌟 Key Features

### Interactive Filtering

Every chart responds to sidebar filters in real-time, allowing for dynamic exploration of the data from multiple angles.

### Transparent Design

Charts feature transparent backgrounds that adapt seamlessly to Streamlit's light and dark themes.

### Professional Aesthetics

Consistent color scheme (#13957b primary color), clean typography, and thoughtful layout create a polished, professional appearance.

### Comprehensive Coverage

40+ charts across 7 themed tabs provide 360-degree visibility into all aspects of e-commerce performance.

### Export-Ready

All charts can be downloaded as high-resolution images for use in presentations and reports.

### Responsive Layout

Charts automatically adjust to different screen sizes and display configurations.

---

## 📊 Data Coverage

This dashboard analyzes:

- **113,270 orders** from a full year of e-commerce transactions
- **3 product categories** (Office Supplies, Furniture, Technology)
- **1,849 unique products**
- **42,047 unique customers**
- **3 customer segments** (Corporate, Consumer, Home Office)
- **4 US regions** covering **49 states** and **531 cities**
- **4 shipping types** with **4 delivery status classifications**

---

## 🎨 Visual Design Philosophy

### Clarity Over Complexity

Each chart is designed to answer a specific business question clearly and directly without unnecessary embellishment.

### Consistency

Uniform color schemes, fonts, and layouts make the dashboard intuitive and easy to navigate.

### Context

Charts include reference lines, benchmarks, and comparisons to provide context and meaning to the data.

### Interactivity

Hover details, filters, and drill-downs empower users to explore the data at their own pace.

### Accessibility

Color choices consider colorblind users, and text is sized for readability.

---

## 📈 Success Metrics

This dashboard enables tracking of:

- **Revenue growth** month-over-month and year-over-year
- **Profit margin** improvements and erosion
- **Delivery performance** against targets (e.g., 95% on-time)
- **Customer satisfaction** proxies (cancellations, late deliveries)
- **Product portfolio** health and balance
- **Geographic expansion** effectiveness
- **Operational efficiency** in fulfillment and logistics

---

## 🔄 Dashboard Updates

The dashboard is designed to work with:

- **Static CSV data** for historical analysis
- **Live data connections** for real-time monitoring
- **Scheduled refreshes** for daily/weekly updates

All charts and KPIs automatically recalculate when new data is loaded.

---

## 🎯 Strategic Value

This dashboard transforms raw e-commerce transaction data into actionable insights that drive:

✅ **Better decision-making** through data visibility
✅ **Improved profitability** by identifying margin opportunities
✅ **Enhanced customer satisfaction** via delivery improvements
✅ **Optimized product mix** based on performance data
✅ **Strategic resource allocation** to high-value markets
✅ **Proactive problem-solving** through trend identification

---

## 📚 Dashboard Navigation Guide

### Getting Started

1. Use the sidebar filters to focus on specific time periods, regions, or segments
2. Review the main KPIs at the top for overall performance
3. Navigate through tabs to explore different aspects of the business

### Deep Diving

1. Start with the Overview tab to understand big-picture trends
2. Use Sales Analysis to understand what's selling
3. Check Profitability to ensure healthy margins
4. Monitor Shipping to maintain customer satisfaction
5. Explore Customer/Geographic to find growth opportunities
6. Review Product Performance to optimize the portfolio
7. Analyze Time Series to understand patterns and forecast

### Making Decisions

Each tab is designed to support specific types of decisions:

- **Overview** → Executive dashboarding
- **Sales** → Product and inventory decisions
- **Profitability** → Pricing and discount strategy
- **Shipping** → Operational improvements
- **Customer/Geographic** → Market expansion and targeting
- **Product** → Portfolio management
- **Time Series** → Planning and forecasting

---

_Built with ❤️ for data-driven e-commerce decision making_
