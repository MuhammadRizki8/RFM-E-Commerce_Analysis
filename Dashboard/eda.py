import pandas as pd
import matplotlib.pyplot as plt

def create_monthly_df(df_ecommerce):
    monthly_orders_df = df_ecommerce.resample(rule='M', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })
    monthly_orders_df.index = monthly_orders_df.index.strftime('%Y-%B')  # Format: Year-Month
    monthly_orders_df = monthly_orders_df.reset_index()
    monthly_orders_df.rename(columns={
        "order_purchase_timestamp":"bulan",
        "order_id": "order_count",
        "payment_value": "total_transaction"
    }, inplace=True)
    return monthly_orders_df

def create_yearly_df(df_ecommerce):
    yearly_orders_df = df_ecommerce.resample(rule='Y', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })
    yearly_orders_df.index = yearly_orders_df.index.strftime('%Y')  # Format: Year
    yearly_orders_df = yearly_orders_df.reset_index()
    yearly_orders_df.rename(columns={
        "order_purchase_timestamp":"tahun",
        "order_id": "order_count",
        "payment_value": "total_transaction"
    }, inplace=True)
    return yearly_orders_df

def create_daily_df(df_ecommerce):
    daily_orders_df = df_ecommerce.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })
    daily_orders_df.index = daily_orders_df.index.strftime('%Y-%m-%d')  # Format: Year-Month-Day
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_purchase_timestamp":"tanggal",
        "order_id": "order_count",
        "payment_value": "total_transaction"
    }, inplace=True)
    return daily_orders_df

def create_weekly_df(df_ecommerce):
    weekly_orders_df = df_ecommerce.resample(rule='W', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })
    weekly_orders_df.index = weekly_orders_df.index.strftime('%Y-%U')  # Format: Year-Week
    weekly_orders_df = weekly_orders_df.reset_index()
    weekly_orders_df.rename(columns={
        "order_purchase_timestamp":"tanggal",
        "order_id": "order_count",
        "payment_value": "total_transaction"
    }, inplace=True)
    return weekly_orders_df

def calculate_daily_income_total(df):
    # Pastikan 'order_purchase_timestamp' merupakan objek datetime
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    
    # Hitung total pendapatan harian
    result_df = df.groupby(df['order_purchase_timestamp'].dt.strftime('%A'))['order_id'].nunique().reset_index(name='jumlah_order')
    
    # Ubah nama kolom dan urutkan hasil
    result_df = result_df.rename(columns={"order_purchase_timestamp": "Hari"})
    result_df = result_df.sort_values(by='jumlah_order', ascending=False)
    
    return result_df