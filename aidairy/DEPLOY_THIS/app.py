"""
SmartDairy - AI Powered Digital Dairy Management System
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import matplotlib.pyplot as plt
import os
from utils.db import (
    init_database, add_customer, get_all_customers, get_customer_by_id,
    update_customer, delete_customer, add_entry, get_entries
)
from utils.billing import (
    calculate_monthly_billing, generate_pdf_invoice,
    generate_excel_invoice, generate_csv_invoice,
    send_whatsapp_bill, get_whatsapp_link
)
from utils.forecasting import (
    predict_next_day_quantity, get_forecast_dataframe, get_forecast_summary
)

# Page configuration
st.set_page_config(
    page_title="SmartDairy - AI Powered Digital Dairy Management",
    page_icon="🐄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #2E86AB;
        color: white;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E86AB;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize database
if 'db_initialized' not in st.session_state:
    init_database()
    st.session_state.db_initialized = True

# Main header
st.markdown('<h1 class="main-header">🐄 SmartDairy</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI Powered Digital Dairy Management System</p>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["🏠 Dashboard", "👥 Customer Management", "🥛 Daily Milk Entry", "💰 Monthly Billing", "🤖 AI Forecasting"]
)

# Dashboard Page
if page == "🏠 Dashboard":
    st.header("📊 Dashboard")
    
    # Get statistics
    customers = get_all_customers()
    entries = get_entries()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Customers", len(customers))
    
    with col2:
        st.metric("Total Entries", len(entries))
    
    with col3:
        total_litres = sum(e['quantity'] for e in entries)
        st.metric("Total Litres", f"{total_litres:.2f} L")
    
    with col4:
        total_revenue = sum(e['quantity'] * e['price_per_ltr'] for e in entries)
        st.metric("Total Revenue", f"₹{total_revenue:.2f}")
    
    st.divider()
    
    # Recent entries table
    if entries:
        st.subheader("Recent Entries")
        recent_entries = entries[:10]  # Show last 10 entries
        df_recent = pd.DataFrame(recent_entries)
        df_recent = df_recent[['entry_date', 'customer_name', 'quantity', 'price_per_ltr']]
        df_recent.columns = ['Date', 'Customer', 'Quantity (L)', 'Rate (₹/L)']
        st.dataframe(df_recent, use_container_width=True, hide_index=True)
    else:
        st.info("No entries found. Start adding milk entries!")

# Customer Management Page
elif page == "👥 Customer Management":
    st.header("👥 Customer Management")
    
    tab1, tab2, tab3 = st.tabs(["➕ Add Customer", "📋 View Customers", "✏️ Update/Delete Customer"])
    
    with tab1:
        st.subheader("Add New Customer")
        with st.form("add_customer_form"):
            name = st.text_input("Customer Name *", placeholder="Enter customer name")
            price = st.number_input("Price per Litre (₹) *", min_value=0.0, value=50.0, step=0.5)
            mobile = st.text_input("Mobile Number (WhatsApp)", placeholder="e.g., 9876543210 or +919876543210")
            submit = st.form_submit_button("Add Customer", type="primary")
            
            if submit:
                if name.strip():
                    mobile_clean = mobile.strip() if mobile.strip() else None
                    if add_customer(name.strip(), price, mobile_clean):
                        st.success(f"✅ Customer '{name}' added successfully!")
                    else:
                        st.error("❌ Customer with this name already exists!")
                else:
                    st.warning("⚠️ Please enter a valid customer name")
    
    with tab2:
        st.subheader("All Customers")
        customers = get_all_customers()
        
        if customers:
            df = pd.DataFrame(customers)
            # Include mobile_number if available
            display_cols = ['id', 'name', 'price_per_ltr']
            if 'mobile_number' in df.columns:
                display_cols.append('mobile_number')
            df = df[display_cols]
            df.columns = ['ID', 'Customer Name', 'Price per Litre (₹)', 'Mobile Number'] if 'mobile_number' in display_cols else ['ID', 'Customer Name', 'Price per Litre (₹)']
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No customers found. Add your first customer!")
    
    with tab3:
        st.subheader("Update or Delete Customer")
        customers = get_all_customers()
        
        if customers:
            customer_options = {f"{c['name']} (₹{c['price_per_ltr']}/L)": c['id'] for c in customers}
            selected_customer = st.selectbox("Select Customer", list(customer_options.keys()))
            customer_id = customer_options[selected_customer]
            
            customer = get_customer_by_id(customer_id)
            
            with st.form("update_customer_form"):
                new_name = st.text_input("Customer Name", value=customer['name'])
                new_price = st.number_input("Price per Litre (₹)", min_value=0.0, value=float(customer['price_per_ltr']), step=0.5)
                current_mobile = customer.get('mobile_number', '') if customer.get('mobile_number') else ''
                new_mobile = st.text_input("Mobile Number (WhatsApp)", value=current_mobile, placeholder="e.g., 9876543210")
                
                col1, col2 = st.columns(2)
                with col1:
                    update_btn = st.form_submit_button("🔄 Update Customer", type="primary")
                with col2:
                    delete_btn = st.form_submit_button("🗑️ Delete Customer", use_container_width=True)
                
                if update_btn:
                    if new_name.strip():
                        mobile_clean = new_mobile.strip() if new_mobile.strip() else None
                        if update_customer(customer_id, new_name.strip(), new_price, mobile_clean):
                            st.success("✅ Customer updated successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Update failed. Customer name might already exist.")
                    else:
                        st.warning("⚠️ Please enter a valid customer name")
                
                if delete_btn:
                    if delete_customer(customer_id):
                        st.success("✅ Customer deleted successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete customer. Customer might have entries.")
        else:
            st.info("No customers available to update or delete.")

# Daily Milk Entry Page
elif page == "🥛 Daily Milk Entry":
    st.header("🥛 Daily Milk Entry")
    
    customers = get_all_customers()
    
    if not customers:
        st.warning("⚠️ Please add customers first before entering milk data!")
    else:
        with st.form("milk_entry_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                customer_options = {c['name']: c['id'] for c in customers}
                selected_customer_name = st.selectbox("Select Customer *", list(customer_options.keys()))
                customer_id = customer_options[selected_customer_name]
            
            with col2:
                quantity = st.number_input("Quantity (Litres) *", min_value=0.0, value=0.0, step=0.1)
            
            with col3:
                entry_date = st.date_input("Entry Date *", value=date.today())
            
            submit = st.form_submit_button("➕ Add Entry", type="primary")
            
            if submit:
                if quantity > 0:
                    if add_entry(customer_id, entry_date.strftime('%Y-%m-%d'), quantity):
                        st.success(f"✅ Entry added successfully for {selected_customer_name}!")
                    else:
                        st.error("❌ Failed to add entry. Entry might already exist for this date.")
                else:
                    st.warning("⚠️ Please enter a valid quantity")
        
        st.divider()
        
        # Filter and display entries
        st.subheader("📋 View Entries")
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date (Optional)", value=None)
        with col2:
            end_date = st.date_input("End Date (Optional)", value=None)
        
        # Get filtered entries
        start_str = start_date.strftime('%Y-%m-%d') if start_date else None
        end_str = end_date.strftime('%Y-%m-%d') if end_date else None
        
        entries = get_entries(start_str, end_str)
        
        if entries:
            df = pd.DataFrame(entries)
            df = df[['entry_date', 'customer_name', 'quantity', 'price_per_ltr']]
            df.columns = ['Date', 'Customer', 'Quantity (L)', 'Rate (₹/L)']
            df['Amount (₹)'] = df['Quantity (L)'] * df['Rate (₹/L)']
            df = df[['Date', 'Customer', 'Quantity (L)', 'Rate (₹/L)', 'Amount (₹)']]
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # CSV Export
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"milk_entries_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No entries found for the selected date range.")

# Monthly Billing Page
elif page == "💰 Monthly Billing":
    st.header("💰 Monthly Billing")
    
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("Select Year", range(2020, 2030), index=datetime.now().year - 2020)
    with col2:
        month = st.selectbox("Select Month", range(1, 13), index=datetime.now().month - 1)
    
    if st.button("📊 Calculate Billing", type="primary"):
        billing_data = calculate_monthly_billing(year, month)
        
        if billing_data['customers']:
            st.success(f"✅ Billing calculated for {datetime(year, month, 1).strftime('%B %Y')}")
            
            # Display summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Customers", billing_data['total_customers'])
            with col2:
                total_litres = sum(c['total_litres'] for c in billing_data['customers'])
                st.metric("Total Litres", f"{total_litres:.2f} L")
            with col3:
                st.metric("Grand Total", f"₹{billing_data['grand_total']:.2f}")
            
            st.divider()
            
            # Display billing table
            st.subheader("Billing Details")
            df_billing = pd.DataFrame(billing_data['customers'])
            df_billing = df_billing[['name', 'total_litres', 'price_per_ltr', 'total_amount']]
            df_billing.columns = ['Customer Name', 'Total Litres', 'Rate/Litre (₹)', 'Total Amount (₹)']
            st.dataframe(df_billing, use_container_width=True, hide_index=True)
            
            st.divider()
            
            # Export buttons
            st.subheader("📥 Export Invoice")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("📄 Generate PDF Invoice"):
                    pdf_path = generate_pdf_invoice(billing_data, "invoice.pdf")
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=pdf_file.read(),
                            file_name=f"invoice_{year}_{month:02d}.pdf",
                            mime="application/pdf"
                        )
            
            with col2:
                if st.button("📊 Generate Excel Invoice"):
                    excel_path = generate_excel_invoice(billing_data, "invoice.xlsx")
                    with open(excel_path, "rb") as excel_file:
                        st.download_button(
                            label="⬇️ Download Excel",
                            data=excel_file.read(),
                            file_name=f"invoice_{year}_{month:02d}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
            
            with col3:
                if st.button("📋 Generate CSV Invoice"):
                    csv_path = generate_csv_invoice(billing_data, "invoice.csv")
                    with open(csv_path, "rb") as csv_file:
                        st.download_button(
                            label="⬇️ Download CSV",
                            data=csv_file.read(),
                            file_name=f"invoice_{year}_{month:02d}.csv",
                            mime="text/csv"
                        )
            
            st.divider()
            
            # WhatsApp sending section
            st.subheader("📱 Send Bills via WhatsApp")
            st.info("💡 Select a customer below to send their bill via WhatsApp. Make sure WhatsApp Web is open in your browser.")
            
            # Customer selection for WhatsApp
            customer_list = billing_data['customers']
            if customer_list:
                customer_names = [f"{c['name']} - ₹{c['total_amount']:.2f}" for c in customer_list]
                selected_customer_idx = st.selectbox(
                    "Select Customer to Send Bill",
                    range(len(customer_names)),
                    format_func=lambda x: customer_names[x]
                )
                
                selected_customer = customer_list[selected_customer_idx]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📱 Send via WhatsApp (Auto)", type="primary", use_container_width=True):
                        if selected_customer.get('mobile_number'):
                            success, message = send_whatsapp_bill(selected_customer, billing_data)
                            if success:
                                st.success(f"✅ {message}")
                                st.info("⚠️ Please keep your browser open. WhatsApp Web will open automatically in 1 minute.")
                            else:
                                st.error(f"❌ {message}")
                        else:
                            st.warning("⚠️ Mobile number not found for this customer. Please update customer details.")
                
                with col2:
                    whatsapp_link = get_whatsapp_link(selected_customer, billing_data)
                    if whatsapp_link:
                        st.markdown(f'<a href="{whatsapp_link}" target="_blank"><button style="background-color: #25D366; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; width: 100%;">📱 Open WhatsApp Link</button></a>', unsafe_allow_html=True)
                    else:
                        st.warning("Mobile number not available")
                
                # Show customer mobile number
                if selected_customer.get('mobile_number'):
                    st.caption(f"📞 Mobile: {selected_customer['mobile_number']}")
                else:
                    st.caption("⚠️ No mobile number registered for this customer")
        else:
            st.warning(f"⚠️ No entries found for {datetime(year, month, 1).strftime('%B %Y')}")

# AI Forecasting Page
elif page == "🤖 AI Forecasting":
    st.header("🤖 AI Forecasting - Milk Quantity Prediction")
    
    customers = get_all_customers()
    
    if not customers:
        st.warning("⚠️ Please add customers and entries first!")
    else:
        customer_options = {c['name']: c['id'] for c in customers}
        selected_customer_name = st.selectbox("Select Customer", list(customer_options.keys()))
        customer_id = customer_options[selected_customer_name]
        
        window_size = st.slider("Moving Average Window (Days)", min_value=3, max_value=30, value=7, step=1)
        
        if st.button("🔮 Predict Next Day Quantity", type="primary"):
            predicted, historical = predict_next_day_quantity(customer_id, window_size)
            
            if historical:
                forecast_summary = get_forecast_summary(customer_id, window_size)
                
                # Display metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Predicted Quantity", f"{forecast_summary['predicted_quantity']:.2f} L")
                with col2:
                    st.metric("Historical Average", f"{forecast_summary['historical_avg']:.2f} L")
                with col3:
                    st.metric("Minimum", f"{forecast_summary['historical_min']:.2f} L")
                with col4:
                    st.metric("Maximum", f"{forecast_summary['historical_max']:.2f} L")
                
                st.divider()
                
                # Get forecast dataframe
                df_forecast = get_forecast_dataframe(customer_id, window_size)
                
                # Plot forecast
                st.subheader("📈 Forecast Visualization")
                fig, ax = plt.subplots(figsize=(12, 6))
                
                # Plot historical data
                historical_df = df_forecast[:-1] if len(df_forecast) > 1 else df_forecast
                ax.plot(historical_df['Date'], historical_df['Quantity'], 
                       marker='o', label='Historical Data', linewidth=2, markersize=6)
                
                # Plot predicted value
                if len(df_forecast) > 1:
                    predicted_df = df_forecast.tail(1)
                    ax.plot(predicted_df['Date'], predicted_df['Quantity'], 
                           marker='*', label='Predicted', color='red', 
                           markersize=15, linewidth=2)
                
                ax.set_xlabel('Date', fontsize=12)
                ax.set_ylabel('Quantity (Litres)', fontsize=12)
                ax.set_title(f'Milk Quantity Forecast for {selected_customer_name}', fontsize=14, fontweight='bold')
                ax.legend()
                ax.grid(True, alpha=0.3)
                plt.xticks(rotation=45)
                plt.tight_layout()
                
                st.pyplot(fig)
                
                # Display data table
                st.subheader("📊 Forecast Data")
                df_display = df_forecast.copy()
                df_display['Date'] = df_display['Date'].dt.strftime('%Y-%m-%d')
                df_display.columns = ['Date', 'Quantity (L)']
                df_display['Type'] = ['Historical' if i < len(df_display) - 1 else 'Predicted' 
                                     for i in range(len(df_display))]
                st.dataframe(df_display, use_container_width=True, hide_index=True)
                
                st.info(f"💡 Prediction based on {window_size}-day moving average of {forecast_summary['data_points']} data points.")
            else:
                st.warning(f"⚠️ No historical data found for {selected_customer_name}. Please add some entries first.")

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: #666; padding: 20px;'>"
    "🐄 SmartDairy - AI Powered Digital Dairy Management System | "
    "Built with ❤️ using Streamlit"
    "</div>",
    unsafe_allow_html=True
)

