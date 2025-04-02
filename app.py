import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO
import datetime

# Set page configuration
st.set_page_config(
    page_title="Task Assignment Tool",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling with dark theme
st.markdown("""
<style>
    .main {
        background-color: #1e1e1e;
        color: #e0e0e0;
    }
    .stApp {
        background-color: #1e1e1e;
        color: #e0e0e0;
    }
    .css-1d391kg {
        background-color: #2d2d2d;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #1e1e1e;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #2d2d2d;
        border-radius: 5px 5px 0 0;
        gap: 1px;
        padding: 10px 16px;
        font-weight: 500;
        color: #e0e0e0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3d3d3d;
        border-bottom: 3px solid #81c784;
        color: #81c784;
    }
    h1 {
        color: #81c784;
        padding-bottom: 10px;
        border-bottom: 2px solid #3d3d3d;
    }
    h2 {
        color: #66bb6a;
        margin-top: 30px;
    }
    h3 {
        color: #4caf50;
    }
    .stButton>button {
        background-color: #43a047;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: 500;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #4caf50;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .download-link {
        text-decoration: none;
        background-color: #43a047;
        color: white;
        padding: 8px 16px;
        border-radius: 4px;
        transition: background-color 0.3s;
    }
    .download-link:hover {
        background-color: #4caf50;
    }
    .metric-card {
        background-color: #2d2d2d;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        color: #e0e0e0;
    }
    .high-priority {
        color: #ef5350;
        font-weight: bold;
    }
    .medium-priority {
        color: #ffb74d;
        font-weight: bold;
    }
    .low-priority {
        color: #81c784;
        font-weight: bold;
    }
    /* Dark theme for dataframes */
    .stDataFrame {
        background-color: #2d2d2d;
    }
    .dataframe {
        background-color: #2d2d2d;
        color: #e0e0e0;
    }
    /* Make text inputs and number inputs visible on dark background */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #3d3d3d;
        color: #e0e0e0;
    }
    /* File uploader styling */
    .stFileUploader>div {
        background-color: #2d2d2d;
        border: 1px dashed #43a047;
        padding: 20px;
        border-radius: 5px;
    }
    /* Other Streamlit elements */
    .stSelectbox>div>div {
        background-color: #3d3d3d;
    }
    .stMultiSelect>div>div {
        background-color: #3d3d3d;
    }
    p, li, span {
        color: #e0e0e0;
    }
    /* Sidebar tweaks */
    section[data-testid="stSidebar"] {
        background-color: #2d2d2d;
    }
    section[data-testid="stSidebar"] .stTextInput>div>div>input, 
    section[data-testid="stSidebar"] .stNumberInput>div>div>input,
    section[data-testid="stSidebar"] .stSelectbox>div>div {
        background-color: #3d3d3d;
    }
    /* Info box */
    .stAlert {
        background-color: #3d3d3d !important;
        color: #e0e0e0 !important;
    }
</style>
""", unsafe_allow_html=True)

# Title and app header
st.title("📋 Task Assignment Tool")
st.markdown("""
<div style='background-color: #1b5e20; padding: 15px; border-radius: 8px; margin-bottom: 20px; color: #e0e0e0;'>
    This app automatically distributes tasks among team members while balancing priorities 
    (high, medium, low) across all team members. Each member gets a fair share 
    of all priority levels based on their capacity.
</div>
""", unsafe_allow_html=True)

# Initialize session state variables
if "team_members" not in st.session_state:
    st.session_state.team_members = {
        "Naman Chouksey": 6.5,
        "Megha Gadag": 26.5,
        "Shreeraj Hegde": 16.5,
        "Anwesha Satapathy": 36.5
    }

if "df_tasks" not in st.session_state:
    st.session_state.df_tasks = None

if "results" not in st.session_state:
    st.session_state.results = None

# Sidebar - Team Management
st.sidebar.markdown("## 👥 Team Management")
st.sidebar.markdown("<div style='background-color: #1b5e20; padding: 10px; border-radius: 5px; margin-bottom: 15px; color: #e0e0e0;'>Configure your team members and their capacity in hours.</div>", unsafe_allow_html=True)

# Edit existing team members
edited_team_members = {}
for member, capacity in st.session_state.team_members.items():
    col1, col2, col3 = st.sidebar.columns([3, 1.5, 0.5])
    
    with col1:
        st.markdown(f"**{member}**")
        
    with col2:
        edited_capacity = st.number_input(
            "Hours",
            min_value=0.0,
            max_value=100.0,
            value=float(capacity),
            step=0.5,
            key=f"capacity_{member}",
            label_visibility="collapsed"
        )
        
    with col3:
        if st.button("❌", key=f"remove_{member}"):
            continue
            
    edited_team_members[member] = edited_capacity

# Add new team member
st.sidebar.markdown("---")
st.sidebar.subheader("Add New Team Member")

new_member_name = st.sidebar.text_input("Name")
new_member_capacity = st.sidebar.number_input(
    "Capacity (hours)",
    min_value=0.0,
    max_value=100.0,
    value=20.0,
    step=0.5
)

if st.sidebar.button("Add Team Member", type="primary") and new_member_name:
    edited_team_members[new_member_name] = new_member_capacity
    
# Update session state with edited team members
st.session_state.team_members = edited_team_members

# Display team statistics
total_capacity = sum(edited_team_members.values())
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div class='metric-card'>
    <h3 style='margin-top:0'>Team Capacity</h3>
    <p style='font-size:24px; font-weight:bold; color:#81c784;'>{total_capacity} hours</p>
</div>
""", unsafe_allow_html=True)

# Main area - Task Upload
task_tab, assignment_tab, results_tab = st.tabs(["📤 Upload Tasks", "🔄 Assign Tasks", "📊 Results"])

with task_tab:
    st.header("Upload Tasks")
    st.markdown("<div style='background-color: #1b5e20; padding: 15px; border-radius: 8px; margin-bottom: 20px; color: #e0e0e0;'>Upload a CSV file containing your tasks with Priority, Original Estimates, and State columns.</div>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        try:
            # Load and prepare data
            df = pd.read_csv(uploaded_file)
            df = df.rename(columns=lambda x: x.strip())  # Clean column names
            
            # Filter out 'Done' tasks
            if "State" in df.columns:
                df = df[~df["State"].str.lower().str.contains("done", na=False)]
            
            # Store in session state
            st.session_state.df_tasks = df
            
            # Display data preview
            st.subheader("Task Preview")
            st.dataframe(df, use_container_width=True)
            
            # Task statistics
            st.subheader("Task Statistics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if "Priority" in df.columns:
                    priority_counts = df["Priority"].str.lower().value_counts()
                    
                    st.markdown(f"""
                    <div class='metric-card'>
                        <h4>Priority Breakdown</h4>
                        <p><span class='high-priority'>High: {priority_counts.get('high', 0)}</span></p>
                        <p><span class='medium-priority'>Medium: {priority_counts.get('medium', 0)}</span></p>
                        <p><span class='low-priority'>Low: {priority_counts.get('low', 0)}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                if "Original Estimates" in df.columns:
                    total_estimate = df["Original Estimates"].sum()
                    avg_estimate = df["Original Estimates"].mean()
                    
                    st.markdown(f"""
                    <div class='metric-card'>
                        <h4>Work Estimates</h4>
                        <p>Total: <b>{total_estimate:.1f} hours</b></p>
                        <p>Average: <b>{avg_estimate:.1f} hours/task</b></p>
                    </div>
                    """, unsafe_allow_html=True)
                
            with col3:
                if "Original Estimates" in df.columns:
                    capacity_ratio = total_estimate / total_capacity if total_capacity > 0 else 0
                    
                    status_color = "#388e3c" if capacity_ratio <= 1 else "#d32f2f"
                    status_message = f"Team has {(1-capacity_ratio)*100:.1f}% spare capacity" if capacity_ratio <= 1 else f"Work exceeds capacity by {(capacity_ratio-1)*100:.1f}%"
                    
                    st.markdown(f"""
                    <div class='metric-card'>
                        <h4>Capacity Analysis</h4>
                        <p>Work/Capacity Ratio: <b>{capacity_ratio:.2f}</b></p>
                        <p style='color:{status_color};'><b>{status_message}</b></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error("Please make sure your CSV file has the required columns (Priority, Original Estimates, State)")
    else:
        st.info("Please upload a CSV file with your tasks data")
        
        # Sample structure explanation
        with st.expander("CSV Format Requirements"):
            st.markdown("""
            Your CSV file should include these columns:
            
            - **Work Item Type**: Type of the task
            - **ID**: Unique identifier for the task
            - **Title**: Task title
            - **Priority**: Task priority (high, medium, low)
            - **State**: Current state of the task (should not be "Done")
            - **Original Estimates**: Estimated hours required for the task
            """)

with assignment_tab:
    st.header("Assign Tasks")
    
    if st.session_state.df_tasks is None:
        st.warning("Please upload tasks data in the Upload Tasks tab first.")
    else:
        st.markdown("<div style='background-color: #1b5e20; padding: 15px; border-radius: 8px; margin-bottom: 20px; color: #e0e0e0;'>Configure assignment options and run the task distribution algorithm.</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            priority_balance = st.slider(
                "Priority Balance",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher values prioritize even distribution of priorities, lower values focus on capacity utilization"
            )
        
        with col2:
            respect_category = st.checkbox(
                "Consider Category Specialization",
                value=False,
                help="When enabled, members will be assigned tasks from their specialized categories when possible"
            )
            
        # Assignment button
        if st.button("Run Assignment", type="primary", use_container_width=True):
            # Get the data
            df = st.session_state.df_tasks.copy()
            team_members = st.session_state.team_members
            
            # Check for required columns
            required_columns = ["Priority", "Original Estimates"]
            if not all(col in df.columns for col in required_columns):
                st.error(f"CSV must contain these columns: {', '.join(required_columns)}")
            else:
                with st.spinner("Assigning tasks..."):
                    # Prepare data
                    assigned_hours = {member: 0 for member in team_members}
                    assigned_priorities = {member: {"high": 0, "medium": 0, "low": 0, "other": 0} for member in team_members}
                    
                    # Define priority order and sort tasks
                    priority_order = {"high": 1, "medium": 2, "low": 3}
                    df["PriorityOrder"] = df["Priority"].str.lower().map(priority_order).fillna(4)
                    df = df.sort_values("PriorityOrder")
                    
                    # Add columns if missing
                    if "Assigned To" not in df.columns:
                        df["Assigned To"] = ""
                    if "Iteration Path" not in df.columns:
                        df["Iteration Path"] = ""
                    
                    # Modified assignment algorithm to balance all priorities across team members
                    for priority_level in ["high", "medium", "low", "other"]:
                        # Filter tasks for current priority
                        if priority_level == "other":
                            priority_tasks = df[~df["Priority"].str.lower().isin(["high", "medium", "low"])]
                        else:
                            priority_tasks = df[df["Priority"].str.lower() == priority_level]
                        
                        if len(priority_tasks) == 0:
                            continue
                        
                        # Reset member order for each priority level
                        member_order = list(team_members.keys())
                        
                        # Assign tasks for this priority level
                        for idx in priority_tasks.index:
                            task = df.loc[idx]
                            estimate = task["Original Estimates"]
                            
                            if pd.isna(estimate) or estimate <= 0:
                                continue
                            
                            # Shuffle members based on current assignments of this priority and remaining capacity
                            shuffled_members = sorted(
                                member_order,
                                key=lambda m: (
                                    assigned_priorities[m][priority_level if priority_level != "other" else "other"],
                                    assigned_hours[m] / team_members[m] if team_members[m] > 0 else float('inf')
                                )
                            )
                            
                            # Try to assign to the first available member
                            for member in shuffled_members:
                                remaining_capacity = team_members[member] - assigned_hours[member]
                                
                                if estimate <= remaining_capacity:
                                    df.at[idx, "Assigned To"] = member
                                    df.at[idx, "Iteration Path"] = "/priority_balanced"
                                    
                                    assigned_hours[member] += estimate
                                    if priority_level in ["high", "medium", "low"]:
                                        assigned_priorities[member][priority_level] += 1
                                    else:
                                        assigned_priorities[member]["other"] += 1
                                    
                                    # Re-sort member order
                                    member_order = sorted(
                                        member_order,
                                        key=lambda m: assigned_priorities[m][priority_level if priority_level != "other" else "other"]
                                    )
                                    break
                    
                    # Clean up
                    if "PriorityOrder" in df.columns:
                        df = df.drop(columns=["PriorityOrder"])
                    
                    # Store results
                    st.session_state.results = {
                        "df": df,
                        "assigned_hours": assigned_hours,
                        "assigned_priorities": assigned_priorities,
                        "team_members": team_members
                    }
                    
                    # Switch to results tab
                    st.success("Tasks assigned successfully! See the Results tab for details.")
                    
with results_tab:
    st.header("Assignment Results")
    
    if st.session_state.results is None:
        st.warning("No assignment results available. Please run the assignment algorithm first.")
    else:
        results = st.session_state.results
        df = results["df"]
        assigned_hours = results["assigned_hours"]
        assigned_priorities = results["assigned_priorities"]
        team_members = results["team_members"]
        
        # Assignment summary
        st.subheader("Summary")
        
        total_assigned = sum(assigned_hours.values())
        total_capacity = sum(team_members.values())
        percent_utilized = (total_assigned / total_capacity * 100) if total_capacity > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Tasks Assigned", len(df[df["Assigned To"] != ""]))
            
        with col2:
            st.metric("Hours Assigned", f"{total_assigned:.1f}/{total_capacity:.1f}")
            
        with col3:
            st.metric("Capacity Utilized", f"{percent_utilized:.1f}%")
            
        # Detailed results
        st.subheader("Assigned Tasks")
        st.dataframe(
            df,
            column_config={
                "Priority": st.column_config.Column(
                    "Priority",
                    help="Task priority level",
                    width="medium",
                ),
                "Original Estimates": st.column_config.NumberColumn(
                    "Hours",
                    help="Estimated work hours",
                    format="%.1f",
                ),
                "Assigned To": st.column_config.Column(
                    "Assigned To",
                    help="Team member assigned to the task",
                    width="medium",
                ),
            },
            use_container_width=True
        )
        
        # Visualizations
        st.subheader("Capacity Utilization")
        
        # Prepare data for visualization
        members = list(team_members.keys())
        capacities = [team_members[m] for m in members]
        used_capacities = [assigned_hours[m] for m in members]
        remaining_capacities = [capacities[i] - used_capacities[i] for i in range(len(members))]
        
        # Create capacity chart with dark theme
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 5))
        bar_width = 0.35
        x = np.arange(len(members))
        
        # Use more vibrant colors for dark theme
        ax.bar(x, used_capacities, bar_width, label='Used', color='#81c784')
        ax.bar(x, remaining_capacities, bar_width, bottom=used_capacities, label='Remaining', color='#455a64')
        
        ax.set_ylabel('Hours', color='#e0e0e0')
        ax.set_title('Capacity Utilization by Team Member', color='#81c784')
        ax.set_xticks(x)
        ax.set_xticklabels(members, rotation=45, ha='right', color='#e0e0e0')
        ax.tick_params(axis='y', colors='#e0e0e0')
        ax.spines['bottom'].set_color('#555555')
        ax.spines['top'].set_color('#555555')
        ax.spines['left'].set_color('#555555')
        ax.spines['right'].set_color('#555555')
        ax.grid(color='#333333', linestyle='-', linewidth=0.5, alpha=0.7)
        ax.legend(facecolor='#2d2d2d', edgecolor='#555555', labelcolor='#e0e0e0')
        
        fig.patch.set_facecolor('#1e1e1e')
        plt.tight_layout()
        st.pyplot(fig)
        
        # Priority distribution
        st.subheader("Priority Distribution")
        
        # Prepare data for priority chart
        priorities = ["high", "medium", "low", "other"]
        priority_data = {member: [assigned_priorities[member].get(p, 0) for p in priorities] for member in members}
        
        # Create stacked bar chart with dark theme
        # We're already using dark_background style from the previous chart
        fig, ax = plt.subplots(figsize=(10, 5))
        bottom = np.zeros(len(members))
        
        # Enhanced colors for better visibility on dark background
        colors = {'high': '#ef5350', 'medium': '#ffb74d', 'low': '#81c784', 'other': '#b0bec5'}
        
        for i, priority in enumerate(priorities):
            priority_counts = [priority_data[member][i] for member in members]
            ax.bar(members, priority_counts, bottom=bottom, label=priority.capitalize(), color=colors[priority])
            bottom += priority_counts
        
        ax.set_ylabel('Number of Tasks', color='#e0e0e0')
        ax.set_title('Priority Distribution by Team Member', color='#81c784')
        ax.set_xticks(range(len(members)))
        ax.set_xticklabels(members, rotation=45, ha='right', color='#e0e0e0')
        ax.tick_params(axis='y', colors='#e0e0e0')
        ax.spines['bottom'].set_color('#555555')
        ax.spines['top'].set_color('#555555')
        ax.spines['left'].set_color('#555555')
        ax.spines['right'].set_color('#555555')
        ax.grid(color='#333333', linestyle='-', linewidth=0.5, alpha=0.7)
        ax.legend(facecolor='#2d2d2d', edgecolor='#555555', labelcolor='#e0e0e0')
        
        fig.patch.set_facecolor('#1e1e1e')
        plt.tight_layout()
        st.pyplot(fig)
        
        # Download options
        st.subheader("Export Results")
        
        col1, col2 = st.columns(2)
        
        # Function to convert to Excel
        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Tasks')
            processed_data = output.getvalue()
            return processed_data
        
        # Function to get download link
        def get_download_link(df, filename, format_type):
            if format_type == 'excel':
                data = to_excel(df)
                b64 = base64.b64encode(data).decode()
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}" class="download-link">Download Excel File</a>'
            elif format_type == 'csv':
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:text/csv;base64,{b64}" download="{filename}" class="download-link">Download CSV File</a>'
            return href
        
        with col1:
            st.markdown(get_download_link(df, "Task_Assignments.xlsx", "excel"), unsafe_allow_html=True)
            
        with col2:
            st.markdown(get_download_link(df, "Task_Assignments.csv", "csv"), unsafe_allow_html=True)