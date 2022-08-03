#!/usr/bin/env python3
CSS="""* {
      margin:0;
      padding:0;
      box-sizing:border-box;
      transition:all .3s;
      font-family:sans-serif;
    } 
    body {
      margin:1rem auto;
      width:100%;
      max-width:1000px;
    }
    #question-selector {
      display:flex;
      flex-flow:wrap;
      justify-content:center;
    }
    nav input {
      min-width:2rem;
      height:2rem;
      padding:.5rem;
      margin:.2rem;
      border-radius:.2rem;
      display:flex;
      justify-content:center;
      align-items:center;
      border:1px solid #444;
      background-color:#eee;
    }
    .curr {
      outline:2px solid black;
    }
    legend {
      padding:.25rem;
      margin-left:.5rem;
      font-weight:bold;
    }
    fieldset {
      padding:1rem;
      margin:1rem 0;
      background-color:#eee;
      border-radius:.3rem;
      display:flex;
      flex-direction:column;
    }
    p {
      line-height: 1.5;
      text-align:inherit;
    }
    fieldset > p:last-of-type {
      font-weight:bold;
      text-align:justify;
    }
    label {
      width:100%;
      display:flex;
      padding:.25rem;
      align-items:center;
      cursor:pointer;
    } 
    input[type="radio"] {
      border-radius:100%;
      display:inline-block;
      margin-right:1rem;
      position:relative;
      min-width:2rem;
      max-width:2rem;
      height:2rem;
      cursor:pointer;
      -webkit-appearance:none;
    }
    input[type=radio]:after {
      border-radius:100%;
      top:-100%;
      left:0;
      content:'';
      width:100%;
      height:100%;
      display: block;
      position:relative;
      outline:.2rem solid #444;
      opacity:0;
      transition:all .3s;
    }
    input[type=radio]:checked:after {
      opacity:1;
    }
    input[type=radio]:before {
      content:' ';
      position:relative;
      display:flex;
      justify-content:center;
      align-items:center;
      font-size:1rem;
      width:100%;
      height:100%;
    }
    input[value=A]:before {content:"A)"}
    input[value=B]:before {content:"B)"}
    input[value=C]:before {content:"C)"}
    input[value=D]:before {content:"D)"}
    input[value=E]:before {content:"E)"}
    input[value=" "]:before {content:"X"}
    input[type=submit]:hover {
      background-image:linear-gradient(to top, #bba, #ddd)
    }
    .ticked {
      background-color:aqua;
    }
    .true {
      background-color:green;
    }
    .false {
      background-color:red;
    }
    .empty {
      background-color:gray;
    }
    #true-count {color:green;}
    #false-count {color:red;}
    #empty-count {color:gray;}
    #confirm {
      padding:.25rem;
      background-color:#eee;
      border-radius:.3rem;
      border:1px solid darkgray;
      display:none;
      flex-direction:column;
      width: 280px;
      text-align:center;
      position: fixed;
      left: calc(50% - 140px);
      top: calc(50vh - 107px);
    }
    #quit-buttons {
      display:flex;
      justify-content:flex-end;
    }
    #confirm button {
      margin:.25rem;
      color:white;
      border-radius:.3rem;
      border:1px solid darkgray;
      padding:.25rem;
    }
    #quit {
      background-color:red;
    }
    #dont-quit {
      background-color:green;
    }"""
