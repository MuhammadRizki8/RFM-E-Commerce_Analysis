import streamlit as st
import pandas as pd
from eda import *
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency
import plotly.express as px
st.set_page_config(page_title="E-commerce Dashboard")

st.title("E-Commerce Dashboard \U0001F6D2")

df_ecommerce = pd.read_csv("df_ecommerce.csv")
df_rfm=pd.read_csv("df_rfm.csv")
df_ecommerce['order_purchase_timestamp'] = pd.to_datetime(df_ecommerce['order_purchase_timestamp'])

# Create DataFrames
yearly_orders_df = create_yearly_df(df_ecommerce)
monthly_orders_df = create_monthly_df(df_ecommerce)
weekly_orders_df = create_weekly_df(df_ecommerce)
daily_orders_df = create_daily_df(df_ecommerce)
order_perhari=calculate_daily_income_total(df_ecommerce)
category_counts = df_ecommerce.groupby(by="product_category_name").order_id.nunique().sort_values(ascending=False)
customer_counts = df_ecommerce.groupby('customer_Region')['customer_id'].nunique().sort_values(ascending=False)
seller_counts = df_ecommerce.groupby('seller_Region')['seller_id'].nunique().sort_values(ascending=False)
payment_percentage = df_ecommerce.groupby("payment_type").order_id.nunique().reset_index(name='total_order').sort_values(by='total_order', ascending=False)
segment_counts=df_rfm.Segment.value_counts(normalize=True)
segment_counts_nonnmlz=df_rfm.Segment.value_counts()

