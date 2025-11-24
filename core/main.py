import pandas as pd
import numpy as np


def clean_data(path):
    data = pd.read_csv(path)
    # data.drop(["author.bot", "author.avatar", "author.discriminator", "author.global_name", "author.id", "author.username", "call", "channel_id", "components", "content", "edited_timestamp", "embeds.0.author.icon_url", "embeds.0.author.proxy_icon_url", "embeds.0.color", "embeds.0.content_scan_version", "embeds.0.type",
    #           "flags", "interaction", "mention_everyone", "mentions", "message_reference", "nonce", "pinned", "position", "reactions", "referenced_message", "resolved", "role_subscription_data", "sticker_items", "stickers", "thread", "tts", "type", "userName", "webhook_id", "mention_channels"], axis=1, inplace=True)
    # # Select columns from index 10 to 56 (inclusive)
    # cols_to_drop = data.columns[8:57]
    # data.drop(cols_to_drop, axis=1, inplace=True)
    return data


def totalActiveDays(data):
    data['timestamp'] = pd.to_datetime(
        data['timestamp'], format='ISO8601', errors='coerce')
    data['date'] = pd.to_datetime(data['timestamp']).dt.date

    data = data.dropna(subset=['date'])
    unique_dates = data['date'].unique()
    print(f"Total Active Days: {len(unique_dates)}")
    return len(unique_dates)


def longestGap(data):
    longestGap = 0
    gap = 0
    start_date = None
    end_date = None

    data['timestamp'] = pd.to_datetime(
        data['timestamp'], format='ISO8601', errors='coerce')
    data['date'] = pd.to_datetime(data['timestamp']).dt.date

    data = data.dropna(subset=['date'])
    unique_dates = sorted(data['date'].unique())

    for i in range(1, len(unique_dates)):
        current_gap = (unique_dates[i] - unique_dates[i - 1]).days - 1
        if current_gap > 0:
            gap = current_gap
            if gap > longestGap:
                longestGap = gap
                start_date = unique_dates[i - 1]
                end_date = unique_dates[i]
        else:
            gap = 0

    print(f"Longest Gap: {longestGap}")
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")

    return [longestGap, start_date, end_date]


def busiestDay(data):
    data['timestamp'] = pd.to_datetime(
        data['timestamp'], format='ISO8601', errors='coerce')
    data['date'] = pd.to_datetime(data['timestamp']).dt.date
    busiest_day = data['date'].value_counts().idxmax()
    busiest_day_count = data['date'].value_counts().max()
    print(f"Busiest Day: {busiest_day}")
    print(f"Total Messages: {busiest_day_count}")
    return [busiest_day, busiest_day_count]


def longestStreak(data):
    longestStreak = 0
    streak = 0

    data['timestamp'] = pd.to_datetime(
        data['timestamp'], format='ISO8601', errors='coerce')
    data['date'] = pd.to_datetime(data['timestamp']).dt.date

    data = data.dropna(subset=['date'])
    unique_dates = sorted(data['date'].unique())

    for i in range(1, len(unique_dates)):
        if (unique_dates[i] - unique_dates[i - 1]).days == 1:
            if streak == 0:
                temp_start_date = unique_dates[i - 1]
            streak += 1
        else:
            if streak > longestStreak:
                longestStreak = streak
                start_date = temp_start_date
                end_date = unique_dates[i - 1]
            streak = 0
            temp_start_date = None

    if streak > longestStreak:
        longestStreak = streak
        start_date = temp_start_date
        end_date = unique_dates[-1]

    print(f"Longest Streak: {longestStreak}")
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")

    return [longestStreak, start_date, end_date]


def monthWiseActivity(data):
    data['timestamp'] = pd.to_datetime(
        data['timestamp'], format='ISO8601', errors='coerce')
    data['month'] = pd.to_datetime(data['timestamp']).dt.to_period('M')
    month_wise_activity = data.groupby('month').size()
    print(month_wise_activity)
    return month_wise_activity


def timeWiseActivity(data):
    data['timestamp'] = pd.to_datetime(
        data['timestamp'], format='ISO8601', errors='coerce')
    data['hour'] = pd.to_datetime(data['timestamp']).dt.hour
    time_wise_activity = data.groupby('hour').size()
    time_wise_activity = time_wise_activity.groupby(
        pd.cut(time_wise_activity.index, np.arange(0, 25, 4))).sum()
    print(time_wise_activity)
    return time_wise_activity


