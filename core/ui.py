import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Add parent directory to path to import config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ORGANIZATIONS, DEFAULT_ORG, DEFAULT_CSV_PATH

# Get default organization config
org_key_default = list(ORGANIZATIONS.keys()).index(DEFAULT_ORG) if DEFAULT_ORG in ORGANIZATIONS else 0
default_org_config = ORGANIZATIONS[list(ORGANIZATIONS.keys())[org_key_default]]

# SET PAGE CONFIG FIRST - BEFORE ANY OTHER STREAMLIT COMMANDS
st.set_page_config(
    page_title=f"{default_org_config['name']} GitHub Analytics {default_org_config['year']}",
    layout="wide",
    initial_sidebar_state="expanded"
)

# NOW import remaining modules after set_page_config
from main import (clean_data, totalActiveDays, longestGap, busiestDay, longestStreak, 
                  monthWiseActivity, timeWiseActivity, allDeveloperActivity, repoActivity,
                  getTopRepositories, getCommitFrequency, getActivityByHour, getActivityCalendar,
                  getMostActiveRepositories, getContributorStats, getContributorDetails, getContributorTimeline)
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# ===== SIDEBAR CONFIGURATION =====
st.sidebar.title("Dashboard Configuration")
st.sidebar.markdown("---")

# Organization selector
st.sidebar.subheader("Organization Settings")
org_key = st.sidebar.selectbox(
    "Select Organization",
    options=list(ORGANIZATIONS.keys()),
    index=org_key_default,
    help="Choose the organization to analyze"
)

org_config = ORGANIZATIONS[org_key]
org_name = org_config["name"]
org_full_name = org_config["full_name"]
org_year = org_config["year"]
color_primary = org_config["color_primary"]
color_secondary = org_config["color_secondary"]

# Data file loading
st.sidebar.subheader("Data Management")

# Construct expected filename
expected_filename = f"{org_name}_{org_year}.csv"
file_status = "✅ File found" if os.path.exists(expected_filename) else "❌ File not found"
st.sidebar.info(f"Looking for: `{expected_filename}` \n {file_status}")

# Options to load data
data_source = st.sidebar.radio(
    "Data Source",
    options=["Use Default File", "Upload CSV File"],
    help="Choose how to load the data"
)

data_loaded = False
data = None

if data_source == "Use Default File":
    if os.path.exists(expected_filename):
        try:
            data = pd.read_csv(expected_filename)
            data_loaded = True
            st.sidebar.success(f"Loaded: {expected_filename}")
        except Exception as e:
            st.sidebar.error(f"Error loading {expected_filename}: {e}")
    else:
        st.sidebar.warning(f"{expected_filename} not found in project root")
else:
    uploaded_file = st.sidebar.file_uploader(
        "Upload CSV File",
        type='csv',
        help="Upload a CSV file with GitHub activity data"
    )
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
            data_loaded = True
            st.sidebar.success(f"Loaded: {uploaded_file.name}")
        except Exception as e:
            st.sidebar.error(f"Error loading file: {e}")

# Data preview in sidebar
if data_loaded and data is not None:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Data Preview")
    st.sidebar.write(f"**Rows:** {len(data)}")
    st.sidebar.write(f"**Columns:** {len(data.columns)}")
    
    with st.sidebar.expander("View Columns"):
        st.write(data.columns.tolist())

st.sidebar.markdown("---")
st.sidebar.subheader("About")
st.sidebar.markdown(f"""
**Organization:** {org_full_name}  
**Year:** {org_year}  
**Description:** {org_config['description']}
""")

# ===== MAIN CONTENT =====

# Custom CSS with dynamic colors
st.markdown(f"""
    <style>
        .metric-card {{
            background: linear-gradient(135deg, {color_primary} 0%, {color_secondary} 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
        }}
        .metric-value {{
            font-size: 32px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .metric-label {{
            font-size: 14px;
            opacity: 0.9;
        }}
    </style>
""", unsafe_allow_html=True)