JS="""const questions=Array.from(document.getElementsByTagName("fieldset"))
    const selectors=Array.from(document.getElementsByClassName("qstn-sel"))
    const confirmation=document.getElementById("confirm")
    const lenq=questions.length
    let answers=[]
    let curr=0
    let finished=false
    let asked=false
    const startTime=performance.now()
    questions.forEach(element=>{answers.push(" ")})
    const hideAll=()=>{
      questions.forEach(element=>{element.style.display="none"})
      selectors.forEach(element=>{element.classList.remove("curr")
      })
    }
    const showQ=(nth)=>{
      hideAll()
      questions[nth].style.display="flex"
      selectors[nth].classList.add("curr")
      curr=nth
    }
    const nextQ=()=>{
      if (curr<lenq-1) {curr++}
      else {curr=0}
      showQ(curr)
    }
    const prevQ=()=>{
      if (curr>0) {curr--}
      else {curr=lenq-1}
      showQ(curr)
    }
    const updateNavBar=(nth,val)=>{
      answers[nth]=val
      if (val!==" ") {
        selectors[nth].classList.add("ticked")
      } else {
        selectors[nth].classList.remove("ticked")
      }
    }
    const radios=Array.from(document.querySelectorAll("input[type=radio]"))
    radios.forEach(element=>{
      element.addEventListener("change",()=>{
        updateNavBar(element.name-1,element.value)
      })
    })
    const humanizeTime=(ms)=>{
      var floor=Math.floor,secs=floor(ms/1000),mins=floor(secs/60),hrs=floor(mins/60),result=""
      if (hrs>0) {result+=hrs%24 +" hour(s), "}
      if (mins>0) {result+=mins%60+" minute(s), "}
      if (secs>0) {result+=secs%60+" second(s)"}
      if (result==="") {return "0 second"}
      else {return result}
    }
    function calcMark() {
      let mt=lenq
      let fl=0
      let tr=0
      for (let i=0;i<answerKey.length;i++) {
        let ans=answerKey.charAt(i)===answers[i]
        if (ans===true) {
          tr++
          mt--
          selectors[i].classList.add("true")
        }
        else if (ans===false && answers[i]!==" ") {
          fl++
          mt--
          selectors[i].classList.add("false")
        }
        else {
          selectors[i].classList.add("empty")
        }
      }
      const ppq=100/lenq
      const wtar=ppq/(Array.from(questions[0].getElementsByTagName("input")).length-2)
      const net=tr*ppq-wtar*fl
      const nwc=ppq*tr
      document.querySelector("footer").innerHTML=`
            <fieldset>
                <legend>Result</legend>
                <p>True: <span id="true-count">${tr}</span></p>
                <p>False <span id="false-count">${fl}</span></p>
                <p>Empty: <span id="empty-count">${mt}</span></p>
                <p>Time: ${humanizeTime(performance.now()-startTime)}</p>
                <p>Score Without Correction: ${nwc.toFixed(2)}<br/>
                Score With Correction: ${net.toFixed(2)}</p>
            </fieldset>
            `
    }
    function doFinishExam(answ) {
      if (answ===true) {
        radios.forEach(element=>{element.disabled=true})
        for (let i=0;i<answerKey.length;i++) {
          questions[i].querySelector(`input[value=${answerKey.charAt(i)}]`).parentElement.style.color="green"
          questions[i].querySelector(`input[value=${answerKey.charAt(i)}]`).parentElement.style.fontWeight="bold"
          questions[i].querySelector(`input[value=${answerKey.charAt(i)}]`).style.fontWeight="bold"
        }
        calcMark()
        confirmation.parentElement.removeChild(confirmation)
        finished=true
      }
      else {
        confirmation.style.display="none"
      }
      asked=false
    }
    function promptToFinish() {
      confirmation.style.display="flex"
      asked=true
    }
    window.onkeydown=key=> {
      if (finished===false) {
        if (key.keyCode===65) {questions[curr].querySelector("input[value=A]").checked=true;updateNavBar(curr,"A")}
        if (key.keyCode===66) {questions[curr].querySelector("input[value=B]").checked=true;updateNavBar(curr,"B")}
        if (key.keyCode===67) {questions[curr].querySelector("input[value=C]").checked=true;updateNavBar(curr,"C")}
        if (key.keyCode===68) {questions[curr].querySelector("input[value=D]").checked=true;updateNavBar(curr,"D")}
        if (key.keyCode===69) {questions[curr].querySelector("input[value=E]").checked=true;updateNavBar(curr,"E")}
        if (key.keyCode===8)  {questions[curr].querySelector("input[value=' ']").checked=true;updateNavBar(curr," ")}
        if (key.keyCode===35) {promptToFinish()}
        if (key.keyCode===27) {doFinishExam(false)}
        if (key.keyCode===13 && asked===true) {doFinishExam(true)}
      }
      if ([39].includes(key.keyCode)) {nextQ()}
      if ([37].includes(key.keyCode)) {prevQ()}
    }
    showQ(0)
    for (let i=0;i<answerKey.length;i++) {
      questions[i].querySelector("input[value=' ']").checked=true;
    }"""
def parse(inp,out): 
    content=inp.split("\n")
    result=""
    question=0
    for line in content[1:-1]:
        print(line)
        if line.strip()=="": continue
        elif line[0] in "0123456789":
            if ")" in line:
                parenthesis=line.split(")")
                if "(" not in parenthesis[0]:
                    result+=((f"    <label><input  type=\"radio\" name=\"{question}\" value=\" \" checked/> Leave Blank.</label>\n</fieldset>\n" if question!=0 else "")+f"<fieldset>\n    <legend>Question {parenthesis[0]}</legend>\n    <p>"+line[len(parenthesis[0])+1:].strip()+"</p>\n")
                    question+=1
        elif line[0] in "ABCDE" and line[1]==")":
            result+=(f"    <label><input autocomplete=\"off\" type=\"radio\" name=\"{question}\" value=\"{line[0]}\"/> "+line[2:].strip()+"</label>\n")
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
<style>
    {CSS}
</style>
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
"""+result+f"""    <label><input type=\"radio\" name=\"{question}\" value=\" \"/ checked> Leave Blank.</label>\n</fieldset>
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
<script>
    {JS}
</script>
</html>"""
    with open(out,"w",encoding="UTF-8") as file: file.write(html)
