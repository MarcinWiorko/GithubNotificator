from string import Template

from github_notificator.models.results import Discussion, ReadyForMerge, ReadyForReview, ToTested
from github_notificator.view.html_generator import HTMLGenerator


class TestHTMLGenerator:
    html_template = Template("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>Github Notificator</title>
            <style>
                body {
                    background-color: rgb(20, 40, 60);
                    color: rgb(240, 248, 255);
                    font-family: "Helvetica", "Arial", sans-serif;
                    font-size: 1.3em;
                }
                
                a {
                    color: rgb(255, 111, 111);
                }
                
                .tooltip {
                  position: relative;
                  display: inline-block;
                  border-bottom: 1px dotted black;
                }
                
                .tooltip .tooltiptext {
                  visibility: hidden;
                  width: 120px;
                  background-color: black;
                  color: #fff;
                  text-align: center;
                  border-radius: 6px;
                  padding: 5px 0;
                  
                  /* Position the tooltip */
                  position: absolute;
                  z-index: 1;
                  top: -5px;
                  left: 105%;
                }
                
                .tooltip:hover .tooltiptext {
                  visibility: visible;
                }
            </style>
        </head>
    <body>
        <h1>Github Notificator</h1>
        $body
    </body
    </html>
    """)

    def test_generate_html_for_discussion(self) -> None:
        discussion = Discussion("repo", "title", "pr_link", "discussion_to_resolve_link")
        ready_for_merge = ReadyForMerge("repo2", "title2", "pr_link2", ("succeed", "completed"))
        ready_for_review = ReadyForReview("repo2", "title2", "pr_link2")
        to_tested = ToTested("repo2", "title2", "pr_link2")
        html_generator = HTMLGenerator()
        expected_results = \
        """<p>🗣️To discuss: repo <a href='pr_link'>title</a>&nbsp;<a href='discussion_to_resolve_link'>Discussion</a></p>
		<p>😎 To merge: repo2 <a href='pr_link2'>title2</a>&nbsp;<span class="tooltip">Main branch: 🟢\
<span class="tooltiptext">succeed completed</span></span></p>
		<p>👀 To review: repo2 <a href='pr_link2'>title2</a></p>
		<p>🧪 To test: repo2 <a href='pr_link2'>title2</a></p>"""
        # print(html_generator.generate_html([discussion, ready_for_merge, ready_for_review, to_tested]))
        # print(self.html_template.substitute({"body": expected_results}))
        assert html_generator.generate_html(
            [discussion, ready_for_merge, ready_for_review, to_tested]) == self.html_template.substitute(
            {"body": expected_results})
