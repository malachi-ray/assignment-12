# Module 12 Assignment: Business Analytics Fundamentals and Applications
# GreenGrocer Data Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Welcome message
print("=" * 60)
print("GREENGROCER BUSINESS ANALYTICS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Set seed for reproducibility
np.random.seed(42)

# Store information
stores = ["Tampa", "Orlando", "Miami", "Jacksonville", "Gainesville"]
store_data = {
    "Store": stores,
    "SquareFootage": [15000, 12000, 18000, 10000, 8000],
    "StaffCount": [45, 35, 55, 30, 25],
    "YearsOpen": [5, 3, 7, 2, 1],
    "WeeklyMarketingSpend": [2500, 2000, 3000, 1800, 1500]
}

# Create store dataframe
store_df = pd.DataFrame(store_data)

# Product categories and departments
departments = ["Produce", "Dairy", "Bakery", "Grocery", "Prepared Foods"]
categories = {
    "Produce": ["Organic Vegetables", "Organic Fruits", "Fresh Herbs"],
    "Dairy": ["Milk & Cream", "Cheese", "Yogurt"],
    "Bakery": ["Bread", "Pastries", "Cakes"],
    "Grocery": ["Grains", "Canned Goods", "Snacks"],
    "Prepared Foods": ["Hot Bar", "Salad Bar", "Sandwiches"]
}

# Generate sales data for each store
sales_data = []
dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

# Base performance factors for each store (relative scale)
store_performance = {
    "Tampa": 1.0, 
    "Orlando": 0.85, 
    "Miami": 1.2, 
    "Jacksonville": 0.75, 
    "Gainesville": 0.65
}

# Base performance factors for each department (relative scale)
dept_performance = {
    "Produce": 1.2,
    "Dairy": 1.0,
    "Bakery": 0.85,
    "Grocery": 0.95,
    "Prepared Foods": 1.1
}

# Generate daily sales data for each store, department, and category
for date in dates:
    # Seasonal factor (higher in summer and December)
    month = date.month
    seasonal_factor = 1.0
    if month in [6, 7, 8]:  # Summer
        seasonal_factor = 1.15
    elif month == 12:  # December
        seasonal_factor = 1.25
    elif month in [1, 2]:  # Winter
        seasonal_factor = 0.9
    
    # Day of week factor (weekends are busier)
    dow_factor = 1.3 if date.dayofweek >= 5 else 1.0  # Weekend vs weekday
    
    for store in stores:
        store_factor = store_performance[store]
        
        for dept in departments:
            dept_factor = dept_performance[dept]
            
            for category in categories[dept]:
                # Base sales amount
                base_sales = np.random.normal(loc=500, scale=100)
                
                # Calculate final sales with all factors and some randomness
                sales_amount = base_sales * store_factor * dept_factor * seasonal_factor * dow_factor
                sales_amount = sales_amount * np.random.normal(loc=1.0, scale=0.1)  # Add noise
                
                # Calculate profit margin (different base margins for departments)
                base_margin = {
                    "Produce": 0.25,
                    "Dairy": 0.22,
                    "Bakery": 0.35,
                    "Grocery": 0.20,
                    "Prepared Foods": 0.40
                }[dept]
                profit_margin = base_margin * np.random.normal(loc=1.0, scale=0.05)
                profit_margin = max(min(profit_margin, 0.5), 0.15)  # Keep within reasonable range
                
                # Calculate profit
                profit = sales_amount * profit_margin
                
                # Add record
                sales_data.append({
                    "Date": date,
                    "Store": store,
                    "Department": dept,
                    "Category": category,
                    "Sales": round(sales_amount, 2),
                    "ProfitMargin": round(profit_margin, 4),
                    "Profit": round(profit, 2)
                })

# Create sales dataframe
sales_df = pd.DataFrame(sales_data)

# Generate customer data
customer_data = []
total_customers = 5000

# Age distribution parameters
age_mean, age_std = 42, 15

# Income distribution parameters (in $1000s)
income_mean, income_std = 85, 30

# Create customer segments (will indirectly influence spending)
segments = ["Health Enthusiast", "Gourmet Cook", "Family Shopper", "Budget Organic", "Occasional Visitor"]
segment_probabilities = [0.25, 0.20, 0.30, 0.15, 0.10]

# Store preference probabilities (matches store performance somewhat)
store_probs = {
    "Tampa": 0.25,
    "Orlando": 0.20,
    "Miami": 0.30,
    "Jacksonville": 0.15,
    "Gainesville": 0.10
}

for i in range(total_customers):
    # Basic demographics
    age = int(np.random.normal(loc=age_mean, scale=age_std))
    age = max(min(age, 85), 18)  # Keep age in reasonable range
    
    gender = np.random.choice(["M", "F"], p=[0.48, 0.52])
    
    income = int(np.random.normal(loc=income_mean, scale=income_std))
    income = max(income, 20)  # Minimum income
    
    # Customer segment
    segment = np.random.choice(segments, p=segment_probabilities)
    
    # Preferred store
    preferred_store = np.random.choice(stores, p=list(store_probs.values()))
    
    # Shopping behavior - influenced by segment
    if segment == "Health Enthusiast":
        visit_frequency = np.random.randint(8, 15)  # Visits per month
        avg_basket = np.random.normal(loc=75, scale=15)
    elif segment == "Gourmet Cook":
        visit_frequency = np.random.randint(4, 10)
        avg_basket = np.random.normal(loc=120, scale=25)
    elif segment == "Family Shopper":
        visit_frequency = np.random.randint(5, 12)
        avg_basket = np.random.normal(loc=150, scale=30)
    elif segment == "Budget Organic":
        visit_frequency = np.random.randint(6, 10)
        avg_basket = np.random.normal(loc=60, scale=10)
    else:  # Occasional Visitor
        visit_frequency = np.random.randint(1, 5)
        avg_basket = np.random.normal(loc=45, scale=15)
    
    # Ensure values are reasonable
    visit_frequency = max(min(visit_frequency, 30), 1)
    avg_basket = max(avg_basket, 15)
    
    # Loyalty tier based on combination of frequency and spending
    monthly_spend = visit_frequency * avg_basket
    if monthly_spend > 1000:
        loyalty_tier = "Platinum"
    elif monthly_spend > 500:
        loyalty_tier = "Gold"
    elif monthly_spend > 200:
        loyalty_tier = "Silver"
    else:
        loyalty_tier = "Bronze"
    
    # Add to customer data
    customer_data.append({
        "CustomerID": f"C{i+1:04d}",
        "Age": age,
        "Gender": gender,
        "Income": income * 1000,  # Convert to actual income
        "Segment": segment,
        "PreferredStore": preferred_store,
        "VisitsPerMonth": visit_frequency,
        "AvgBasketSize": round(avg_basket, 2),
        "MonthlySpend": round(visit_frequency * avg_basket, 2),
        "LoyaltyTier": loyalty_tier
    })

# Create customer dataframe
customer_df = pd.DataFrame(customer_data)

# Create some calculated operational metrics for stores
operational_data = []

for store in stores:
    # Get store details
    store_row = store_df[store_df["Store"] == store].iloc[0]
    square_footage = store_row["SquareFootage"]
    staff_count = store_row["StaffCount"]
    
    # Calculate store metrics
    store_sales = sales_df[sales_df["Store"] == store]["Sales"].sum()
    store_profit = sales_df[sales_df["Store"] == store]["Profit"].sum()
    
    # Calculate derived metrics
    sales_per_sqft = store_sales / square_footage
    profit_per_sqft = store_profit / square_footage
    sales_per_staff = store_sales / staff_count
    inventory_turnover = np.random.uniform(12, 18) * store_performance[store]
    customer_satisfaction = min(5, np.random.normal(loc=4.0, scale=0.3) * 
                                (store_performance[store] ** 0.5))
    
    # Add to operational data
    operational_data.append({
        "Store": store,
        "AnnualSales": round(store_sales, 2),
        "AnnualProfit": round(store_profit, 2),
        "SalesPerSqFt": round(sales_per_sqft, 2),
        "ProfitPerSqFt": round(profit_per_sqft, 2),
        "SalesPerStaff": round(sales_per_staff, 2),
        "InventoryTurnover": round(inventory_turnover, 2),
        "CustomerSatisfaction": round(customer_satisfaction, 2)
    })

# Create operational dataframe
operational_df = pd.DataFrame(operational_data)

# Print data info
print("\nDataframes created successfully. Ready for analysis!")
print(f"Sales data shape: {sales_df.shape}")
print(f"Customer data shape: {customer_df.shape}")
print(f"Store data shape: {store_df.shape}")
print(f"Operational data shape: {operational_df.shape}")

# Print sample of each dataframe
print("\nSales Data Sample:")
print(sales_df.head(3))
print("\nCustomer Data Sample:")
print(customer_df.head(3))
print("\nStore Data Sample:")
print(store_df)
print("\nOperational Data Sample:")
print(operational_df)
# ----- END OF DATA CREATION -----


# TODO 1: Descriptive Analytics - Overview of Current Performance
# 1.1 Calculate and display basic descriptive statistics for sales and profit
# REQUIRED: Store results in variables for testing
def analyze_sales_performance():
    """
    Analyze overall sales performance with descriptive statistics
    REQUIRED: Create and return dictionary with keys:
    - 'total_sales': float
    - 'total_profit': float
    - 'avg_profit_margin': float
    - 'sales_by_store': pandas Series
    - 'sales_by_dept': pandas Series
    """
    # Your code here
    total_sales = sales_df['Sales'].sum()
    total_profit = sales_df['Profit'].sum()
    avg_profit_margin = sales_df['ProfitMargin'].mean()
    sales_by_store = sales_df.groupby(sales_df['Store'])['Sales'].sum()
    sales_by_dept = sales_df.groupby(sales_df['Department'])['Sales'].sum()
    return {'total_sales':total_sales,'total_profit':total_profit,'avg_profit_margin':avg_profit_margin,'sales_by_store':sales_by_store,'sales_by_dept':sales_by_dept}


# 1.2 Create visualizations showing sales distribution by store, department, and time
# REQUIRED: Return matplotlib figures
def visualize_sales_distribution():
    """
    Create visualizations showing how sales are distributed
    REQUIRED: Return tuple of three figures (store_fig, dept_fig, time_fig)
    """
    # Your code here
    store_sales = analyze_sales_performance()['sales_by_store']
    dept_sales = analyze_sales_performance()['sales_by_dept']
    
    store_fig,ax1 = plt.subplots()
    ax1.bar(store_sales.index,store_sales.values,color='green')
    ax1.set_title("Sales by Store")
    ax1.set_ylabel("Sales ($)")
    ax1.set_xlabel('Store')
    ax1.grid(True,alpha=0.6,linestyle='--')
    
    dept_fig,ax2 = plt.subplots()
    ax2.bar(dept_sales.index,dept_sales.values,color='red')
    ax2.set_title("Sales by Department")
    ax2.set_ylabel("Sales ($)")
    ax2.set_xlabel('Department')
    ax2.grid(True,alpha=0.6,linestyle='--')
    
    time_fig,ax3 = plt.subplots(figsize=(12,9))
    date_sales = sales_df.groupby(sales_df['Date'])['Sales'].sum()
    ax3.plot(date_sales.index, date_sales.values ,color='blue')
    ax3.set_title("Sales by Date")
    ax3.set_ylabel("Sales ($)")
    ax3.set_xlabel('Date')
    ax3.grid(True,alpha=0.6,linestyle='--')
    
    return (store_fig,dept_fig,time_fig)
    

# 1.3 Analyze customer segments and their spending patterns
# REQUIRED: Return analysis results
def analyze_customer_segments():
    """
    Analyze customer segments and their relationship to spending
    REQUIRED: Return dictionary with keys:
    - 'segment_counts': pandas Series
    - 'segment_avg_spend': pandas Series
    - 'segment_loyalty': pandas DataFrame
    """
    # Your code here
    segment_counts = customer_df['Segment'].value_counts()
    segment_avg_spend = customer_df.groupby('Segment')['MonthlySpend'].mean()
    segment_loyalty = customer_df.groupby(['Segment','LoyaltyTier'])['CustomerID'].count()
    return {'segment_counts':segment_counts, 'segment_avg_spend':segment_avg_spend, 'segment_loyalty':segment_loyalty}


# TODO 2: Diagnostic Analytics - Understanding Relationships
# 2.1 Identify factors correlated with sales performance
# REQUIRED: Return correlation results
def analyze_sales_correlations():
    """
    Analyze correlations between various factors and sales performance
    REQUIRED: Return dictionary with keys:
    - 'store_correlations': pandas DataFrame
    - 'top_correlations': list of tuples (factor, correlation)
    - 'correlation_fig': matplotlib figure
    """
    # Your code here
    store_correlations = operational_df.drop(columns=['Store']).corr()
    
    sales_corr = store_correlations['AnnualSales'].drop('AnnualSales')
    
    top_corrs = sales_corr.abs().sort_values(ascending=False).head(5)
    top_corrs = list(top_corrs.items())

    correlation_fig,ax = plt.subplots(figsize=(6,4))
    ax.scatter(store_correlations.index,store_correlations['AnnualSales'])
    ax.tick_params(axis='x',labelrotation=270)
    correlation_fig.subplots_adjust(top=.9,bottom=.35)
    return {'store_correlations':store_correlations,'top_correlations':top_corrs,'correlation_fig':correlation_fig}
# 2.2 Compare stores based on operational metrics
# REQUIRED: Return comparison results
def compare_store_performance():
    """
    Compare stores across different operational metrics
    REQUIRED: Return dictionary with keys:
    - 'efficiency_metrics': pandas DataFrame (with SalesPerSqFt, SalesPerStaff)
    - 'performance_ranking': pandas Series (ranked by profit)
    - 'comparison_fig': matplotlib figure
    """
    # Your code here
    efficiency_metrics = operational_df[['SalesPerSqFt','SalesPerStaff']]
    performance_ranking = operational_df.sort_values('AnnualProfit',ascending=False)['Store']
    
    comparison_fig, ax = plt.subplots(1,2)
    ax[0].bar(performance_ranking.values,efficiency_metrics['SalesPerSqFt'],color='green',label='Sales Per Sq Ft')
    ax[1].bar(performance_ranking.values,efficiency_metrics['SalesPerStaff'],color='blue',label='Sales Per Staff')
    
    ax[0].set_title("Sales Per Sq Ft by Store")
    ax[0].set_xlabel("Store")
    ax[0].tick_params('x',rotation=90)
    ax[0].set_ylabel("Sales per Sq Ft($)")
    ax[0].grid(True,alpha=0.6,linestyle='--')
    
    ax[1].set_title("Sales Per Staff by Store")
    ax[1].set_xlabel("Store")
    ax[1].tick_params('x',rotation=90)
    ax[1].set_ylabel("Sales per Staff ($)")
    ax[1].grid(True,alpha=0.6,linestyle='--')
    comparison_fig.tight_layout()
# 2.3 Analyze seasonal patterns and their impact
# REQUIRED: Return seasonal analysis
def analyze_seasonal_patterns():
    """
    Identify and visualize seasonal patterns in sales data
    REQUIRED: Return dictionary with keys:
    - 'monthly_sales': pandas Series
    - 'dow_sales': pandas Series (day of week)
    - 'seasonal_fig': matplotlib figure
    """
    # Your code here
    monthly_sales = sales_df.groupby(sales_df['Date'].dt.month_name(),sort=False)['Sales'].sum()
    dow_sales = sales_df.groupby(sales_df['Date'].dt.day_name(),sort=False)['Sales'].sum()
    
    seasonal_fig, ax = plt.subplots(1,2)
    ax[0].plot(monthly_sales, linestyle='-')
    ax[0].set_title("Sales by Month")
    ax[0].set_xlabel("Month")
    ax[0].tick_params('x',rotation=90)
    ax[0].set_ylabel("Sales ($)")
    ax[0].grid(True,alpha=0.6,linestyle='--')
    
    ax[1].plot(dow_sales, linestyle='-')
    ax[1].set_title("Sales by Day of Week")
    ax[1].set_xlabel("Store")
    ax[1].tick_params('x',rotation=90)
    ax[1].set_ylabel("Sales ($)")
    ax[1].grid(True,alpha=0.6,linestyle='--')
    seasonal_fig.tight_layout()
    
    return {'monthly_sales':monthly_sales,'dow_sales':dow_sales,'seasonal_fig':seasonal_fig}
# TODO 3: Predictive Analytics - Basic Forecasting
# 3.1 Create a simple linear regression model to predict store sales
# REQUIRED: Return model results
def predict_store_sales():
    """
    Use linear regression to predict store sales based on store characteristics
    REQUIRED: Return dictionary with keys:
    - 'coefficients': dict (feature: coefficient)
    - 'r_squared': float
    - 'predictions': pandas Series
    - 'model_fig': matplotlib figure
    """
    # Your code here
    slope_sf, intercept_sf = np.polyfit(store_df['SquareFootage'], operational_df['AnnualSales'], 1)
    slope_sc, intercept_sc = np.polyfit(store_df['StaffCount'], operational_df['AnnualSales'], 1)
    slope_yo, intercept_yo = np.polyfit(store_df['YearsOpen'], operational_df['AnnualSales'], 1)
    slope_wms, intercept_wms = np.polyfit(store_df['WeeklyMarketingSpend'], operational_df['AnnualSales'], 1)
    coefficients = {'SquareFootage':slope_sf, 'StaffCount':slope_sc, 'YearsOpen':slope_yo, 'WeeklyMarketingSpend':slope_wms,}
    
    coeffs, residuals, rank, singular_values, rcond = np.polyfit(store_df['StaffCount'], operational_df['AnnualSales'], 1, full=True)
    
    # residuals is the SS_res
    ss_res = residuals[0]
    ss_tot = np.sum((operational_df['AnnualSales'] - np.mean(operational_df['AnnualSales']))**2)
    r_squared = 1 - (ss_res / ss_tot)
    
    pred_dict = {}
    predictions_list = [60,65,70,75,80]
    for i in predictions_list:
        pred_dict[i] = ((slope_sc*i)+intercept_sc)
    predictions = pd.Series(pred_dict)
    
    model_fig, ax = plt.subplots()
    ax.scatter(x=store_df['StaffCount'],y=operational_df['AnnualSales'])
    ax.plot(store_df['StaffCount'], intercept_sc + slope_sc*store_df['StaffCount'])
    ax.set_ylabel("Annual Sales")
    ax.set_xlabel("# of Staff")
    ax.set_title("Annual Sales by # of Staff")
    
    return coefficients, r_squared, predictions, model_fig

# 3.2 Forecast departmental sales trends
# REQUIRED: Return forecast results
def forecast_department_sales():
    """
    Analyze and forecast departmental sales trends
    REQUIRED: Return dictionary with keys:
    - 'dept_trends': pandas DataFrame
    - 'growth_rates': pandas Series
    - 'forecast_fig': matplotlib figure
    """
    # Your code here
    dept_list = sales_df['Department'].unique()
    
    dept_df = sales_df.copy()
    dept_df['Month'] = dept_df['Date'].dt.month
    dept_df['Day'] = dept_df['Date'].dt.day
    dept_trends = dept_df.groupby(['Department','Month','Day'])['Sales'].sum().reset_index()

    dept_trends['GrowthRate'] = dept_trends['Sales'].pct_change(periods=1)

    growth_rates = dept_trends.groupby(['Department','Month'])['GrowthRate'].mean()    
    
    forecast_fig, ax = plt.subplots()
    color_dict = {"Bakery":'r','Dairy':'b','Grocery':'purple','Prepared Foods':'y', 'Produce':'g'}
    for dept in dept_list:
        working_df = dept_trends[dept_trends['Department']==dept]
        sales_monthly = working_df.groupby('Month')['Sales'].sum()
        
        ax.plot(sales_monthly.index, sales_monthly.values, linestyle='-', color=color_dict[dept], label=dept)
        last_sales=sales_monthly[12]
        predictions = {12:last_sales}
        
        for i in range(1,13):
            new_sales = last_sales*(1 + growth_rates[dept][i])
            predictions[i+12] = new_sales
            last_sales = new_sales
        predictions_series = pd.Series(predictions)
        ax.plot(predictions_series.index, predictions_series.values, linestyle='--', color=color_dict[dept],label=(dept+' Forecast'))
    ax.set_xlabel("Months from Jan 2023")
    ax.set_ylabel('Sales ($)')
    ax.set_title("Sales Trends and Forecasts by Department")
    ax.legend()
    forecast_fig.tight_layout()
    
    return dept_trends, growth_rates, forecast_fig

# TODO 4: Integrated Analysis - Business Insights and Recommendations
# 4.1 Identify the most profitable combinations of store, department, and customer segments
# REQUIRED: Return opportunity analysis
def identify_profit_opportunities():
    """
    Identify the most profitable combinations and potential opportunities
    REQUIRED: Return dictionary with keys:
    - 'top_combinations': pandas DataFrame (top 10 store-dept combinations)
    - 'underperforming': pandas DataFrame (bottom 10)
    - 'opportunity_score': pandas Series (by store)
    """
    # Your code here
    grouped_frame = sales_df.groupby(['Store', 'Department'])['Profit'].sum().reset_index().sort_values(by='Profit',ascending=False)
    top_combinations = grouped_frame.head(10)
    underperforming = grouped_frame.tail(10)
    
    store_list = sales_df['Store'].unique()
    vals = [5,4,4,2,3]
    opportunity_score = pd.Series(vals,index=store_list)
    
    return top_combinations, underperforming, opportunity_score

# 4.2 Develop recommendations for improving performance
# REQUIRED: Return list of recommendations
def develop_recommendations():
    """
    Develop actionable recommendations based on the analysis
    REQUIRED: Return list of at least 5 recommendation strings
    """
    # Your code here
    return ['Investigate the lack of profitability of the Grocery and Dairy departments, as they are underperforming in most stores.',
            'Major sales drop in September, October, and November could be mitigated with more aggressive marketing and promotions.',
            "Weekday sales are significantly lower than weekend sales, add BOGO's and other deals to increase said sales.",
            "Increase the size of the Gainsville location, as it has some of the best sales ratios while being the smallest location.",
            "Maintain customer satisfaction, as it shows extremely high correlation with sales."]


# TODO 5: Summary Report
# REQUIRED: Generate comprehensive summary
def generate_executive_summary():
    """
    Generate an executive summary of key findings and recommendations
    REQUIRED: Print executive summary with sections:
    - Overview (1 paragraph)
    - Key Findings (3-5 bullet points)
    - Recommendations (3-5 bullet points)
    - Expected Impact (1 paragraph)
    """
    # Your code here
    print("""Overall, successful profitability has been maintained, and sales numbers continue to grow. We are, all in all, looking at a good year. Although we're perfoming well so far, we should still look to improve. The main findings to focus on will be our sales patterns, both weekly and yearly,as well as some areas of particular success we want to maintain.

Key Findings:
-Major sales drop in fall months
-Gainsville location showing strong efficiency
-Customer satisfaction showing major correlation with sales

Recommendations:
-Run more sales and promotions during fall months
-Study Gainesville management's tactics and look to incorporate in other locations
-Increase loyalty rewards to keep boosting customer satisfaction

We expect that these changes will further boost sales, and as a byproduct, profitability. Ideally, we could use the knowledge imparted by the Gainesville location to either further expand or reduce the amount of active staff, thus saving money on payroll. Furthermore, we hope to keep improving customer satisfaction and can expect to see further sales growth from that.""")

# Main function to execute all analyses
# REQUIRED: Do not modify function name
def main():
    print("\n" + "=" * 60)
    print("GREENGROCER BUSINESS ANALYTICS RESULTS")
    print("=" * 60)
    
    # Execute analyses in a logical order
    # REQUIRED: Store all results for potential testing
    
    print("\n--- DESCRIPTIVE ANALYTICS: CURRENT PERFORMANCE ---")
    sales_metrics = analyze_sales_performance()
    dist_figs = visualize_sales_distribution()
    customer_analysis = analyze_customer_segments()
    
    print("\n--- DIAGNOSTIC ANALYTICS: UNDERSTANDING RELATIONSHIPS ---")
    correlations = analyze_sales_correlations()
    store_comparison = compare_store_performance()
    seasonality = analyze_seasonal_patterns()
    
    print("\n--- PREDICTIVE ANALYTICS: FORECASTING ---")
    sales_model = predict_store_sales()
    dept_forecast = forecast_department_sales()
    
    print("\n--- BUSINESS INSIGHTS AND RECOMMENDATIONS ---")
    opportunities = identify_profit_opportunities()
    recommendations = develop_recommendations()
    
    print("\n--- EXECUTIVE SUMMARY ---")
    generate_executive_summary()
    
    # Show all figures
    plt.show()
    
    # Return results for testing purposes
    return {
        'sales_metrics': sales_metrics,
        'customer_analysis': customer_analysis,
        'correlations': correlations,
        'store_comparison': store_comparison,
        'seasonality': seasonality,
        'sales_model': sales_model,
        'dept_forecast': dept_forecast,
        'opportunities': opportunities,
        'recommendations': recommendations
    }

# Run the main function
if __name__ == "__main__":
    results = main()