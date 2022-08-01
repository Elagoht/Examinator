const questions=Array.from(document.getElementsByTagName("fieldset"))
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
      questions[i].querySelector(`input[value=${answerKey.charAt(i)}]`).style.backgroundColor="gold"
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