# Main title
col1, col2 = st.columns([3, 1])
with col1:
    st.title(f"{org_full_name} GitHub Analytics")
    st.markdown(f"Comprehensive GitHub activity analysis and insights - {org_year} Yearly Recap")
with col2:
    st.markdown("")

st.markdown("---")

# Display banner image if it exists
banner_path = "banner.jpeg"
if os.path.exists(banner_path):
    st.image(banner_path, use_column_width=True)
    st.markdown("---")

# Show message if no data loaded
if not data_loaded:
    st.warning("No data loaded. Please configure the data source in the sidebar to begin analysis.")
    st.info("""
    ### How to use:
    1. Select your organization from the sidebar
    2. Choose a data source (default file or upload)
    3. The file should be named: `{organization_name}_{year}.csv`
    4. Expected columns:
       - `timestamp`: Event timestamp
       - `embeds.0.title`: Event title
       - `embeds.0.author.name`: Author name
       - `embeds.0.author.url`: Author URL
    """)
else:
    # Data processing and analysis
    with st.spinner('Loading and processing data...'):
        # Calculate all metrics
        total_active_days = totalActiveDays(data)
        longest_gap, gap_start_date, gap_end_date = longestGap(data)
        busiest_day, busiest_day_count = busiestDay(data)
        longest_streak, streak_start_date, streak_end_date = longestStreak(data)
        month_wise_activity = monthWiseActivity(data)
        time_wise_activity = timeWiseActivity(data)
        developer_activity, most_active_developer = allDeveloperActivity(data)
        repo_activity_dict, stars, issues_opened, issues_resolved, pr_opened, pr_closed, commits, branches, forks, actions_success, action_failures, new_collaborator, comments = repoActivity(data)
        
        # New metrics
        top_repos = getTopRepositories(repo_activity_dict, limit=10)
        commit_frequency = getCommitFrequency(data)
        hourly_activity = getActivityByHour(data)
        daily_activity = getActivityCalendar(data)
        contributor_stats = getContributorStats(data)

    # Add tabs for different views
    tab1, tab2, tab3 = st.tabs(["Overview", "Contributors", "Repositories"])
    
    with tab1:
        # Key metrics row 1
        st.markdown("### Key Metrics")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Active Days", f"{total_active_days}", delta=None)
        with col2:
            st.metric("Total Stars", f"{stars}", delta=None)
        with col3:
            st.metric("Pull Requests", f"{pr_opened + pr_closed}", delta=None)
        with col4:
            st.metric("Issues", f"{issues_opened + issues_resolved}", delta=None)
        with col5:
            st.metric("Commits", f"{commits}", delta=None)

        # Key metrics row 2
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Branches", f"{branches}", delta=None)
        with col2:
            st.metric("Forks", f"{forks}", delta=None)
        with col3:
            st.metric("Actions Success", f"{actions_success}", delta=None)
        with col4:
            st.metric("Action Failures", f"{action_failures}", delta=None)
        with col5:
            st.metric("Repositories", f"{len(repo_activity_dict)}", delta=None)

        st.markdown("---")

        # Activity Heatmap
        st.markdown("### Activity Heatmap")
        
        # Convert daily activity to DataFrame for heatmap
        activity_df = pd.DataFrame({
            'date': daily_activity.index,
            'activity': daily_activity.values
        })
        activity_df['date'] = pd.to_datetime(activity_df['date'])
        activity_df['week'] = activity_df['date'].dt.isocalendar().week
        activity_df['day'] = activity_df['date'].dt.day_name()
        activity_df['day_num'] = activity_df['date'].dt.dayofweek
        
        # Create heatmap
        heatmap_data = activity_df.pivot_table(
            values='activity', 
            index='day_num', 
            columns='week', 
            aggfunc='sum',
            fill_value=0
        )
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            y=[days[i] for i in heatmap_data.index],
            colorscale='Greens',
            showscale=True
        ))
        
        fig.update_layout(
            title="Activity Heatmap (Weekly View)",
            xaxis_title="Week",
            yaxis_title="Day of Week",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True, key="heatmap_overview")

        st.markdown("---")

        # Streaks and Gaps
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Longest Streaks")
            st.info(f"""
            **Streak Duration:** {longest_streak} days  
            **From:** {streak_start_date} to {streak_end_date}
            """)
        
        with col2:
            st.markdown("### Time Statistics")
            st.info(f"""
            **Longest Gap:** {longest_gap} days  
            **From:** {gap_start_date} to {gap_end_date}  
            **Busiest Day:** {busiest_day} ({busiest_day_count} events)
            """)

        st.markdown("---")

        # Activity Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Monthly Activity")
            month_wise_activity.index = month_wise_activity.index.astype(str)
            fig_month = px.bar(
                x=month_wise_activity.index, 
                y=month_wise_activity.values,
                labels={'x': 'Month', 'y': 'Activity Count'},
                color=month_wise_activity.values,
                color_continuous_scale='Blues'
            )
            fig_month.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_month, use_container_width=True, key="monthly_activity_tab1")
        
        with col2:
            st.markdown("### Activity by Hour")
            fig_hour = px.bar(
                x=hourly_activity.index,
                y=hourly_activity.values,
                labels={'x': 'Hour of Day', 'y': 'Activity Count'},
                color=hourly_activity.values,
                color_continuous_scale='Purples'
            )
            fig_hour.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_hour, use_container_width=True, key="hourly_activity_tab1")

        st.markdown("---")

        # Day of Week Distribution
        st.markdown("### Activity by Day of Week")
        fig_dow = px.bar(
            x=commit_frequency.index,
            y=commit_frequency.values,
            labels={'x': 'Day of Week', 'y': 'Activity Count'},
            color=commit_frequency.values,
            color_continuous_scale='Oranges'
        )
        fig_dow.update_layout(height=400)
        st.plotly_chart(fig_dow, use_container_width=True, key="day_of_week_overview")

        st.markdown("---")

        # Top Repositories
        st.markdown("### Top 10 Most Active Repositories")
        
        repo_names = [repo[0] for repo in top_repos]
        repo_activities = [sum(repo[1].values()) for repo in top_repos]
        
        repos_df = pd.DataFrame({
            'Repository': repo_names,
            'Activity': repo_activities
        })
        
        fig_repos = px.bar(
            repos_df,
            x='Activity',
            y='Repository',
            orientation='h',
            color='Activity',
            color_continuous_scale='Viridis'
        )
        fig_repos.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_repos, use_container_width=True, key="top_repos_overview")

        st.markdown("---")

        # Top Contributors
        st.markdown("### Top 10 Contributors")
        
        contributor_stats = getContributorStats(data)
        
        if contributor_stats is None or len(contributor_stats) == 0:
            st.info("No contributor data available or all contributors are unknown.")
        else:
            contrib_df = pd.DataFrame({
                'Contributor': contributor_stats.index,
                'Contributions': contributor_stats.values
            })
            
            fig_contrib = px.bar(
                contrib_df,
                x='Contributions',
                y='Contributor',
                orientation='h',
                color='Contributions',
                color_continuous_scale='Reds'
            )
            fig_contrib.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_contrib, use_container_width=True, key="top_contributors_overview")

        st.markdown("---")

        # Detailed Repository Stats
        st.markdown("### Repository Details (Top 10)")
        
        repo_details = []
        for repo_name, metrics in top_repos:
            repo_details.append({
                'Repository': repo_name,
                'Stars': metrics.get('stars', 0),
                'PRs': metrics.get('pr_opened', 0) + metrics.get('pr_closed', 0),
                'Issues': metrics.get('issues_opened', 0) + metrics.get('issues_resolved', 0),
                'Commits': metrics.get('commits', 0),
                'Forks': metrics.get('forks', 0),
                'Actions Success': metrics.get('actions_success', 0),
                'Branches': metrics.get('branches', 0)
            })
        
        repo_df = pd.DataFrame(repo_details)
        st.dataframe(repo_df, use_container_width=True)

        st.markdown("---")

        # Detailed Repository Stats - All Repositories
        st.markdown("### Repository Details (All Repositories)")
        
        # Create detailed stats for ALL repositories
        all_repo_details = []
        for repo_name, metrics in repo_activity_dict.items():
            all_repo_details.append({
                '#': len(all_repo_details) + 1,
                'Repository': repo_name,
                'Stars': metrics.get('stars', 0),
                'PRs': metrics.get('pr_opened', 0) + metrics.get('pr_closed', 0),
                'Issues': metrics.get('issues_opened', 0) + metrics.get('issues_resolved', 0),
                'Commits': metrics.get('commits', 0),
                'Forks': metrics.get('forks', 0),
                'Branches': metrics.get('branches', 0),
                'Actions Success': metrics.get('actions_success', 0),
                'Actions Failed': metrics.get('action_failures', 0),
                'Comments': metrics.get('comments', 0),
                'Collaborators': metrics.get('new_collaborator', 0)
            })
        
        all_repo_df = pd.DataFrame(all_repo_details)
        
        # Sorting options
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Sort by:**")
        with col2:
            sort_by = st.selectbox(
                "Sort repositories by",
                options=['Stars', 'Commits', 'PRs', 'Issues', 'Forks', 'Actions Success'],
                label_visibility="collapsed",
                key="sort_by_tab1"
            )
        
        # Sort the dataframe
        all_repo_df_sorted = all_repo_df.sort_values(by=sort_by, ascending=False).reset_index(drop=True)
        all_repo_df_sorted['#'] = range(1, len(all_repo_df_sorted) + 1)
        
        # Pagination
        items_per_page = st.selectbox(
            "Repositories per page",
            options=[10, 20, 50, 100, len(all_repo_df_sorted)],
            index=0,
            key="items_per_page_tab1"
        )
        
        # Calculate pagination
        total_pages = (len(all_repo_df_sorted) + items_per_page - 1) // items_per_page
        page = st.number_input(
            "Page",
            min_value=1,
            max_value=max(1, total_pages),
            value=1,
            key="page_number_tab1"
        )
        
        # Get data for current page
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        page_data = all_repo_df_sorted.iloc[start_idx:end_idx]
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Repositories", len(all_repo_df_sorted))
        with col2:
            st.metric("Total Pages", total_pages)
        with col3:
            st.metric("Current Page", page)
        with col4:
            st.metric("Repos on Page", len(page_data))
        
        # Display table
        st.dataframe(page_data, use_container_width=True, hide_index=True)
        
        # Export option
        csv = all_repo_df_sorted.to_csv(index=False)
        st.download_button(
            label="Download All Repositories as CSV",
            data=csv,
            file_name="all_repositories.csv",
            mime="text/csv",
            key="download_repos_tab1"
        )

        st.markdown("---")

        # Summary Statistics
        st.markdown("### Summary Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Repository Metrics")
            st.write(f"Total Repositories: **{len(repo_activity_dict)}**")
            st.write(f"Avg Stars per Repo: **{stars/len(repo_activity_dict) if len(repo_activity_dict) > 0 else 0:.1f}**")
            st.write(f"Avg Commits per Repo: **{commits/len(repo_activity_dict) if len(repo_activity_dict) > 0 else 0:.1f}**")
        
        with col2:
            st.markdown("#### Activity Metrics")
            st.write(f"Total Events: **{len(data)}**")
            st.write(f"Avg Events per Day: **{len(data)/total_active_days if total_active_days > 0 else 0:.1f}**")
            st.write(f"Most Active Day: **{commit_frequency.idxmax()}**")
        
        with col3:
            st.markdown("#### Action Metrics")
            success_rate = (actions_success / (actions_success + action_failures) * 100) if (actions_success + action_failures) > 0 else 0
            st.write(f"Action Success Rate: **{success_rate:.1f}%**")
            st.write(f"Total Actions: **{actions_success + action_failures}**")
            st.write(f"PR Merge Rate: **{pr_closed / (pr_opened + pr_closed) * 100 if (pr_opened + pr_closed) > 0 else 0:.1f}%**")

    with tab2:
        st.markdown("### Contributor Analytics")
        
        # Get all unique contributors
        all_contributors = data['embeds.0.author.name'].dropna().unique().tolist()
        all_contributors = [c for c in all_contributors if c.strip().lower() not in ['unknown', 'nan', '']]
        all_contributors = sorted(all_contributors)
        
        if len(all_contributors) == 0:
            st.warning("No contributors found in the data.")
        else:
            # Contributor selector
            st.subheader("Select Contributor")
            selected_contributor = st.selectbox(
                "Choose a contributor to view their contribution details",
                options=all_contributors,
                help="Select a contributor to see their activity and statistics"
            )
            
            if selected_contributor:
                # Get contributor details
                contributor_info = getContributorDetails(data, selected_contributor)
                
                if contributor_info:
                    st.markdown("---")
                    st.markdown(f"### {selected_contributor} - Contribution Profile")
                    
                    # Display contributor metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Activities", contributor_info['total_activities'])
                    with col2:
                        st.metric("Repositories", len(contributor_info['repositories_contributed']))
                    with col3:
                        if contributor_info['most_active_day']:
                            st.metric("Most Active Day", contributor_info['most_active_day'])
                    with col4:
                        if contributor_info['most_active_hour'] is not None:
                            st.metric("Most Active Hour", f"{contributor_info['most_active_hour']}:00")
                    
                    st.markdown("---")
                    
                    # Activity type breakdown
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Activity Type Breakdown")
                        activity_breakdown = contributor_info['activity_type_breakdown']
                        
                        if activity_breakdown:
                            activity_df = pd.DataFrame({
                                'Activity Type': list(activity_breakdown.keys()),
                                'Count': list(activity_breakdown.values())
                            })
                            
                            fig_activity = px.pie(
                                activity_df,
                                values='Count',
                                names='Activity Type',
                                title=f"{selected_contributor}'s Activity Distribution"
                            )
                            st.plotly_chart(fig_activity, use_container_width=True, key=f"activity_breakdown_{selected_contributor}")
                    
                    with col2:
                        st.subheader("Repositories Contributed To")
                        if contributor_info['repositories_contributed']:
                            repos_df = pd.DataFrame({
                                'Repository': contributor_info['repositories_contributed']
                            })
                            st.dataframe(repos_df, use_container_width=True, hide_index=True)
                        else:
                            st.info("No repository data available")
                    
                    st.markdown("---")
                    
                    # Activity timeline
                    st.subheader("Recent Activities Timeline")
                    timeline_data = getContributorTimeline(data, selected_contributor, limit=20)
                    
                    if len(timeline_data) > 0:
                        # Format timeline data for display
                        display_data = timeline_data.copy()
                        display_data['timestamp'] = pd.to_datetime(display_data['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
                        display_data.columns = ['Date & Time', 'Activity', 'URL']
                        
                        st.dataframe(display_data, use_container_width=True, hide_index=True)
                        
                        # Timeline chart
                        timeline_for_chart = timeline_data.copy()
                        timeline_for_chart['timestamp'] = pd.to_datetime(timeline_for_chart['timestamp'])
                        timeline_for_chart['date'] = timeline_for_chart['timestamp'].dt.date
                        activity_by_date = timeline_for_chart.groupby('date').size().reset_index(name='count')
                        
                        fig_timeline = px.bar(
                            activity_by_date,
                            x='date',
                            y='count',
                            title=f"{selected_contributor}'s Activity Over Time",
                            labels={'date': 'Date', 'count': 'Number of Activities'}
                        )
                        st.plotly_chart(fig_timeline, use_container_width=True, key=f"timeline_{selected_contributor}")
        
        st.markdown("---")
    
    with tab3:
        st.markdown("### Top 10 Most Active Repositories")
        
        repo_names = [repo[0] for repo in top_repos]
        repo_activities = [sum(repo[1].values()) for repo in top_repos]
        
        repos_df = pd.DataFrame({
            'Repository': repo_names,
            'Activity': repo_activities
        })
        
        fig_repos = px.bar(
            repos_df,
            x='Activity',
            y='Repository',
            orientation='h',
            color='Activity',
            color_continuous_scale='Viridis'
        )
        fig_repos.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_repos, use_container_width=True, key="top_repos_tab3")

        st.markdown("---")

        # Detailed Repository Stats
        st.markdown("### Repository Details (Top 10)")
        
        repo_details = []
        for repo_name, metrics in top_repos:
            repo_details.append({
                'Repository': repo_name,
                'Stars': metrics.get('stars', 0),
                'PRs': metrics.get('pr_opened', 0) + metrics.get('pr_closed', 0),
                'Issues': metrics.get('issues_opened', 0) + metrics.get('issues_resolved', 0),
                'Commits': metrics.get('commits', 0),
                'Forks': metrics.get('forks', 0),
                'Actions Success': metrics.get('actions_success', 0),
                'Branches': metrics.get('branches', 0)
            })
        
        repo_df = pd.DataFrame(repo_details)
        st.dataframe(repo_df, use_container_width=True)

        st.markdown("---")

        # Detailed Repository Stats - All Repositories
        st.markdown("### Repository Details (All Repositories)")
        
        # Create detailed stats for ALL repositories
        all_repo_details = []
        for repo_name, metrics in repo_activity_dict.items():
            all_repo_details.append({
                '#': len(all_repo_details) + 1,
                'Repository': repo_name,
                'Stars': metrics.get('stars', 0),
                'PRs': metrics.get('pr_opened', 0) + metrics.get('pr_closed', 0),
                'Issues': metrics.get('issues_opened', 0) + metrics.get('issues_resolved', 0),
                'Commits': metrics.get('commits', 0),
                'Forks': metrics.get('forks', 0),
                'Branches': metrics.get('branches', 0),
                'Actions Success': metrics.get('actions_success', 0),
                'Actions Failed': metrics.get('action_failures', 0),
                'Comments': metrics.get('comments', 0),
                'Collaborators': metrics.get('new_collaborator', 0)
            })
        
        all_repo_df = pd.DataFrame(all_repo_details)
        
        # Sorting options
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**Sort by:**")
        with col2:
            sort_by = st.selectbox(
                "Sort repositories by",
                options=['Stars', 'Commits', 'PRs', 'Issues', 'Forks', 'Actions Success'],
                label_visibility="collapsed",
                key="sort_by_tab3"
            )
        
        # Sort the dataframe
        all_repo_df_sorted = all_repo_df.sort_values(by=sort_by, ascending=False).reset_index(drop=True)
        all_repo_df_sorted['#'] = range(1, len(all_repo_df_sorted) + 1)
        
        # Pagination
        items_per_page = st.selectbox(
            "Repositories per page",
            options=[10, 20, 50, 100, len(all_repo_df_sorted)],
            index=0,
            key="items_per_page_tab3"
        )
        
        # Calculate pagination
        total_pages = (len(all_repo_df_sorted) + items_per_page - 1) // items_per_page
        page = st.number_input(
            "Page",
            min_value=1,
            max_value=max(1, total_pages),
            value=1,
            key="page_number_tab3"
        )

        # Get data for current page
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        page_data = all_repo_df_sorted.iloc[start_idx:end_idx]
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Repositories", len(all_repo_df_sorted))
        with col2:
            st.metric("Total Pages", total_pages)
        with col3:
            st.metric("Current Page", page)
        with col4:
            st.metric("Repos on Page", len(page_data))
        
        # Display table
        st.dataframe(page_data, use_container_width=True, hide_index=True)
        
        # Export option
        csv = all_repo_df_sorted.to_csv(index=False)
        st.download_button(
            label="Download All Repositories as CSV",
            data=csv,
            file_name="all_repositories.csv",
            mime="text/csv",
            key="download_repos_tab3"
        )

    st.markdown("---")
    
    # Footer with organization info
    st.markdown(f"""
    <div style="text-align: center; padding: 20px; color: gray;">
    {org_full_name} - GitHub Analytics Dashboard | {org_name} {org_year} Yearly Recap | Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    </div>
    """, unsafe_allow_html=True)