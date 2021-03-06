import os
import json
from utilities import get_csv_contents, write_data_to_csv_file, convert_str_to_dict

class RepoActiveness:

    def __init__(self):
        self.issues_per_month = []
        self.commits_per_month = []
        self.combined_activities = []
    

    def find_commits_per_month(self):
        input_filename = 'tensorflow_commits.csv'
        contents = get_csv_contents(os.path.join('commits-issues', input_filename))
        contents = convert_str_to_dict(contents)

        for content in contents:
            if content['committer_commit_date']:
                year_month_day = content['committer_commit_date'].split("T")[0]
                year_month = year_month_day.split("-")[0]+'-'+year_month_day.split("-")[1]
                
                year_month_already_included = False

                for month in self.commits_per_month:
                    if month[0] == year_month:
                        month[1] = int(month[1]) + 1
                        year_month_already_included = True
                        break
                
                if year_month_already_included is False:
                    self.commits_per_month.append([year_month, 1])

        self.commits_per_month.sort(key = lambda x: x[0], reverse=True)

        output_filename = os.path.join('per-month-commits', 'per_month_'+input_filename)
        write_data_to_csv_file(output_filename, self.commits_per_month)
        
        # print(['month', 'commits'])
        # for item in self.commits_per_month:
        #     print(item)
        
        

    def issue_opened_per_month(self):
        input_filename = 'react_issues.csv'
        contents = get_csv_contents(os.path.join('commits-issues', input_filename))
        contents = convert_str_to_dict(contents)

        for content in contents:
            if content['created_at']:
                year_month_day = content['created_at'].split("T")[0]
                year_month = year_month_day.split("-")[0]+'-'+year_month_day.split("-")[1]
                
                year_month_already_included = False

                for month in self.issues_per_month:
                    if month[0] == year_month:
                        month[1] = int(month[1]) + 1
                        year_month_already_included = True
                        break
                
                
                if year_month_already_included is False:
                    self.issues_per_month.append([str(year_month), 1])

        self.issues_per_month.sort(key = lambda x: x[0])
        
        output_filename = os.path.join('per-month-commits', 'per_month_'+input_filename)
        write_data_to_csv_file(output_filename, self.issues_per_month)
        
        
        # print(['month', 'issues'])
        # for item in self.issues_per_month:
        #     print(item)
        

    def combine_commits_issues(self):
        self.find_commits_per_month()
        self.issue_opened_per_month()

        for commit in self.commits_per_month:
            month = commit[0]

            for issue in self.issues_per_month:
                if issue[0] == month:
                    self.combined_activities.append([str(month), commit[1], issue[1]])
                    break
            
        print(len(self.combined_activities))
        for activity in self.combined_activities:
            print(activity)
        
