#!/usr/bin/env python3
from sys import argv
with open(argv[1]) as file: 
    content=file.readlines()
    result=""
    question=0
    for lineNo,line in enumerate(content[1:-1]):
        print(line)
        if line.strip()=="": continue
        elif line[0] in "0123456789":
            if ")" in line:
                parenthesis=line.split(")")
                if "(" not in parenthesis[0]:
                    result+=((f"    <label><input  type=\"radio\" name=\"{question}\" value=\" \" checked/> Empty.</label>\n</fieldset>\n" if question!=0 else "")+f"<fieldset>\n    <legend>Question {parenthesis[0]}</legend>\n    <p>"+line[len(parenthesis[0])+1:].strip()+"</p>\n")
                    question+=1
        elif line[0] in "ABCDE" and line[1]==")":
            result+=(f"    <label><input type=\"radio\" name=\"{question}\" value=\"{line[0]}\"/> "+line[2:].strip()+"</label>\n")
        else:
            result+="    <p>"+line.strip()+"</p>\n"
    html=f"""<!DOCTYPE html>
<!-- This document automatically generated with Examination by Elagoht -->
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="design.css">
    <title>Examination</title>
</head>
<script>
    const answerKey="{content[-1].strip().upper()}"
</script>
<body>
    <header>
        <h1>"""+content[0].strip()+"""</h1>
        <nav id="question-selector">
            """+"\n            ".join([f"""<input type="button" class="qstn-sel" onclick="showQ({i})" value="{i+1}"/>""" for i in range(question)])+"""
    <input id="prev-question" type="button" value="&#8656;" onclick="prevQ()">
    <input id="next-question" type="button" value="&#8658;" onclick="nextQ()">
    <input id="finish" type="submit" value="Sınavı Bitir" onclick="promptToFinish()">
        </nav>
    <header>
    <section>
"""+result+f"""    <label><input type=\"radio\" name=\"{question}\" value=\" \"/ checked> Empty.</label>\n</fieldset>
    </section>
    <footer>
    </footer>
    <div id="confirm">
            <p>Are you sure you want to finish your exam?</p>
        <div id="quit-buttons">
            <button id="quit" onclick="doFinishExam(true)">Yes, I want to finish.</button>
            <button id="dont-quit" onclick="doFinishExam(false)">No, I'll keep solving.</button>
        <div>
    </div>
</body> 
<script src="/behaviour.js"></script>
</html>"""
with open(argv[2],"w",encoding="UTF-8") as file: file.write(html)
