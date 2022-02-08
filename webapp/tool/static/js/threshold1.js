var selectAge = document.getElementById("selectThreshold");
var contents;
contents += "<option value='' disabled selected hidden>{{threshold.low}}</option>"
for (let i = 1; i <= 100; i++) {
  contents += "<option>" + i + "</option>";
}
selectAge.innerHTML = contents;