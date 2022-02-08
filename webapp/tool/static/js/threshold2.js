var selectAge = document.getElementById("selectThreshold2");
var contents;
contents += "<option value='' disabled selected hidden>{{threshold.medium}}</option>"
for (let i = 1; i <= 100; i++) {
  contents += "<option>" + i + "</option>";
}

selectAge.innerHTML = contents;