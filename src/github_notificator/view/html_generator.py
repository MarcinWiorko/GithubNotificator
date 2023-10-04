"""
File contains logic to render html with results
"""
import os
import webbrowser
from string import Template

from github_notificator.models.results import Result


class HTMLGenerator:
    """Class for generate html"""

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

    def generate_html(self, results: list[Result]) -> str:
        """ Generate html """
        results_html = "\n\t\t".join([result.get_paragraph_html() for result in results])
        return self.html_template.substitute({"body": results_html})

    def open_generated_html(self, results: list[Result]) -> None:
        with open("resul.html", 'w') as f:
            f.write(self.generate_html(results))
        webbrowser.open(f'file://{os.path.realpath(f.name)}')
