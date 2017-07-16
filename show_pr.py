"""
Search for and jump to a PR on bitbucket in sublime.
"""
import sublime
import sublime_plugin

import json
import webbrowser
import requests


SHOWPR_SETTINGS = "show_pr.sublime-settings"
URL = "https://api.bitbucket.org/2.0/repositories/{}/{}/pullrequests"


def load_creds():
    user = sublime.load_settings(SHOWPR_SETTINGS).get("user")
    password = sublime.load_settings(SHOWPR_SETTINGS).get("password")
    return user, password


def load_repositories():
    repo = sublime.load_settings(SHOWPR_SETTINGS).get("repos")
    if isinstance(repo, str):
        return [repo]
    return repo


def load_organization():
    return sublime.load_settings(SHOWPR_SETTINGS).get("organization")


def get_prs(org, repo, creds):
    """
    Gets PRs for repository for specific organization.
    Uses 'creds' credentials.
    """
    user, password = creds
    url = URL.format(org, repo)
    v = requests.get(url, auth=requests.auth.HTTPBasicAuth(user, password))
    if v.status_code != 200:
        return [["Problem with obtaining a response from bitbucket."]]
    resp = json.loads(v.text)
    output = []
    for i, val in enumerate(resp['values']):
        output.append([
            str(i),
            val['title'],
            val['author']['username'],
            val['links']['html']['href']
        ])
    return output


def format_output(output):
    """
    output is a list of lists. Every list has the
    same number of elements which are the columns.
    """
    columns = zip(*output)
    mxs = [max(map(len, column)) for column in columns]
    lines = []
    for row in output:
        line = ""
        for i, col in enumerate(row):
            line += col
            line += (mxs[i] - len(col) + 4) * " "
        lines.append(line.strip())
    return lines


class ShowPrCommand(sublime_plugin.TextCommand):

    def _handle_input(self, inp):
        values = inp.split(":")
        if len(values) == 0:
            return None, None
        elif len(values) == 1:
            org = load_organization()
            return org, inp
        else:
            return values[:2]

    def process_command(self, inp):
        organization, repo = self._handle_input(inp)
        if not organization:
            formatted_prs = [["Repository couldn't be found."]]
            return None, formatted_prs

        user, password = load_creds()
        if user is None or password is None:
            formatted_prs = [["Please specify both user and password in the config file."]]
            return None, formatted_prs

        prs = get_prs(organization, repo, load_creds())
        formatted_prs = format_output(prs)
        return prs, formatted_prs

    def run(self, edit):
        window = self.view.window()

        def input_panel_closed(inp):
            """
            When input panel is closed
            ask bitbucket for PRs and
            show quick panel to display them.
            """
            prs, formatted_prs = self.process_command(inp)

            def quick_panel_closed(selection):
                if selection < 0:
                    return
                if prs:
                    webbrowser.open(prs[selection][-1])

            window.show_quick_panel(
                formatted_prs,
                quick_panel_closed,
                sublime.MONOSPACE_FONT,
                0,
            )

        # search window
        window.show_input_panel(
            "Repository:",
            load_repositories()[0],
            input_panel_closed,
            None, None
        )