def allDeveloperActivity(data):
    developer_activity = {}

    data['embeds.0.author.url'] = data['embeds.0.author.url'].fillna('')

    for url in data['embeds.0.author.url']:
        if url != '':
            dev_name = url.split('/')[-1]
            if dev_name in developer_activity:
                developer_activity[dev_name] += 1
            else:
                developer_activity[dev_name] = 1

    developer_activity = dict(
        sorted(developer_activity.items(), key=lambda item: item[1], reverse=True))
    for key, value in developer_activity.items():
        print(f"{key}: {value}")
    print("Most Active Developer: ", list(developer_activity.keys())[0])

    return [developer_activity, list(developer_activity.keys())[0]]


def repoActivity(data):
    repo_activity = {}
    data['embeds.0.title'] = data['embeds.0.title'].fillna('')
    stars, issues_opened, issues_resolved, pr_opened, pr_closed, commits, branches, forks, actions_success, action_failures, new_collaborator, comments = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    for title in data['embeds.0.title']:
        if title != '':
            if ('New star added' in title):
                stars += 1
                repoName = title.split(']')[0].split('/')[1]
                if repoName in repo_activity:
                    repo_activity[repoName]['stars'] += 1
                else:
                    repo_activity[repoName] = {'stars': 1, 'issues_opened': 0, 'issues_resolved': 0, 'pr_opened': 0, 'pr_closed': 0, 'commits': 0,
                                               'branches': 0, 'forks': 0, 'actions_success': 0, 'action_failures': 0, 'new_collaborator': 0, 'comments': 0}
            elif ('New collaborator added' in title):
                new_collaborator += 1
                repoName = title.split(']')[0].split('/')[1]
                if repoName in repo_activity:
                    repo_activity[repoName]['new_collaborator'] += 1
                else:
                    repo_activity[repoName] = {'stars': 0, 'issues_opened': 0, 'issues_resolved': 0, 'pr_opened': 0, 'pr_closed': 0, 'commits': 0,
                                               'branches': 0, 'forks': 0, 'actions_success': 0, 'action_failures': 0, 'new_collaborator': 1, 'comments': 0}
            elif ('New branch created' in title):
                branches += 1
                repoName = title.split(']')[0].split('/')[1]
                if repoName in repo_activity:
                    repo_activity[repoName]['branches'] += 1
                else:
                    repo_activity[repoName] = {'stars': 0, 'issues_opened': 0, 'issues_resolved': 0, 'pr_opened': 0, 'pr_closed': 0, 'commits': 0,
                                               'branches': 1, 'forks': 0, 'actions_success': 0, 'action_failures': 0, 'new_collaborator': 0, 'comments': 0}
            elif ('New comment on' in title):
                comments += 1
                repoName = title.split(']')[0].split('/')[1]
                if repoName in repo_activity:
                    repo_activity[repoName]['comments'] += 1
                else:
                    repo_activity[repoName] = {'stars': 0, 'issues_opened': 0, 'issues_resolved': 0, 'pr_opened': 0, 'pr_closed': 0, 'commits': 0,
                                               'branches': 0, 'forks': 0, 'actions_success': 0, 'action_failures': 0, 'new_collaborator': 0, 'comments': 1}
            elif ('New review comment' in title):
                comments += 1
                repoName = title.split(']')[0].split('/')[1]
                if repoName in repo_activity:
                    repo_activity[repoName]['comments'] += 1
                else:
                    repo_activity[repoName] = {'stars': 0, 'issues_opened': 0, 'issues_resolved': 0, 'pr_opened': 0, 'pr_closed': 0, 'commits': 0,
                                               'branches': 0, 'forks': 0, 'actions_success': 0, 'action_failures': 0, 'new_collaborator': 0, 'comments': 1}
            elif ('Fork created' in title):
                forks += 1
                repoName = title.split(']')[0].split('/')[1]
                if repoName in repo_activity:
                    repo_activity[repoName]['forks'] += 1
                else:
                    repo_activity[repoName] = {'stars': 0, 'issues_opened': 0, 'issues_resolved': 0, 'pr_opened': 0, 'pr_closed': 0, 'commits': 0,
                                               'branches': 0, 'forks': 1, 'actions_success': 0, 'action_failures': 0, 'new_collaborator': 0, 'comments': 0}

            elif ('Issue opened' in title):
                issues_opened += 1
                repoName = title.split(']')[0].split('/')[1]
                if repoName in repo_activity:
                    repo_activity[repoName]['issues_opened'] += 1
                else:
                    repo_activity[repoName] = {'stars': 0, 'issues_opened': 1, 'issues_resolved': 0, 'pr_opened': 0, 'pr_closed': 0, 'commits': 0,
                                               'branches': 0, 'forks': 0, 'actions_success': 0, 'action_failures': 0, 'new_collaborator': 0, 'comments': 0}
            elif ('Issue closed' in title):
                issues_resolved += 1
                repoName = title.split(']')[0].split('/')[1]
                if repoName in repo_activity:
                    repo_activity[repoName]['issues_resolved'] += 1
                else:
                    repo_activity[repoName] = {'stars': 0, 'issues_opened': 0, 'issues_resolved': 1, 'pr_opened': 0, 'pr_closed': 0, 'commits': 0,
                                               'branches': 0, 'forks': 0, 'actions_success': 0, 'action_failures': 0, 'new_collaborator': 0, 'comments': 0}
            elif ('GitHub Actions checks success' in title or 'commitlint success' in title or 'deploy-main success' in title or 'Deployed successfully' in title or 'create_commit success' in title or 'Lint Code Base success' in title):
                actions_success += 1
                repoName = title[1:title.index(']')]
                if repoName in repo_activity:
                    repo_activity[repoName]['actions_success'] += 1
                else:
                    repo_activity[repoName] = {'stars': 0, 'issues_opened': 0, 'issues_resolved': 0, 'pr_opened': 0, 'pr_closed': 0, 'commits': 0,
                                               'branches': 0, 'forks': 0, 'actions_success': 1, 'action_failures': 0, 'new_collaborator': 0, 'comments': 0}
            elif ('GitHub Actions checks failure' in title or 'commitlint failure' in title or 'deploy-main failure' in title or 'Deploy failed' in title or 'Deploy failure' in title or 'Lint Code Base failure' in title):
                action_failures += 1
                # here repo name is <name>
                repoName = title[1:title.index(']')]
                if repoName in repo_activity:
                    repo_activity[repoName]['action_failures'] += 1
                else:
                    repo_activity[repoName] = {'stars': 0, 'issues_opened': 0, 'issues_resolved': 0, 'pr_opened': 0, 'pr_closed': 0, 'commits': 0,
                                               'branches': 0, 'forks': 0, 'actions_success': 0, 'action_failures': 1, 'new_collaborator': 0, 'comments': 0}
            elif ('Pull request opened' in title):
                pr_opened += 1
                repoName = title.split(']')[0].split('/')[1]
                if repoName in repo_activity:
                    repo_activity[repoName]['pr_opened'] += 1
                else:
                    repo_activity[repoName] = {'stars': 0, 'issues_opened': 0, 'issues_resolved': 0, 'pr_opened': 1, 'pr_closed': 0, 'commits': 0,
                                               'branches': 0, 'forks': 0, 'actions_success': 0, 'action_failures': 0, 'new_collaborator': 0, 'comments': 0}
            elif ('Pull request closed' in title):
                pr_closed += 1
                repoName = title.split(']')[0].split('/')[1]
                if repoName in repo_activity:
                    repo_activity[repoName]['pr_closed'] += 1
                else:
                    repo_activity[repoName] = {'stars': 0, 'issues_opened': 0, 'issues_resolved': 0, 'pr_opened': 0, 'pr_closed': 1, 'commits': 0,
                                               'branches': 0, 'forks': 0, 'actions_success': 0, 'action_failures': 0, 'new_collaborator': 0, 'comments': 0}

            elif ('new commit' in title):
                repoName = title[1:].split(':')[0]
                val = int(title.split(' ')[1])
                commits += val
                if repoName in repo_activity:
                    repo_activity[repoName]['commits'] += val
                else:
                    repo_activity[repoName] = {'stars': 0, 'issues_opened': 0, 'issues_resolved': 0, 'pr_opened': 0, 'pr_closed': 0, 'commits': val,
                                               'branches': 0, 'forks': 0, 'actions_success': 0, 'action_failures': 0, 'new_collaborator': 0, 'comments': 0}
                    
    
                    
    print("Repository Activity")
    print("RepoName   Stars Issues PRs Commits Branches Forks Actions colab comments")
    c = 0
    for key, value in repo_activity.items():
        c += 1
        print(f"{c}: {key},{value}")
    print("Total Activity")
    print(f"Number of repositories", len(repo_activity.keys()))
    print(f"Stars: {stars}")
    print(f"Issues Opened: {issues_opened}")
    print(f"Issues Resolved: {issues_resolved}")
    print(f"Pull Requests Opened: {pr_opened}")
    print(f"Pull Requests Closed: {pr_closed}")
    print(f"Commits: {commits}")
    print(f"Branches: {branches}")
    print(f"Forks: {forks}")
    print(f"Actions: {actions_success}")
    print(f"Action Failures: {action_failures}")
    print(f"New Collaborator: {new_collaborator}")
    print(f"Comments: {comments}")

    return [repo_activity, stars, issues_opened, issues_resolved, pr_opened, pr_closed, commits, branches, forks, actions_success, action_failures, new_collaborator, comments]

