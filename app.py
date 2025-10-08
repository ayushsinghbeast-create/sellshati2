import streamlit as st
import pandas as pd
import datetime
import random

# --- 1. CONFIGURATION AND INITIALIZATION ---

# Set up page config (Blue and White theme preference)
st.set_page_config(
    page_title="SellSathi - Business Manager",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for aesthetic, square metric boxes with rounded corners (Blue & White theme)
st.markdown("""
<style>
    /* Main app colors */
    :root {
        --primary-color: #1E90FF; /* Dodger Blue */
        --secondary-color: #f0f2f6; /* Light gray for background/cards */
        --text-color: #333333;
    }
    
    /* Overall styling */
    .stApp {
        background-color: white;
        color: var(--text-color);
    }
    
    /* Header/Title styling */
    .css-1dp5ss0 { /* Targets the main title area */
        color: var(--primary-color);
    }

    /* Metric Box Styling (The key aesthetic requirement) */
    .metric-box {
        background-color: var(--secondary-color);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 10px 0;
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: var(--text-color);
    }
    .metric-box h3 {
        margin: 0;
        font-size: 1.2em;
        color: #555;
    }
    .metric-box p {
        margin: 5px 0 0 0;
        font-size: 2em;
        font-weight: bold;
        color: var(--primary-color);
    }
    
    /* Colored highlights for metrics */
    .color-1 { border-left: 5px solid #1E90FF; } /* Blue - Sales */
    .color-2 { border-left: 5px solid #3CB371; } /* Medium Sea Green - Profit */
    .color-3 { border-left: 5px solid #FF6347; } /* Tomato - Expenditure */
    
    /* Sidebar navigation styling */
    .css-1d3w5ao, .css-1y4p8pa { /* Targets sidebar elements */
        color: var(--primary-color);
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state for app data and navigation
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'Dashboard'
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = pd.DataFrame(columns=['Product Name', 'Buy Price', 'Sell Price', 'Quantity', 'Sales Count'])
if 'sales_data' not in st.session_state:
    st.session_state.sales_data = pd.DataFrame(columns=['Date', 'Product Name', 'Quantity Sold', 'Sale Price', 'Buy Price', 'Profit'])
if 'bill_history' not in st.session_state:
    st.session_state.bill_history = []
if 'bill_items' not in st.session_state:
    st.session_state.bill_items = []


# --- 2. CORE FUNCTIONS (DATA MANIPULATION) ---

def calculate_metrics(df_sales):
    """Calculates sales and profit metrics for today and the current month."""
    today = datetime.date.today()
    
    # Filter for today's sales
    today_sales = df_sales[df_sales['Date'] == str(today)]
    
    # Filter for monthly sales
    current_month = today.strftime('%Y-%m')
    monthly_sales = df_sales[df_sales['Date'].str.startswith(current_month)]

    metrics = {
        'Today Sales': today_sales['Sale Price'].sum(),
        'Today Profit': today_sales['Profit'].sum(),
        'Today Expenditure': today_sales['Buy Price'].sum(), 
        'Monthly Sales': monthly_sales['Sale Price'].sum(),
        'Monthly Profit': monthly_sales['Profit'].sum(),
        'Monthly Expenditure': monthly_sales['Buy Price'].sum(),
    }
    return metrics

def register_user(name, email, business_name, business_type):
    """Saves user data and sets logged_in state."""
    st.session_state.user_data = {
        'name': name,
        'email': email,
        'business_name': business_name,
        'business_type': business_type
    }
    st.session_state.logged_in = True
    st.session_state.page = 'Dashboard'
    st.success("Registration successful! Redirecting to Dashboard.")
    st.experimental_rerun()


# --- 3. PAGE FUNCTIONS ---

def RegistrationPage():
    """Renders the initial registration form."""
    st.title("SellSathi")
    st.header("Register Your Business")

    with st.form("registration_form"):
        st.subheader("Basic Details")
        
        name = st.text_input("1. Your Full Name", placeholder="e.g., Rohan Sharma")
        email = st.text_input("2. Email Address", placeholder="e.g., business@example.com")
        business_name = st.text_input("3. Business Name (Displayed in App)", placeholder="e.g., Sharma General Store")
        
        business_type = st.selectbox(
            "4. Business Type",
            ["Retail Store", "Online E-commerce", "Service Provider", "Manufacturing", "Other"]
        )

        # Confirm submit button is correctly inside the form
        confirm_register = st.form_submit_button("Confirm Register")
        
        if confirm_register:
            if name and email and business_name and business_type:
                register_user(name, email, business_name, business_type)
            else:
                st.error("Please fill in all required fields.")

def DashboardPage():
    """Renders the main dashboard with metrics and Add Sales feature."""
    user = st.session_state.user_data
    st.header(f"Welcome, {user.get('business_name', 'Your Business')}!")
    st.subheader("Performance Overview")

    metrics = calculate_metrics(st.session_state.sales_data)
    
    # Row 1 for Today's Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""<div class="metric-box color-1"><h3>Today Sales</h3><p>₹{metrics['Today Sales']:.2f}</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-box color-2"><h3>Today Profit</h3><p>₹{metrics['Today Profit']:.2f}</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="metric-box color-3"><h3>Today Expenditure</h3><p>₹{metrics['Today Expenditure']:.2f}</p></div>""", unsafe_allow_html=True)

    # Row 2 for Monthly Metrics
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown(f"""<div class="metric-box color-1"><h3>Monthly Sales</h3><p>₹{metrics['Monthly Sales']:.2f}</p></div>""", unsafe_allow_html=True)
    with col5:
        st.markdown(f"""<div class="metric-box color-2"><h3>Monthly Profit</h3><p>₹{metrics['Monthly Profit']:.2f}</p></div>""", unsafe_allow_html=True)
    with col6:
        st.markdown(f"""<div class="metric-box color-3"><h3>Monthly Expenditure</h3><p>₹{metrics['Monthly Expenditure']:.2f}</p></div>""", unsafe_allow_html=True)

    st.markdown("---")
    
    # Add Sales Feature (using a popover for small form)
    st.subheader("Record New Sale")
    
    stock_names = st.session_state.stock_data['Product Name'].tolist()
    
    if not stock_names:
        st.warning("Please add some products to your Stock first to record a sale.")
        return

    # Use st.expander as a compact form
    with st.expander("➕ Add Sales"):
        with st.form("add_sales_form", clear_on_submit=True):
            # 1. Search/Select Product
            selected_product_name = st.selectbox(
                "Search Product (Select from Stock)",
                options=[''] + stock_names,
                key="sale_product_select_input"
            )
            
            if selected_product_name:
                product_row = st.session_state.stock_data[st.session_state.stock_data['Product Name'] == selected_product_name].iloc[0]
                
                # Pre-fill/Edit Prices
                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    buy_price = st.number_input(f"Buy Price (from stock: ₹{product_row['Buy Price']:.2f})", 
                                                value=product_row['Buy Price'], min_value=0.01, key="sale_buy_price")
                with col_p2:
                    sale_price = st.number_input(f"Selling Price (from stock: ₹{product_row['Sell Price']:.2f})", 
                                                 value=product_row['Sell Price'], min_value=0.01, key="sale_sell_price")
                
                # Quantity and Stock Check
                quantity_available = product_row['Quantity']
                st.info(f"Quantity in Stock: {quantity_available}")
                quantity_sold = st.number_input("Quantity Sold", min_value=1, max_value=int(quantity_available), value=1, step=1, key="sale_qty")
                
                # CONFIRM SUBMIT BUTTON IS HERE
                confirm_sale = st.form_submit_button("Confirm Sale")
                
                if confirm_sale:
                    if quantity_sold > quantity_available:
                        st.error("Error: Quantity sold exceeds stock availability!")
                    else:
                        # Calculation logic
                        profit = (sale_price - buy_price) * quantity_sold
                        
                        # 1. Update Sales Data
                        new_sale = {
                            'Date': str(datetime.date.today()),
                            'Product Name': selected_product_name,
                            'Quantity Sold': quantity_sold,
                            'Sale Price': sale_price * quantity_sold,
                            'Buy Price': buy_price * quantity_sold,
                            'Profit': profit
                        }
                        st.session_state.sales_data = pd.concat([st.session_state.sales_data, pd.DataFrame([new_sale])], ignore_index=True)

                        # 2. Update Stock Data
                        stock_index = st.session_state.stock_data[st.session_state.stock_data['Product Name'] == selected_product_name].index[0]
                        st.session_state.stock_data.loc[stock_index, 'Quantity'] -= quantity_sold
                        st.session_state.stock_data.loc[stock_index, 'Sales Count'] = st.session_state.stock_data.loc[stock_index, 'Sales Count'] + quantity_sold
                        
                        st.success(f"Sale confirmed! {quantity_sold} x {selected_product_name} sold. Profit: ₹{profit:.2f}")
                        st.experimental_rerun() 
            else:
                st.warning("Please select a product.")

def StockPage():
    """Renders the stock management and product addition page."""
    user = st.session_state.user_data
    st.header(f"{user.get('business_name', 'Your Business')} - Stock Management")

    st.subheader("➕ Add New Stock / Product")
    with st.expander("Add Product Form"):
        with st.form("add_stock_form", clear_on_submit=True):
            product_name = st.text_input("Product Name", placeholder="e.g., T-Shirt Blue M")
            
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                buy_price = st.number_input("Buy Price (per unit)", min_value=0.01, format="%.2f", key="stock_buy_price")
            with col_s2:
                sell_price = st.number_input("Sell Price (per unit)", min_value=0.01, format="%.2f", key="stock_sell_price")
            with col_s3:
                quantity = st.number_input("Stock Quantity", min_value=1, step=1, key="stock_quantity")
                st.form_submit_button()
            if confirm_add:
                if product_name and buy_price > 0 and sell_price > 0 and quantity > 0:
                    new_product = {
                        'Product Name': product_name,
                        'Buy Price': buy_price,
                        'Sell Price': sell_price,
                        'Quantity': quantity,
                        'Sales Count': 0 
                    }
                    # Check if product already exists
                    if product_name in st.session_state.stock_data['Product Name'].tolist():
                        st.error(f"Product '{product_name}' already exists. Please update quantity or rename.")
                    else:
                        st.session_state.stock_data = pd.concat([st.session_state.stock_data, pd.DataFrame([new_product])], ignore_index=True)
                        st.success(f"Product '{product_name}' added to stock!")
                        st.experimental_rerun() 
                else:
                    st.error("Please ensure all fields are filled correctly (prices and quantity must be positive).")


    st.markdown("---")
    st.subheader("Current Stock Inventory")

    if st.session_state.stock_data.empty:
        st.info("Your stock is empty. Please add products using the form above.")
        return

    # Filter
    search_term = st.text_input("Filter Stock by Product Name", placeholder="Search for product...")
    
    df_display = st.session_state.stock_data.copy()
    
    if search_term:
        df_display = df_display[df_display['Product Name'].str.contains(search_term, case=False, na=False)]

    # Display table
    st.dataframe(df_display[['Product Name', 'Buy Price', 'Sell Price', 'Quantity']].rename(columns={
        'Product Name': 'Product Name',
        'Buy Price': 'Buy Price (₹)',
        'Sell Price': 'Sell Price (₹)',
        'Quantity': 'Available Stock'
    }), use_container_width=True, hide_index=True)
    
    st.caption("Note: Changes made in the stock are temporary in this demo (uses session state).")


def BillPage():
    """Renders the invoice generation and history page."""
    st.header("Billing & Invoice Generator")
    user = st.session_state.user_data
    business_name = user.get('business_name', 'SellSathi Business')
    
    st.subheader("Generate New Bill")
    
    stock_names = st.session_state.stock_data['Product Name'].tolist()
    
    if not stock_names:
        st.warning("Please add some products to your Stock first to create a bill.")
        return

    # Removed the unnecessary st.form block around customer details to prevent 'missing submit button' warning
    st.text_input("Business Name (Auto-filled)", value=business_name, disabled=True)
    customer_name = st.text_input("Customer Name", placeholder="e.g., Aman Kumar", key="bill_customer_name")
    selling_date = st.date_input("Selling Date", value=datetime.date.today(), key="bill_selling_date")

    st.markdown("### Product Items")
    
    # Item Addition Logic (Uses regular button)
    col_i1, col_i2, col_i3, col_i4 = st.columns([4, 2, 1, 1])
    
    new_product = col_i1.selectbox("Select Product", options=['-- Add Product --'] + stock_names, key="new_product_select")
    new_qty = col_i2.number_input("Quantity", min_value=1, value=1, key="new_qty_input")
    
    # Get prices for selected product
    item_price = 0.0
    if new_product in stock_names:
        product_row = st.session_state.stock_data[st.session_state.stock_data['Product Name'] == new_product].iloc[0]
        item_price = product_row['Sell Price']
        col_i3.metric(label="Unit Price (₹)", value=f"₹{item_price:.2f}")

    if col_i4.button("Add Item", key="add_item_btn"):
        if new_product != '-- Add Product --':
            # Check for quantity against stock
            quantity_available = st.session_state.stock_data[st.session_state.stock_data['Product Name'] == new_product]['Quantity'].iloc[0]
            
            qty_already_added = sum(item['qty'] for item in st.session_state.bill_items if item['name'] == new_product)
            
            if new_qty + qty_already_added > quantity_available:
                st.error(f"Cannot add: Adding {new_qty} units exceeds stock availability ({quantity_available} total available).")
            else:
                st.session_state.bill_items.append({
                    'name': new_product,
                    'qty': new_qty,
                    'price': item_price,
                    'total': new_qty * item_price
                })
                # Re-run is used to clear the selectbox/qty for a smoother flow.
                st.experimental_rerun()
        else:
            st.warning("Please select a valid product to add.")

    
    # Display current bill items
    if st.session_state.bill_items:
        bill_df = pd.DataFrame(st.session_state.bill_items)
        bill_df = bill_df.rename(columns={'name': 'Product', 'qty': 'Qty', 'price': 'Unit Price (₹)', 'total': 'Total (₹)'})
        st.dataframe(bill_df, use_container_width=True, hide_index=True)
        
        grand_total = bill_df['Total (₹)'].sum()
        st.success(f"**Grand Total:** ₹{grand_total:.2f}")

        # Form 2: Final Bill Submission (with submit button)
        with st.form("final_bill_submission_form"):
            st.write("Click below to finalize, save, and generate the bill.")
            
            # CONFIRM SUBMIT BUTTON IS HERE
            generate_bill_submit = st.form_submit_button("Generate & Save Bill")
            
            if generate_bill_submit:
                if not customer_name:
                    # Use st.form_submit_button's return value to check if submitted
                    st.error("Please ensure the customer's name is entered.")
                else:
                    # 1. Prepare Bill Content (Simulate PDF/Text Output)
                    bill_content = f"""
## SellSathi Invoice - {business_name}

**Invoice Date:** {selling_date}
**Customer Name:** {customer_name}
**Business Type:** {user.get('business_type')}

---

| Product | Quantity | Unit Price (₹) | Total (₹) |
| :--- | :---: | :---: | :---: |
"""
                    for item in st.session_state.bill_items:
                        bill_content += f"| {item['name']} | {item['qty']} | {item['price']:.2f} | {item['total']:.2f} |\n"
                    
                    bill_content += f"\n---"
                    bill_content += f"\n**GRAND TOTAL: ₹{grand_total:.2f}**"
                    bill_content += "\n\n*Thank you for your business!*"

                    st.markdown(bill_content)
                    
                    # 2. Save to History and Update Stock (Assuming the sale is finalized here)
                    bill_record = {
                        'bill_id': random.randint(1000, 9999),
                        'date': str(selling_date),
                        'customer': customer_name,
                        'total': grand_total,
                        'items': st.session_state.bill_items 
                    }
                    st.session_state.bill_history.append(bill_record)
                    
                    # Update stock based on bill items
                    for item in st.session_state.bill_items:
                        product_name = item['name']
                        quantity_sold = item['qty']
                        
                        stock_index = st.session_state.stock_data[st.session_state.stock_data['Product Name'] == product_name].index[0]
                        st.session_state.stock_data.loc[stock_index, 'Quantity'] -= quantity_sold
                        st.session_state.stock_data.loc[stock_index, 'Sales Count'] = st.session_state.stock_data.loc[stock_index, 'Sales Count'] + quantity_sold


                    # 3. Provide Download Button
                    st.download_button(
                        label="Download Invoice (Text/PDF Mock)",
                        data=bill_content,
                        file_name=f"invoice_{selling_date}_{bill_record['bill_id']}.txt",
                        mime="text/plain"
                    )

                    # 4. Clear temporary bill items
                    st.session_state.bill_items = []
                    st.success("Bill saved to history and stock updated.")
                    st.experimental_rerun() 

    else:
        st.info("No items added to the current bill. Please add products above.")
        
    st.markdown("---")
    st.subheader("Bill History")
    if st.session_state.bill_history:
        history_df = pd.DataFrame([{'Bill ID': h['bill_id'], 'Date': h['date'], 'Customer': h['customer'], 'Total (₹)': h['total']} for h in st.session_state.bill_history])
        st.dataframe(history_df, use_container_width=True, hide_index=True)
    else:
        st.info("No bills saved yet.")


def AnalysisPage():
    """Renders business analysis and insights."""
    st.header("Business Analysis")
    
    if st.session_state.sales_data.empty:
        st.info("No sales data available yet. Please record some sales to see the analysis.")
        return

    # Calculate total sales by product
    product_sales = st.session_state.sales_data.groupby('Product Name')['Quantity Sold'].sum().reset_index()
    product_sales = product_sales.sort_values(by='Quantity Sold', ascending=False)
    
    st.subheader("Top Performing Products (by Quantity Sold)")
    
    col_l1, col_l2 = st.columns(2)
    
    with col_l1:
        st.markdown("#### Most Selling Products (Top 3)")
        top_sellers = product_sales.head(3)
        if not top_sellers.empty:
            for index, row in top_sellers.iterrows():
                st.success(f"🥇 **{row['Product Name']}** - {row['Quantity Sold']} units sold")
        else:
            st.info("Not enough data to determine top sellers.")

    with col_l2:
        st.markdown("#### Least Selling Products (Bottom 3)")
        least_sellers = product_sales.tail(3).sort_values(by='Quantity Sold', ascending=True)
        if not least_sellers.empty:
            for index, row in least_sellers.iterrows():
                st.warning(f"📉 **{row['Product Name']}** - {row['Quantity Sold']} units sold")
        else:
            st.info("Not enough data to determine least sellers.")
            
    st.markdown("---")
    st.subheader("Sales Trend Chart")
    
    # Group sales data by date
    daily_sales = st.session_state.sales_data.groupby('Date')['Sale Price'].sum().reset_index()
    daily_sales['Date'] = pd.to_datetime(daily_sales['Date'])
    daily_sales = daily_sales.set_index('Date')
    
    st.line_chart(daily_sales)
    st.caption("Daily Sales Revenue Over Time.")

    st.markdown("---")
    st.subheader("Profit Distribution (Top 10 Products)")
    
    profit_by_product = st.session_state.sales_data.groupby('Product Name')['Profit'].sum().nlargest(10).reset_index()
    st.bar_chart(profit_by_product, x='Product Name', y='Profit')
    st.caption("Total Profit generated by the top 10 products.")


def AboutPage():
    """Renders the About SellSathi page."""
    st.header("About SellSathi")
    
    st.markdown("""
    **SellSathi** is your friendly companion for managing small to medium business operations. 
    It aims to simplify the daily tasks of sales tracking, inventory management, and business analysis, 
    allowing you to focus on growing your business.
    
    ### Key Features:
    * **Dashboard:** Quick overview of daily and monthly performance metrics.
    * **Stock:** Easy addition and tracking of your product inventory.
    * **Bill:** Simple invoice generation and history saving.
    * **Business Analysis:** Insightful reports on product performance and sales trends.
    
    ### For the Customer:
    SellSathi is designed to be intuitive and fast, reducing the time spent on manual record-keeping. 
    We believe that every small business deserves powerful tools without complexity.
    """)


# --- 4. MAIN APPLICATION FLOW ---

def main_app():
    """Renders the main application structure (sidebar and page content)."""
    with st.sidebar:
        st.title("SellSathi")
        st.subheader(st.session_state.user_data.get('business_name', 'Menu'))
        
        # Sidebar navigation buttons
        st.session_state.page = st.radio(
            "Navigation",
            ('Dashboard', 'Stock', 'Bill', 'Business Analysis', 'About')
        )
        
        # Simple Logout (Resets session state)
        if st.button("Logout"):
            st.session_state.logged_in = False
            # Reset all session state variables upon logout
            keys_to_reset = ['user_data', 'stock_data', 'sales_data', 'bill_history', 'bill_items']
            for key in keys_to_reset:
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_rerun()
            

    # Render selected page
    if st.session_state.page == 'Dashboard':
        DashboardPage()
    elif st.session_state.page == 'Stock':
        StockPage()
    elif st.session_state.page == 'Bill':
        BillPage()
    elif st.session_state.page == 'Business Analysis':
        AnalysisPage()
    elif st.session_state.page == 'About':
        AboutPage()

# Check login status and display appropriate view
if st.session_state.logged_in:
    main_app()
else:
    RegistrationPage()