def eda():
    st.header('EDA', divider='rainbow')
    st.subheader('Tren Order')
    col1_left, col2_right = st.columns(2)
    with col1_left:
        total_orders = df_ecommerce.order_id.nunique()
        st.metric("Total Order", value=total_orders)

    with col2_right:
        total_sales = format_currency(df_ecommerce.payment_value.sum(), " R$", locale='es_CO') 
        st.metric("Total Transaksi", value=total_sales)
    
    tabs = st.tabs(['Harian','Mingguan', 'Bulanan', 'Tahunan'])
    with tabs[0]:
        col1_left, col2_right = st.columns(2)
        with col1_left:
            st.subheader('Jumlah Order')
            st.line_chart(
                daily_orders_df,
                x="tanggal",
                y="order_count", 
                color="#90CAF9"
            )
        with col2_right:
            st.subheader('Total Transaksi')
            st.line_chart(
                daily_orders_df,
                x="tanggal",
                y="total_transaction", 
                color="#A0D0D0"
            )
    with tabs[1]:
        col1_left, col2_right = st.columns(2)
        with col1_left:
            st.subheader('Jumlah Order')
            st.line_chart(
                weekly_orders_df,
                x="tanggal",
                y="order_count", 
                color="#90CAF9"
            )
        with col2_right:
            st.subheader('Total Transaksi')
            st.line_chart(
                weekly_orders_df,
                x="tanggal",
                y="total_transaction", 
                color="#A0D0D0"
            )
    with tabs[2]:
        col1_left, col2_right = st.columns(2)
        with col1_left:
            st.subheader('Jumlah Order')
            st.line_chart(
                monthly_orders_df,
                x="bulan",
                y="order_count", 
                color="#90CAF9"
            )
        with col2_right:
            st.subheader('Total Transaksi')
            st.line_chart(
                monthly_orders_df,
                x="bulan",
                y="total_transaction", 
                color="#A0D0D0"
            )
    with tabs[3]:
        col1_left, col2_right = st.columns(2)
        with col1_left:
            st.subheader('Jumlah Order')
            st.line_chart(
                yearly_orders_df,
                x="tahun",
                y="order_count", 
                color="#90CAF9"
            )
        with col2_right:
            st.subheader('Total Transaksi')
            st.line_chart(
                yearly_orders_df,
                x="tahun",
                y="total_transaction", 
                color="#A0D0D0"
            )
    st.markdown("Hasil Analisis:")
    st.markdown("- terdapat tren positif dalam pertumbuhan bisnis sepanjang periode yang diamati.")
    st.markdown("- Puncak penjualan pada bulan November 2017 menunjukkan bahwa perusahaan berhasil memanfaatkan momen tertentu untuk mencapai keuntungan maksimal.")
    st.markdown("- Pada tahun 2018 terjadi penurunan dalam jumlah pembelian dan total transaksi, menandakan adanya perubahan dinamika yang perlu diinvestigasi lebih lanjut")
    
    st.subheader('Frequensi Order Berdasarkan Hari')
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 3))
    sns.barplot(x='Hari', y='jumlah_order', data=order_perhari, palette=sns.color_palette("blend:#7AB,#EDA", n_colors=len(order_perhari)))
    plt.title('Order berdasarkan hari', fontsize=16)
    plt.xlabel('Hari', fontsize=14)
    plt.ylabel('Total Transaksi', fontsize=14)
    st.pyplot(plt)
    st.markdown("Hasil Analisis:")
    st.markdown("- Order memuncak pada hari Senin dan perlahan turun hingga ke hari Minggu")
    st.markdown("- customer cenderung melakukan pembelian pada waktu weekday dibandingkan pada saat weekends.")

    st.subheader('Kategori Produk')
    st.write("**Total Kategori yang Tersedia** :", category_counts.shape[0])
    top_5 = category_counts.head(5).sort_values(ascending=False)  # Urutkan secara terbalik
    bottom_5 = category_counts.tail(5).sort_values(ascending=False)  # Urutkan secara terbalik
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 10))
    colors_top5 = ["limegreen", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    colors_bottom5 = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "salmon"]
    sns.barplot(x=top_5.values, y=top_5.index, palette=colors_top5, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel('Jumlah ID Produk Unik')
    ax[0].set_title("Best Performing Product", loc="center", fontsize=18)
    ax[0].tick_params(axis ='y', labelsize=15)
    sns.barplot(x=bottom_5.values, y=bottom_5.index, palette=colors_bottom5[0::], ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel('Jumlah ID Produk Unik')
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Worst Performing Product", loc="center", fontsize=18)
    ax[1].tick_params(axis='y', labelsize=15)
    plt.suptitle("Best and Worst Performing Product by Number of Sales", fontsize=25)
    st.pyplot(plt)
    st.markdown("Hasil Analisis:")
    st.markdown("- kategori 'Bed Bath Table' menjadi kategori produk terbanyak")
    st.markdown("- kategori 'Security And Services' memiliki jumlah pesanan paling sedikit")

    st.subheader('Demografi Customer dan Seller')
    col1_left, col2_right = st.columns(2)
    with col1_left:
        total_customers = df_ecommerce.customer_id.nunique()
        st.metric("Total Customer", value=total_customers)

    with col2_right:
        total_sallers = df_ecommerce.seller_id.nunique()
        st.metric("Total Seller", value=total_sallers)
    # Palet warna unik untuk setiap region
    customer_palette = sns.color_palette("pastel", n_colors=len(customer_counts))
    seller_palette = sns.color_palette("pastel", n_colors=len(seller_counts))

    # Plotting dengan Seaborn
    plt.figure(figsize=(14, 6))

    # Plotting untuk pelanggan
    plt.subplot(1, 2, 1)
    sns.barplot(x=customer_counts.values, y=customer_counts.index, palette=customer_palette)
    plt.title('Pesebaran Customer berdasarkan Region')
    plt.xlabel('Jumlah Customer')

    # Plotting untuk penjual
    plt.subplot(1, 2, 2)
    sns.barplot(x=seller_counts.values, y=seller_counts.index, palette=seller_palette)
    plt.title('esebaran Seller berdasarkan Region')
    plt.xlabel('Jumlah Seller')
    plt.tight_layout()
    st.pyplot(plt)
    st.markdown("Hasil Analisis:")
    st.markdown("- wilayah Southeast menjadi fokus utama bisnis dengan jumlah pelanggan dan penjual yang signifikan")
    st.markdown("- Wilayah Northeast memiliki potensi pasar yang besar dengan jumlah pelanggan yang signifikan namun jumlah penjual yang masih perlu ditingkatkan")
    st.markdown("- North dan Centwest menunjukkan tingkat aktivitas yang lebih rendah, menciptakan kesenjangan regional yang mungkin perlu diperhatikan dalam strategi penetrasi pasar e-commerce")
    
    
    st.subheader('Pesebaran Metode Pembayaran dalam Order')
    # Normalisasi data
    total_orders = payment_percentage['total_order'].sum()
    payment_percentage['percentage'] = payment_percentage['total_order'] / total_orders * 100

    # Membuat diagram lingkaran dengan Plotly
    fig = px.pie(payment_percentage, values='percentage', names='payment_type', title='Pesebaran Metode Pembayaran dalam Order')

    # Menampilkan diagram lingkaran di Streamlit
    st.plotly_chart(fig)
    st.markdown("Hasil Analisis:")
    st.markdown("- Mayoritas pelanggan menggunakan kartu kredit (credit_card), diikuti oleh metode pembayaran boleto dan voucher. sekitar 3/4 customer lebih memilih menggunakan kartu kredit")

def rfm():
    st.header('RFM', divider='rainbow')
    st.subheader("Penjelasan Singkat RFM")
    rfm_explanation = """
    RFM analysis merupakan salah satu metode yang umum digunakan untuk melakukan segmentasi pelanggan (mengelompokkan pelanggan ke dalam beberapa kategori) berdasarkan tiga parameter, yaitu:

    - Recency: Parameter ini menunjukkan kapan terakhir seorang pelanggan melakukan transaksi.
    - Frequency: Parameter ini mengukur seberapa sering seorang pelanggan melakukan transaksi.
    - Monetary: Parameter ini mengukur seberapa besar revenue yang berasal dari pelanggan tersebut.
    """
    st.write(rfm_explanation)
    col1_left, col2_middle, col3_right = st.columns(3)
    with col1_left:
        avg_recency = round(df_rfm.recency.mean())
        st.metric("Rata-rata Recency (days)", value=avg_recency)
    with col2_middle:
        avg_frequency = round(df_rfm.frequency.mean())
        st.metric("Rata-rata Frequency", value=avg_frequency)
    with col3_right:
        avg_monetary = format_currency(df_rfm.monetary.mean(), " R$", locale='es_CO') 
        st.metric("Rata-rata Monetary", value=avg_monetary)
        
    # st.subheader("Distribusi 3 Parameter RFM")
    # tabs = st.tabs(['Recency','Frequency', 'Monetary'])
    # with tabs[0]:
    #     # Adjust the figure size
    #     plt.figure(figsize=(12, 5))
    #     #Recency
    #     # Create histplot
    #     sns.histplot(df_rfm['recency'], kde=True, stat="density")
    #     # Setting some visual options
    #     plt.title('Recency distribution')
    #     plt.xlabel(None)
    #     st.pyplot(plt)
    # with tabs[1]:
    #     #Frequency
    #     plt.figure(figsize=(12, 5))
    #     # Create histplot
    #     sns.histplot(df_rfm['frequency'], kde=True, stat="density")
    #     # Setting some visual options
    #     plt.title('Frequency distribution')
    #     plt.xlabel(None)
    #     st.pyplot(plt)
    # with tabs[2]:
    #     #Frequency
    #     plt.figure(figsize=(12, 5))
    #     # Create histplot
    #     sns.histplot(df_rfm['monetary'], kde=True, stat="density")
    #     # Setting some visual options
    #     plt.title('Monetary distribution')
    #     plt.xlabel(None)
    #     st.pyplot(plt)
    
    st.subheader('Segmentasi Pelanggan')
    fig = px.pie(segment_counts, values=segment_counts, names=segment_counts.index,
        title='Customer Segmentation')
    st.plotly_chart(fig)
    st.dataframe(segment_counts_nonnmlz, width=600)
    
    champions_description = """
    **Champions (High Value):**
    - RFM Score: 10-12
    - Deskripsi: Pelanggan dalam kelompok ini memiliki nilai tinggi dalam semua kategori RFM. 
    Mereka adalah pelanggan yang baru-baru ini melakukan pembelian (Recency tinggi), sering berbelanja (Frequency tinggi), dan mengeluarkan jumlah uang yang besar (Monetary tinggi).
    """

    loyal_customers_description = """
    **Loyal Customers:**
    - RFM Score: 8-9
    - Deskripsi: Pelanggan ini telah sering berbelanja dan memiliki nilai uang yang baik. 
    Mereka mungkin tidak sebaru Champions, tetapi masih menjadi pelanggan yang berharga.
    """

    potential_loyalists_description = """
    **Potential Loyalists:**
    - RFM Score: 6-7
    - Deskripsi: Grup ini mungkin memiliki nilai Monetari yang lebih rendah dibandingkan dengan Loyal Customers, 
    tetapi mereka sering berbelanja dan memiliki rekam jejak yang baik.
    """

    promising_customers_description = """
    **Promising Customers:**
    - RFM Score: 4-5
    - Deskripsi: Pelanggan dalam kelompok ini mungkin belum sering berbelanja atau mengeluarkan banyak uang, 
    tetapi mereka baru-baru ini melakukan pembelian. Mereka memiliki potensi untuk menjadi pelanggan yang lebih aktif.
    """

    needs_attention_description = """
    **Needs Attention:**
    - RFM Score: 3
    - Deskripsi: Pelanggan ini memiliki skor rendah dalam semua kategori dan memerlukan perhatian khusus. 
    Mungkin mereka adalah pelanggan lama yang tidak melakukan pembelian baru-baru ini.
    """

    # Menampilkan penjelasan di Streamlit
    st.markdown(champions_description, unsafe_allow_html=True)
    st.markdown(loyal_customers_description, unsafe_allow_html=True)
    st.markdown(potential_loyalists_description, unsafe_allow_html=True)
    st.markdown(promising_customers_description, unsafe_allow_html=True)
    st.markdown(needs_attention_description, unsafe_allow_html=True)
    
page_connector_with_funcs = {
    "EDA": eda,
    "RFM": rfm,
    # "EDA": eda
}

demo_name = st.sidebar.selectbox("Select a demo", page_connector_with_funcs.keys())
page_connector_with_funcs[demo_name]()

st.caption('Copyright (c) - Created by Rizki Muhammad - 2023')