import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Set page config
st.set_page_config(
    page_title="Pickyfy - AI Product Recommender",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .product-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

class ProductRecommender:
    def __init__(self):
        self.products_df = None
        self.users_df = None
        self.transactions_df = None
        self.user_item_matrix = None
        self.tfidf_matrix = None
        self.product_features = None
        
    def load_sample_data(self):
        """Load sample data for demonstration"""
        # Sample products data
        categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports', 'Beauty']
        brands = ['Samsung', 'Apple', 'Nike', 'Adidas', 'Zara', 'H&M', 'Canon', 'Sony']
        
        products_data = []
        for i in range(100):
            product = {
                'product_id': f'P{i+1:03d}',
                'name': f'Product {i+1}',
                'category': random.choice(categories),
                'brand': random.choice(brands),
                'price': round(random.uniform(10, 1000), 2),
                'rating': round(random.uniform(3.0, 5.0), 1),
                'description': f'High quality {random.choice(categories).lower()} product with excellent features'
            }
            products_data.append(product)
        
        self.products_df = pd.DataFrame(products_data)
        
        # Sample users data
        users_data = []
        for i in range(50):
            user = {
                'user_id': f'U{i+1:03d}',
                'age': random.randint(18, 65),
                'gender': random.choice(['M', 'F']),
                'location': random.choice(['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Semarang'])
            }
            users_data.append(user)
        
        self.users_df = pd.DataFrame(users_data)
        
        # Sample transactions data
        transactions_data = []
        for i in range(500):
            transaction = {
                'transaction_id': f'T{i+1:04d}',
                'user_id': random.choice(self.users_df['user_id'].tolist()),
                'product_id': random.choice(self.products_df['product_id'].tolist()),
                'rating': random.randint(1, 5),
                'timestamp': datetime.now() - timedelta(days=random.randint(1, 365)),
                'quantity': random.randint(1, 3)
            }
            transactions_data.append(transaction)
        
        self.transactions_df = pd.DataFrame(transactions_data)
        
    def prepare_data(self):
        """Prepare data for recommendation algorithms"""
        # Create user-item matrix
        self.user_item_matrix = self.transactions_df.pivot_table(
            index='user_id', 
            columns='product_id', 
            values='rating', 
            fill_value=0
        )
        
        # Create product features for content-based filtering
        self.products_df['features'] = (
            self.products_df['category'] + ' ' + 
            self.products_df['brand'] + ' ' + 
            self.products_df['description']
        )
        
        # TF-IDF Vectorization
        tfidf = TfidfVectorizer(stop_words='english', max_features=100)
        self.tfidf_matrix = tfidf.fit_transform(self.products_df['features'])
        
    def collaborative_filtering_recommendations(self, user_id, n_recommendations=5):
        """Generate recommendations using collaborative filtering"""
        if user_id not in self.user_item_matrix.index:
            return self.popular_recommendations(n_recommendations)
        
        # SVD for matrix factorization
        svd = TruncatedSVD(n_components=10, random_state=42)
        user_item_svd = svd.fit_transform(self.user_item_matrix)
        
        # Calculate user similarities
        user_idx = self.user_item_matrix.index.get_loc(user_id)
        user_similarities = cosine_similarity([user_item_svd[user_idx]], user_item_svd)[0]
        
        # Find similar users
        similar_users_idx = user_similarities.argsort()[-6:-1][::-1]  # Top 5 similar users
        
        # Get recommendations from similar users
        user_ratings = self.user_item_matrix.iloc[user_idx]
        recommendations = {}
        
        for sim_user_idx in similar_users_idx:
            sim_user_ratings = self.user_item_matrix.iloc[sim_user_idx]
            similarity_score = user_similarities[sim_user_idx]
            
            for product_id, rating in sim_user_ratings.items():
                if rating > 0 and user_ratings[product_id] == 0:  # User hasn't rated this product
                    if product_id not in recommendations:
                        recommendations[product_id] = 0
                    recommendations[product_id] += rating * similarity_score
        
        # Sort and return top recommendations
        top_products = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:n_recommendations]
        return [product_id for product_id, score in top_products]
    
    def content_based_recommendations(self, user_id, n_recommendations=5):
        """Generate recommendations using content-based filtering"""
        # Get user's purchase history
        user_products = self.transactions_df[
            self.transactions_df['user_id'] == user_id
        ]['product_id'].tolist()
        
        if not user_products:
            return self.popular_recommendations(n_recommendations)
        
        # Get indices of user's products
        user_product_indices = []
        for product_id in user_products:
            if product_id in self.products_df['product_id'].values:
                idx = self.products_df[self.products_df['product_id'] == product_id].index[0]
                user_product_indices.append(idx)
        
        if not user_product_indices:
            return self.popular_recommendations(n_recommendations)
        
        # Calculate average feature vector for user's products
        user_profile = np.mean(self.tfidf_matrix[user_product_indices].toarray(), axis=0)
        
        # Calculate similarities with all products
        similarities = cosine_similarity([user_profile], self.tfidf_matrix)[0]
        
        # Get top similar products that user hasn't purchased
        product_similarities = list(enumerate(similarities))
        product_similarities.sort(key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for idx, similarity in product_similarities:
            product_id = self.products_df.iloc[idx]['product_id']
            if product_id not in user_products and len(recommendations) < n_recommendations:
                recommendations.append(product_id)
        
        return recommendations
    
    def popular_recommendations(self, n_recommendations=5):
        """Generate popular product recommendations as fallback"""
        popular_products = (
            self.transactions_df.groupby('product_id')
            .agg({'rating': 'mean', 'transaction_id': 'count'})
            .reset_index()
        )
        popular_products['popularity_score'] = (
            popular_products['rating'] * 0.7 + 
            (popular_products['transaction_id'] / popular_products['transaction_id'].max()) * 0.3
        )
        
        top_products = popular_products.nlargest(n_recommendations, 'popularity_score')
        return top_products['product_id'].tolist()
    
    def hybrid_recommendations(self, user_id, n_recommendations=5):
        """Generate hybrid recommendations combining collaborative and content-based"""
        cf_recs = self.collaborative_filtering_recommendations(user_id, n_recommendations)
        cb_recs = self.content_based_recommendations(user_id, n_recommendations)
        
        # Combine recommendations with weights
        hybrid_recs = []
        
        # Add collaborative filtering recommendations (weight: 0.6)
        for i, product_id in enumerate(cf_recs):
            hybrid_recs.append((product_id, 0.6 * (len(cf_recs) - i)))
        
        # Add content-based recommendations (weight: 0.4)
        for i, product_id in enumerate(cb_recs):
            existing = next((item for item in hybrid_recs if item[0] == product_id), None)
            if existing:
                # Update score if product already exists
                idx = hybrid_recs.index(existing)
                hybrid_recs[idx] = (product_id, existing[1] + 0.4 * (len(cb_recs) - i))
            else:
                hybrid_recs.append((product_id, 0.4 * (len(cb_recs) - i)))
        
        # Sort by score and return top recommendations
        hybrid_recs.sort(key=lambda x: x[1], reverse=True)
        return [product_id for product_id, score in hybrid_recs[:n_recommendations]]

def main():
    # Header
    st.markdown('<h1 class="main-header">🛍️ Pickyfy</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Product Recommendation System</p>', unsafe_allow_html=True)
    
    # Initialize recommender
    if 'recommender' not in st.session_state:
        st.session_state.recommender = ProductRecommender()
        with st.spinner('Loading sample data...'):
            st.session_state.recommender.load_sample_data()
            st.session_state.recommender.prepare_data()
    
    recommender = st.session_state.recommender
    
    # Sidebar
    st.sidebar.header("🎯 Recommendation Settings")
    
    # User selection
    user_ids = recommender.users_df['user_id'].tolist()
    selected_user = st.sidebar.selectbox("Select User ID:", user_ids)
    
    # Recommendation type
    rec_type = st.sidebar.selectbox(
        "Recommendation Method:",
        ["Hybrid", "Collaborative Filtering", "Content-Based", "Popular Items"]
    )
    
    # Number of recommendations
    n_recs = st.sidebar.slider("Number of Recommendations:", 1, 10, 5)
    
    # Main content
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f'<div class="metric-card"><h3>{len(recommender.products_df)}</h3><p>Products</p></div>',
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f'<div class="metric-card"><h3>{len(recommender.users_df)}</h3><p>Users</p></div>',
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f'<div class="metric-card"><h3>{len(recommender.transactions_df)}</h3><p>Transactions</p></div>',
            unsafe_allow_html=True
        )
    
    with col4:
        avg_rating = recommender.transactions_df['rating'].mean()
        st.markdown(
            f'<div class="metric-card"><h3>{avg_rating:.1f}</h3><p>Avg Rating</p></div>',
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    # Generate recommendations
    if st.button("🚀 Generate Recommendations", type="primary"):
        with st.spinner('Generating recommendations...'):
            if rec_type == "Hybrid":
                recommendations = recommender.hybrid_recommendations(selected_user, n_recs)
            elif rec_type == "Collaborative Filtering":
                recommendations = recommender.collaborative_filtering_recommendations(selected_user, n_recs)
            elif rec_type == "Content-Based":
                recommendations = recommender.content_based_recommendations(selected_user, n_recs)
            else:
                recommendations = recommender.popular_recommendations(n_recs)
            
            st.subheader(f"🎯 Recommendations for {selected_user} ({rec_type})")
            
            # Display recommendations
            for i, product_id in enumerate(recommendations, 1):
                product_info = recommender.products_df[
                    recommender.products_df['product_id'] == product_id
                ].iloc[0]
                
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        st.markdown(f"**#{i}**")
                        st.write(f"💰 ${product_info['price']}")
                        st.write(f"⭐ {product_info['rating']}")
                    
                    with col2:
                        st.markdown(f"**{product_info['name']}** ({product_info['product_id']})")
                        st.write(f"📂 {product_info['category']} | 🏷️ {product_info['brand']}")
                        st.write(product_info['description'])
                
                st.markdown("---")
    
    # Analytics section
    st.subheader("📊 Analytics Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["User Behavior", "Product Analysis", "Transaction Trends"])
    
    with tab1:
        # User purchase history
        user_history = recommender.transactions_df[
            recommender.transactions_df['user_id'] == selected_user
        ]
        
        if not user_history.empty:
            st.write(f"**Purchase History for {selected_user}:**")
            
            # Merge with product info
            user_products = user_history.merge(
                recommender.products_df, on='product_id'
            ).rename(columns={
                'rating_x': 'user_rating',
                'rating_y': 'product_rating'
            })[['product_id', 'name', 'category', 'user_rating', 'price', 'timestamp']]

            
            st.dataframe(user_products, use_container_width=True)
            
            # Category preferences
            category_counts = user_products['category'].value_counts()
            fig = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                title=f"{selected_user}'s Category Preferences"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"No purchase history found for {selected_user}")
    
    with tab2:
        # Product category distribution
        category_dist = recommender.products_df['category'].value_counts()
        fig = px.bar(
            x=category_dist.index,
            y=category_dist.values,
            title="Product Distribution by Category"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Price distribution
        fig = px.histogram(
            recommender.products_df,
            x='price',
            title="Product Price Distribution",
            nbins=20
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Transaction trends
        daily_transactions = (
            recommender.transactions_df.groupby(
                recommender.transactions_df['timestamp'].dt.date
            ).size().reset_index()
        )
        daily_transactions.columns = ['date', 'transactions']
        
        fig = px.line(
            daily_transactions,
            x='date',
            y='transactions',
            title="Daily Transaction Trends"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Rating distribution
        rating_dist = recommender.transactions_df['rating'].value_counts().sort_index()
        fig = px.bar(
            x=rating_dist.index,
            y=rating_dist.values,
            title="Rating Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()