def getTopRepositories(repo_activity, limit=10):
    """Get top repositories by activity"""
    sorted_repos = sorted(repo_activity.items(), 
                         key=lambda x: sum(x[1].values()), 
                         reverse=True)
    return sorted_repos[:limit]

def getCommitFrequency(data):
    """Get commit frequency by day of week"""
    data['timestamp'] = pd.to_datetime(data['timestamp'], format='ISO8601', errors='coerce')
    data['day_of_week'] = pd.to_datetime(data['timestamp']).dt.day_name()
    frequency = data['day_of_week'].value_counts().sort_index()
    return frequency

def getActivityByHour(data):
    """Get activity distribution by hour"""
    data['timestamp'] = pd.to_datetime(data['timestamp'], format='ISO8601', errors='coerce')
    data['hour'] = pd.to_datetime(data['timestamp']).dt.hour
    hourly = data['hour'].value_counts().sort_index()
    return hourly

def getActivityCalendar(data):
    """Get daily activity for heatmap"""
    data['timestamp'] = pd.to_datetime(data['timestamp'], format='ISO8601', errors='coerce')
    data['date'] = data['timestamp'].dt.date
    daily_activity = data.groupby('date').size()
    return daily_activity

def getMostActiveRepositories(repo_activity, limit=10):
    """Get most active repositories by type"""
    repos_with_types = {}
    for repo, metrics in repo_activity.items():
        total = sum(metrics.values())
        repos_with_types[repo] = total
    
    sorted_repos = sorted(repos_with_types.items(), key=lambda x: x[1], reverse=True)
    return sorted_repos[:limit]

