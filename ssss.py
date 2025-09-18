# ... (previous code unchanged)

def dashboard_page():
    st.markdown('<div class="section-title">📊 Dashboard Overview</div>', unsafe_allow_html=True)
    
    # Check if data exists
    if 'transactions' not in st.session_state or st.session_state.transactions.empty:
        st.info("No data available to display. Please record some transactions.")
        return
        
    # Create copies to avoid modifying the original data
    transactions = st.session_state.transactions.copy()
    expenditures = st.session_state.expenditures.copy()
    
    # Ensure Date columns are properly formatted
    try:
        if 'Date' in transactions.columns:
            transactions['Date'] = pd.to_datetime(transactions['Date'], errors='coerce')
        if 'Date' in expenditures.columns:
            expenditures['Date'] = pd.to_datetime(expenditures['Date'], errors='coerce')
    except Exception as e:
        st.error(f"Error processing date columns: {e}")
        return
    
    # Use today's date for daily calculations
    today = datetime.now().date()
    
    # Calculate key metrics with proper error handling
    try:
        # Filter for today's transactions
        today_mask = transactions['Date'].dt.date == today
        type_mask = transactions['Type'] == 'Sale'
        
        today_sales = transactions[today_mask & type_mask]['Selling_Price'].sum()
        today_profit = transactions[today_mask]['Profit'].sum()
        
        # Filter for today's expenditures
        today_exp_mask = expenditures['Date'].dt.date == today
        today_expenditure = expenditures[today_exp_mask]['Amount'].sum()
        
        # Overall metrics
        total_sales = transactions['Selling_Price'].sum()
        total_profit = transactions['Profit'].sum()
        total_expenditure = expenditures['Amount'].sum()
        pending_payments = transactions['Left_Amount'].sum()
        
        # Category breakdown
        mobile_sales = transactions[transactions['Category'] == 'Mobile']['Selling_Price'].sum()
        accessories_sales = transactions[transactions['Category'] == 'Accessories']['Selling_Price'].sum()
        service_sales = transactions[transactions['Category'] == 'Repair']['Selling_Price'].sum()
        
    except Exception as e:
        st.error(f"Error calculating metrics: {e}")
        # Set default values
        today_sales = today_profit = today_expenditure = 0
        total_sales = total_profit = total_expenditure = pending_payments = 0
        mobile_sales = accessories_sales = service_sales = 0
    
    # Create metric cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Today's Sales</h3>
            <p style="font-size: 1.5rem; font-weight: bold; color: #a442f5;">{today_sales:,.0f} PKR</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        profit_style = "positive-profit" if today_profit >= 0 else "negative-profit"
        st.markdown(f"""
        <div class="metric-card">
            <h3>Today's Profit</h3>
            <p class="{profit_style}" style="font-size: 1.5rem; font-weight: bold;">{today_profit:,.0f} PKR</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Today's Expenditure</h3>
            <p style="font-size: 1.5rem; font-weight: bold; color: #a442f5;">{today_expenditure:,.0f} PKR</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("Overall Business Performance")
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Sales</h3>
            <p style="font-size: 1.5rem; font-weight: bold; color: #a442f5;">{total_sales:,.0f} PKR</p>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        profit_style = "positive-profit" if total_profit >= 0 else "negative-profit"
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Profit</h3>
            <p class="{profit_style}" style="font-size: 1.5rem; font-weight: bold;">{total_profit:,.0f} PKR</p>
        </div>
        """, unsafe_allow_html=True)
    with col6:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Expenditure</h3>
            <p style="font-size: 1.5rem; font-weight: bold; color: #a442f5;">{total_expenditure:,.0f} PKR</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Additional metrics
    st.subheader("Additional Metrics")
    col7, col8, col9 = st.columns(3)
    with col7:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Pending Payments</h3>
            <p style="font-size: 1.5rem; font-weight: bold; color: #FF9800;">{pending_payments:,.0f} PKR</p>
        </div>
        """, unsafe_allow_html=True)
    with col8:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Mobile Sales</h3>
            <p style="font-size: 1.5rem; font-weight: bold; color: #a442f5;">{mobile_sales:,.0f} PKR</p>
        </div>
        """, unsafe_allow_html=True)
    with col9:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Accessories Sales</h3>
            <p style="font-size: 1.5rem; font-weight: bold; color: #a442f5;">{accessories_sales:,.0f} PKR</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("Sales Distribution")
    if total_sales > 0:
        sales_data = pd.DataFrame({
            'Category': ['Mobiles', 'Accessories', 'Services'],
            'Amount': [mobile_sales, accessories_sales, service_sales]
        })
        st.bar_chart(sales_data.set_index('Category'))
    else:
        st.info("No sales data available for chart visualization.")
    
    st.subheader("Daily Profit & Loss Analysis")
    if not transactions.empty and 'Date' in transactions.columns and 'Profit' in transactions.columns:
        try:
            # Group by date and sum profits
            daily_profit = transactions.groupby(transactions['Date'].dt.date)['Profit'].sum()
            if not daily_profit.empty:
                st.line_chart(daily_profit)
            else:
                st.info("No daily profit data available for visualization.")
        except Exception as e:
            st.error(f"Error creating profit chart: {e}")
    else:
        st.info("No sales data available for daily analysis.")
    
    # Add download report button
    st.markdown("---")
    st.subheader("Download Reports")
    
    # Period selection for reports
    report_period = st.selectbox(
        "Select Report Period",
        ["Daily", "Weekly", "Monthly", "Yearly", "All Time"],
        key="report_period"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        try:
            if st.button(f"📄 Generate {report_period} PDF Report", key="generate_dashboard_pdf", use_container_width=True):
                report_data = create_dashboard_report(period=report_period.lower().replace(" ", "_"))
                st.download_button(
                    label=f"⬇️ Download {report_period} Report (PDF)",
                    data=report_data,
                    file_name=f"{report_period.lower().replace(' ', '_')}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="dashboard_pdf_download"
                )
        except Exception as e:
            st.error(f"Error generating PDF report: {e}")

    with col2:
        try:
            csv_data = transactions.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📊 Download All Data (CSV)",
                data=csv_data,
                file_name=f"business_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error generating CSV: {e}")