def getContributorStats(data):
    """
    Get top contributors with proper filtering and cleaning.
    Removes 'Unknown' and bot accounts.
    """
    if 'embeds.0.author.name' not in data.columns:
        return pd.Series()
    
    # Create a copy to avoid modifying original
    author_data = data['embeds.0.author.name'].copy()
    
    # Fill NaN values but mark for removal
    author_data = author_data.fillna('')
    
    # Filter out empty strings and 'Unknown' entries
    author_data = author_data[
        (author_data.str.strip() != '') & 
        (author_data.str.lower() != 'unknown') &
        (author_data.str.lower() != 'nan')
    ]
    
    if len(author_data) == 0:
        return pd.Series()
    
    # Get value counts and take top 10
    contributors = author_data.value_counts().head(10)
    
    return contributors

def getContributorDetails(data, contributor_name):
    """
    Get detailed statistics for a specific contributor.
    
    Args:
        data (pd.DataFrame): Activity data
        contributor_name (str): Name of the contributor
        
    Returns:
        dict: Detailed contributor statistics
    """
    # Filter data for the contributor
    contributor_data = data[data['embeds.0.author.name'].str.lower() == contributor_name.lower()]
    
    if len(contributor_data) == 0:
        return None
    
    stats = {
        'name': contributor_name,
        'total_activities': len(contributor_data),
        'first_activity': contributor_data['timestamp'].min(),
        'last_activity': contributor_data['timestamp'].max(),
        'activity_type_breakdown': {},
        'monthly_activity': {},
        'most_active_day': None,
        'most_active_hour': None,
        'repositories_contributed': set()
    }
    
    # Parse timestamp
    contributor_data = contributor_data.copy()
    contributor_data['timestamp'] = pd.to_datetime(contributor_data['timestamp'], errors='coerce')
    
    # Activity type breakdown and repository extraction
    for _, row in contributor_data.iterrows():
        title = str(row.get('embeds.0.title', '')).lower()
        title_original = str(row.get('embeds.0.title', ''))
        
        # Extract repository name - improved logic
        repo_name = None
        
        # Try multiple extraction patterns
        if ' in ' in title_original:
            # Pattern: "Action in RepositoryName"
            parts = title_original.split(' in ')
            if len(parts) > 1:
                repo_name = parts[-1].strip()
        elif '/' in title_original:
            # Pattern: "RepositoryName/Action" or "org/repo"
            parts = title_original.split('/')
            if len(parts) >= 1:
                repo_name = parts[0].strip()
        elif ':' in title_original:
            # Pattern: "RepositoryName: Action"
            parts = title_original.split(':')
            if len(parts) > 0:
                repo_name = parts[0].strip()
        
        # Clean up repository name
        if repo_name and repo_name.lower() not in ['unknown', 'nan', '']:
            # Remove common action words from repo name
            action_words = ['opened', 'closed', 'merged', 'created', 'deleted', 'pushed', 'starred']
            for word in action_words:
                if repo_name.lower().startswith(word):
                    repo_name = repo_name[len(word):].strip()
            
            if repo_name and repo_name.lower() not in ['unknown', 'nan', '']:
                stats['repositories_contributed'].add(repo_name)
        
        # Activity type breakdown
        if 'star' in title:
            activity_type = 'Stars'
        elif 'pull request' in title:
            if 'opened' in title:
                activity_type = 'PRs Opened'
            elif 'closed' in title or 'merged' in title:
                activity_type = 'PRs Merged'
            else:
                activity_type = 'Pull Requests'
        elif 'issue' in title:
            if 'opened' in title:
                activity_type = 'Issues Opened'
            elif 'closed' in title:
                activity_type = 'Issues Closed'
            else:
                activity_type = 'Issues'
        elif 'commit' in title or 'push' in title:
            activity_type = 'Commits'
        elif 'fork' in title:
            activity_type = 'Forks'
        elif 'branch' in title:
            activity_type = 'Branches'
        elif 'comment' in title:
            activity_type = 'Comments'
        elif 'created' in title and 'repository' in title:
            activity_type = 'Repository Created'
        else:
            activity_type = 'Other'
        
        stats['activity_type_breakdown'][activity_type] = stats['activity_type_breakdown'].get(activity_type, 0) + 1
    
    # Monthly activity
    contributor_data['month'] = contributor_data['timestamp'].dt.to_period('M')
    monthly = contributor_data['month'].value_counts().sort_index()
    stats['monthly_activity'] = monthly.to_dict()
    
    # Most active day
    contributor_data['day'] = contributor_data['timestamp'].dt.day_name()
    day_counts = contributor_data['day'].value_counts()
    if len(day_counts) > 0:
        stats['most_active_day'] = day_counts.idxmax()
    
    # Most active hour
    contributor_data['hour'] = contributor_data['timestamp'].dt.hour
    hour_counts = contributor_data['hour'].value_counts()
    if len(hour_counts) > 0:
        stats['most_active_hour'] = int(hour_counts.idxmax())
    
    stats['repositories_contributed'] = sorted(list(stats['repositories_contributed']))
    
    return stats

def getContributorTimeline(data, contributor_name, limit=20):
    """
    Get recent activities timeline for a contributor.
    
    Args:
        data (pd.DataFrame): Activity data
        contributor_name (str): Name of the contributor
        limit (int): Number of recent activities to return
        
    Returns:
        pd.DataFrame: Recent activities
    """
    contributor_data = data[data['embeds.0.author.name'].str.lower() == contributor_name.lower()].copy()
    
    if len(contributor_data) == 0:
        return pd.DataFrame()
    
    contributor_data['timestamp'] = pd.to_datetime(contributor_data['timestamp'], errors='coerce')
    contributor_data = contributor_data.sort_values('timestamp', ascending=False).head(limit)
    
    return contributor_data[['timestamp', 'embeds.0.title', 'embeds.0.author.url']].reset_index(drop=True)

def main():
    # data=clean_data("data.csv")
    # data.to_csv("clean_data.csv",index=False)
    data = pd.read_csv("clean_data.csv")
    longestStreak(data)
    monthWiseActivity(data)
    totalActiveDays(data)
    longestGap(data)
    busiestDay(data)
    timeWiseActivity(data)
    allDeveloperActivity(data)
    repoActivity(data)


if __name__ == "__main__":
    main()
